# backend/app/api/careers.py
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.career import Career
from app.models.profile import StudentProfile
from app.schemas.career import CareerDetail, CareerDiscoverRequest, CareerDiscoverResponse
from app.schemas.comparison import CompareRequest, CompareResponse, CareerComparisonItem
from app.api.deps import get_current_user, get_current_user_optional
from app.agents.discovery_agent import discovery_agent
from app.agents.analysis_agent import analysis_agent
from app.recommendation.graph import build_career_graph
from app.recommendation.engine import calculate_career_score
from app.recommendation.skill_gap import analyze_skill_gap
from app.memory.service import memory_service

router = APIRouter(prefix="/careers", tags=["Careers"])

@router.get("", response_model=List[CareerDetail])
def list_careers(
    domain: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Career)
    if domain:
        query = query.filter(Career.domain == domain)
    if search:
        s = f"%{search}%"
        query = query.filter(Career.career_name.ilike(s) | Career.description.ilike(s))
    return query.offset(skip).limit(limit).all()

@router.get("/{career_id}", response_model=CareerDetail)
def get_career_by_id(
    career_id: str,
    db: Session = Depends(get_db),
    user: Optional[User] = Depends(get_current_user_optional)
):
    career = db.query(Career).filter(Career.career_id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found.")
        
    # Log exploration in memory service if user is authenticated
    if user:
        memory_service.record_explored_career(db, user.id, career.career_id, career.career_name)
        
    return career

@router.post("/discover", response_model=CareerDiscoverResponse)
def discover_careers(
    req: CareerDiscoverRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Please complete student onboarding first.")

    all_careers = db.query(Career).all()
    if not all_careers:
        raise HTTPException(status_code=500, detail="Career knowledge base is empty. Please run database seed.")

    res = discovery_agent.discover_careers(
        profile=profile,
        all_careers=all_careers,
        apply_diversity=req.apply_diversity,
        domain_filter=req.domain_filter,
        limit=req.limit
    )
    return res

@router.post("/{career_id}/analyze")
def analyze_career(
    career_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Profile required for personalized analysis.")

    career = db.query(Career).filter(Career.career_id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found.")

    memory_context = memory_service.get_student_memory_context(db, user.id)
    analysis = analysis_agent.analyze_career_path(profile, career, memory_context)
    return analysis

@router.get("/{career_id}/graph")
def get_career_path_graph(career_id: str, db: Session = Depends(get_db)):
    career = db.query(Career).filter(Career.career_id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found.")

    all_careers = db.query(Career).all()
    careers_map = {c.career_id: c for c in all_careers}
    
    graph_data = build_career_graph(career, careers_map)
    return graph_data

@router.post("/compare", response_model=CompareResponse)
def compare_careers(
    req: CompareRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if len(req.career_ids) < 2 or len(req.career_ids) > 4:
        raise HTTPException(status_code=400, detail="Please select between 2 and 4 careers to compare.")

    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Profile required for personalized comparison.")

    careers = db.query(Career).filter(Career.career_id.in_(req.career_ids)).all()
    if len(careers) < len(req.career_ids):
        found_ids = {c.career_id for c in careers}
        missing = set(req.career_ids) - found_ids
        raise HTTPException(status_code=404, detail=f"Careers not found: {missing}")

    items: List[CareerComparisonItem] = []
    neutral_obs: List[str] = []
    tradeoffs: dict = {}

    for c in careers:
        score_breakdown = calculate_career_score(profile, c)
        gap = analyze_skill_gap(profile, c)
        
        # Determine complexity & characteristics
        edu_dur = "3-4 Years Bachelor's Degree"
        if any("5" in p or "mbbs" in p.lower() or "ll.b" in p.lower() for p in c.education_paths):
            edu_dur = "5+ Years Professional Degree"
        elif any("diploma" in p.lower() or "iti" in p.lower() for p in c.education_paths):
            edu_dur = "2-3 Years Vocational Diploma"

        complexity = "Moderate"
        if gap.gap_skills_count >= 4 or "ai_engineer" in c.career_id or "quant" in c.career_id:
            complexity = "Steep Learning Curve"
        elif gap.gap_skills_count >= 2:
            complexity = "Intermediate Curve"

        future_resilience = 85.0
        if c.ai_impact and c.ai_impact.get("human_skills"):
            future_resilience = 92.0

        item = CareerComparisonItem(
            career_id=c.career_id,
            career_name=c.career_name,
            domain=c.domain,
            description=c.description,
            education_duration=edu_dur,
            typical_work=c.typical_work,
            score_breakdown=score_breakdown,
            key_skills_required=[s.get("skill", "") for s in (c.required_skills or [])[:3]],
            missing_skills_count=gap.gap_skills_count,
            future_readiness_score=future_resilience,
            work_characteristics={
                "domain": c.domain,
                "team_style": "Collaborative Cross-Functional" if "design" in c.domain.lower() or "product" in c.career_id else "Technical / Analytical",
                "eligibility": c.eligibility
            },
            learning_curve_complexity=complexity,
            sample_entry_role=c.entry_level_roles[0] if c.entry_level_roles else "Associate Specialist"
        )
        items.append(item)

    # Generate neutral observation
    c_names = [c.career_name for c in careers]
    neutral_obs.append(f"Comparing across {len(set(c.domain for c in careers))} distinct domain(s): {', '.join(set(c.domain for c in careers))}.")
    neutral_obs.append("Notice differences in daily task profiles, upfront educational commitment, and technical skill prerequisite requirements.")
    neutral_obs.append("Remember: No single path is an absolute 'winner'. The best choice aligns with your personal trade-offs and readiness to learn.")

    for c in items:
        tradeoffs[c.career_name] = (
            f"Offers {c.score_breakdown.overall_score}% compatibility with {c.education_duration}. "
            f"Requires bridging {c.missing_skills_count} skill area(s) with {c.learning_curve_complexity.lower()}."
        )

    # Log comparison event in research metrics
    memory_service.log_event(db, user.id, "career_compared", {"careers": req.career_ids})

    return CompareResponse(
        compared_careers=items,
        neutral_observations=neutral_obs,
        tradeoff_insights=tradeoffs
    )
