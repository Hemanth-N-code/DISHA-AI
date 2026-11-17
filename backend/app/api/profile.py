# backend/app/api/profile.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.profile import StudentProfile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse, ProfileAnalysisResponse
from app.api.deps import get_current_user
from app.agents.profile_agent import profile_agent

router = APIRouter(prefix="/profile", tags=["Student Profile"])

@router.get("", response_model=ProfileResponse)
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Student profile not found. Please complete onboarding.")
    return profile

@router.post("", response_model=ProfileResponse)
def create_or_update_profile(req: ProfileCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Run through Profile Agent to synthesize archetype and summary
    agent_output = profile_agent.process_profile(req)
    
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    skills_json = [{"skill": s.skill or s.name, "name": s.skill or s.name, "level": s.level} for s in req.skills]
    
    if not profile:
        profile = StudentProfile(
            user_id=user.id,
            education_level=req.education_level,
            stream=req.stream,
            subjects=req.subjects,
            marks_percentage=req.marks_percentage,
            favorite_subjects=req.favorite_subjects,
            interests=req.interests,
            skills=skills_json,
            preferences=req.preferences,
            goals=req.goals,
            constraints=req.constraints,
            programming_preference=req.programming_preference,
            mathematics_preference=req.mathematics_preference,
            creativity_level=req.creativity_level,
            people_interaction_preference=req.people_interaction_preference,
            profile_summary=agent_output["profile_summary"],
            academic_strengths=agent_output["academic_strengths"]
        )
        db.add(profile)
    else:
        profile.education_level = req.education_level
        profile.stream = req.stream
        profile.subjects = req.subjects
        profile.marks_percentage = req.marks_percentage
        profile.favorite_subjects = req.favorite_subjects
        profile.interests = req.interests
        profile.skills = skills_json
        profile.preferences = req.preferences
        profile.goals = req.goals
        profile.constraints = req.constraints
        profile.programming_preference = req.programming_preference
        profile.mathematics_preference = req.mathematics_preference
        profile.creativity_level = req.creativity_level
        profile.people_interaction_preference = req.people_interaction_preference
        profile.profile_summary = agent_output["profile_summary"]
        profile.academic_strengths = agent_output["academic_strengths"]

    db.commit()
    db.refresh(profile)
    return profile

@router.put("", response_model=ProfileResponse)
def update_profile(req: ProfileUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")

    update_data = req.dict(exclude_unset=True)
    if "skills" in update_data and update_data["skills"] is not None:
        update_data["skills"] = [s.dict() if hasattr(s, "dict") else s for s in update_data["skills"]]

    for key, value in update_data.items():
        setattr(profile, key, value)

    # Re-run Profile Agent to refresh synthesis
    from app.schemas.profile import ProfileCreate
    current_state = ProfileCreate(
        education_level=profile.education_level,
        stream=profile.stream,
        subjects=profile.subjects or [],
        marks_percentage=profile.marks_percentage,
        favorite_subjects=profile.favorite_subjects or [],
        interests=profile.interests or [],
        skills=profile.skills or [],
        preferences=profile.preferences or [],
        goals=profile.goals or [],
        constraints=profile.constraints or [],
        programming_preference=profile.programming_preference,
        mathematics_preference=profile.mathematics_preference,
        creativity_level=profile.creativity_level,
        people_interaction_preference=profile.people_interaction_preference
    )
    agent_output = profile_agent.process_profile(current_state)
    profile.profile_summary = agent_output["profile_summary"]
    profile.academic_strengths = agent_output["academic_strengths"]

    db.commit()
    db.refresh(profile)
    return profile

@router.post("/analyze", response_model=ProfileAnalysisResponse)
def analyze_profile_data(req: ProfileCreate):
    res = profile_agent.process_profile(req)
    return ProfileAnalysisResponse(**res)
