# backend/app/api/cet.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database.session import get_db
from app.api.deps import get_current_user, get_current_user_optional
from app.models.user import User
from app.models.cet import (
    Exam, CetDomain, College, CollegeBranch, HistoricalCutoff,
    CollegePlacement, StudentCetProfile, OptionEntryList, OptionEntryItem,
    CetResearchEvent
)
from app.schemas.cet import (
    ExamResponse, CetDomainResponse, CollegeDetailResponse, CollegeBranchItem,
    StudentCetProfileCreate, StudentCetProfileResponse,
    CetAnalyzeRequest, CetAnalyzeResponse, CutoffTrendResponse,
    CollegeCompareRequest, OptionItemCreate, OptionItemResponse,
    OptionListResponse, OptionListReorderRequest
)
from app.recommendation.cet_engine import (
    analyze_student_options, get_cutoff_trend, compare_colleges,
    map_career_to_cet_branches
)

router = APIRouter(prefix="/cet", tags=["CET-Support"])

DISCLAIMER = (
    "Historical cutoff data is indicative only. Actual allotment depends on the current year's "
    "cutoff, seat availability, category, course, round, reservation and KEA counselling rules."
)

@router.get("/exams", response_model=List[ExamResponse])
def get_supported_exams(db: Session = Depends(get_db)):
    """Returns list of supported entrance examinations (extensible architecture)."""
    return db.query(Exam).filter(Exam.is_active == True).all()

@router.get("/domains", response_model=List[CetDomainResponse])
def get_exam_domains(exam_id: str = "kcet", db: Session = Depends(get_db)):
    """Returns supported counseling domains (Engineering, Pharmacy, Agriculture)."""
    return db.query(CetDomain).filter(
        CetDomain.exam_id == exam_id,
        CetDomain.is_active == True
    ).all()

@router.post("/profile", response_model=StudentCetProfileResponse)
def create_or_update_cet_profile(
    req: StudentCetProfileCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Saves or updates the student's entrance exam rank, category, and preferences."""
    profile = db.query(StudentCetProfile).filter(StudentCetProfile.user_id == user.id).first()
    if profile:
        profile.exam_id = req.exam_id
        profile.domain_id = req.domain_id
        profile.rank = req.rank
        profile.category = req.category
        profile.sub_category = req.sub_category
        profile.gender = req.gender
        profile.preferred_branches = req.preferred_branches
        profile.preferred_locations = req.preferred_locations
        profile.preferences = req.preferences
    else:
        profile = StudentCetProfile(
            user_id=user.id,
            exam_id=req.exam_id,
            domain_id=req.domain_id,
            rank=req.rank,
            category=req.category,
            sub_category=req.sub_category,
            gender=req.gender,
            preferred_branches=req.preferred_branches,
            preferred_locations=req.preferred_locations,
            preferences=req.preferences
        )
        db.add(profile)

    # Log research event
    db.add(CetResearchEvent(
        user_id=user.id,
        event_type="cet_profile_saved",
        event_data={"rank": req.rank, "category": req.category, "exam": req.exam_id}
    ))

    db.commit()
    db.refresh(profile)
    return profile

@router.get("/profile", response_model=Optional[StudentCetProfileResponse])
def get_student_cet_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves current student's saved CET profile."""
    return db.query(StudentCetProfile).filter(StudentCetProfile.user_id == user.id).first()

@router.post("/analyze", response_model=CetAnalyzeResponse)
def analyze_options(
    req: CetAnalyzeRequest,
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """
    Analyzes historical cutoffs against student rank, categorizing options into:
    - Strong historical match
    - Possible match
    - Lower historical cutoff / safer option
    - Competitive option
    """
    options = analyze_student_options(
        db=db,
        rank=req.rank,
        category=req.category,
        domain_id=req.domain_id,
        preferred_branches=req.preferred_branches,
        preferred_locations=req.preferred_locations,
        preferences=req.preferences,
        round_num=req.round_num,
        sort_by=req.sort_by
    )

    strong_c = sum(1 for o in options if o["historical_match_label"] == "Strong historical match")
    possible_c = sum(1 for o in options if o["historical_match_label"] == "Possible match")
    safer_c = sum(1 for o in options if o["historical_match_label"] == "Lower historical cutoff / safer option")
    comp_c = sum(1 for o in options if o["historical_match_label"] == "Competitive option")

    if user:
        db.add(CetResearchEvent(
            user_id=user.id,
            event_type="cet_search_analyzed",
            event_data={"rank": req.rank, "category": req.category, "matches_count": len(options)}
        ))
        db.commit()

    return CetAnalyzeResponse(
        student_rank=req.rank,
        category=req.category,
        round_num=req.round_num,
        total_options_evaluated=len(options),
        strong_matches_count=strong_c,
        possible_matches_count=possible_c,
        safer_matches_count=safer_c,
        competitive_matches_count=comp_c,
        options=options,
        disclaimer=DISCLAIMER
    )

@router.get("/colleges", response_model=List[CollegeDetailResponse])
def list_colleges(
    city: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lists colleges with branch and placement summaries."""
    query = db.query(College)
    if city and city != "Any":
        query = query.filter(College.city == city)
    if search:
        s = f"%{search.lower()}%"
        query = query.filter(College.name.ilike(s) | College.short_name.ilike(s))

    colleges = query.all()
    results = []
    for c in colleges:
        placement = db.query(CollegePlacement).filter(CollegePlacement.college_id == c.id).order_by(CollegePlacement.year.desc()).first()
        results.append(CollegeDetailResponse(
            id=c.id,
            code=c.code,
            name=c.name,
            short_name=c.short_name,
            location=c.location,
            city=c.city,
            district=c.district,
            college_type=c.college_type,
            website=c.website,
            established_year=c.established_year,
            accreditation=c.accreditation,
            campus_area_acres=c.campus_area_acres,
            hostel_facility=c.hostel_facility,
            description=c.description,
            source=c.source,
            source_url=c.source_url,
            branches=[CollegeBranchItem.model_validate(b) for b in c.branches if b.is_active],
            placement=placement
        ))
    return results

@router.get("/colleges/{college_id}", response_model=CollegeDetailResponse)
def get_college_detail(college_id: str, db: Session = Depends(get_db)):
    """Retrieves deep-dive details for an individual college."""
    col = db.query(College).filter(College.id == college_id).first()
    if not col:
        raise HTTPException(status_code=404, detail="College not found")

    placement = db.query(CollegePlacement).filter(CollegePlacement.college_id == col.id).order_by(CollegePlacement.year.desc()).first()

    return CollegeDetailResponse(
        id=col.id,
        code=col.code,
        name=col.name,
        short_name=col.short_name,
        location=col.location,
        city=col.city,
        district=col.district,
        college_type=col.college_type,
        website=col.website,
        established_year=col.established_year,
        accreditation=col.accreditation,
        campus_area_acres=col.campus_area_acres,
        hostel_facility=col.hostel_facility,
        description=col.description,
        source=col.source,
        source_url=col.source_url,
        branches=[CollegeBranchItem.model_validate(b) for b in col.branches if b.is_active],
        placement=placement
    )

@router.get("/college/{college_id}/trend", response_model=CutoffTrendResponse)
def get_college_cutoff_trend(
    college_id: str,
    branch: str = "CS",
    category: str = "GM",
    round_num: int = 1,
    db: Session = Depends(get_db)
):
    """Returns multi-year closing rank history for trend line visualization."""
    return get_cutoff_trend(db, college_id, branch, category, round_num)

@router.post("/compare")
def compare_colleges_endpoint(
    req: CollegeCompareRequest,
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Side-by-side comparison across 2-4 colleges for a specific branch."""
    if len(req.college_ids) < 2 or len(req.college_ids) > 4:
        raise HTTPException(status_code=400, detail="Please select between 2 and 4 colleges to compare.")

    result = compare_colleges(db, req.college_ids, req.branch_code, req.category)

    if user:
        db.add(CetResearchEvent(
            user_id=user.id,
            event_type="college_compared",
            event_data={"colleges": req.college_ids, "branch": req.branch_code}
        ))
        db.commit()

    return result

@router.get("/option-list", response_model=OptionListResponse)
def get_option_list(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retrieves the student's personal option-entry list."""
    opt_list = db.query(OptionEntryList).filter(OptionEntryList.user_id == user.id).first()
    if not opt_list:
        # Create empty list
        profile = db.query(StudentCetProfile).filter(StudentCetProfile.user_id == user.id).first()
        profile_id = profile.id if profile else 0
        opt_list = OptionEntryList(user_id=user.id, cet_profile_id=profile_id, title="My KCET Option Entry Plan")
        db.add(opt_list)
        db.commit()
        db.refresh(opt_list)

    items_res = []
    for it in opt_list.items:
        cb = it.college_branch
        col = cb.college
        items_res.append(OptionItemResponse(
            id=it.id,
            option_list_id=it.option_list_id,
            college_branch_id=it.college_branch_id,
            priority_order=it.priority_order,
            historical_category=it.historical_category,
            student_notes=it.student_notes,
            college_name=col.name,
            college_short_name=col.short_name,
            branch_name=cb.branch_name,
            branch_code=cb.branch_code,
            city=col.city
        ))

    items_res.sort(key=lambda x: x.priority_order)

    return OptionListResponse(
        id=opt_list.id,
        user_id=user.id,
        title=opt_list.title,
        notes=opt_list.notes,
        items=items_res,
        disclaimer=DISCLAIMER
    )

@router.post("/option-list/item")
def add_item_to_option_list(
    req: OptionItemCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Adds a college branch choice to the student's option list."""
    opt_list = db.query(OptionEntryList).filter(OptionEntryList.user_id == user.id).first()
    if not opt_list:
        profile = db.query(StudentCetProfile).filter(StudentCetProfile.user_id == user.id).first()
        profile_id = profile.id if profile else 0
        opt_list = OptionEntryList(user_id=user.id, cet_profile_id=profile_id)
        db.add(opt_list)
        db.commit()
        db.refresh(opt_list)

    # Check if already in list
    existing = db.query(OptionEntryItem).filter(
        OptionEntryItem.option_list_id == opt_list.id,
        OptionEntryItem.college_branch_id == req.college_branch_id
    ).first()
    if existing:
        return {"status": "already_exists", "item_id": existing.id}

    current_max = db.query(OptionEntryItem).filter(
        OptionEntryItem.option_list_id == opt_list.id
    ).count()

    new_item = OptionEntryItem(
        option_list_id=opt_list.id,
        college_branch_id=req.college_branch_id,
        priority_order=current_max + 1,
        historical_category=req.historical_category,
        student_notes=req.student_notes
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    db.add(CetResearchEvent(
        user_id=user.id,
        event_type="option_added",
        event_data={"branch_id": req.college_branch_id, "priority": current_max + 1}
    ))
    db.commit()

    return {"status": "added", "item_id": new_item.id, "priority_order": new_item.priority_order}

@router.put("/option-list/reorder", response_model=OptionListResponse)
def reorder_option_list(
    req: OptionListReorderRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Reorders the student's option-entry preferences according to their manual adjustment."""
    opt_list = db.query(OptionEntryList).filter(OptionEntryList.user_id == user.id).first()
    if not opt_list:
        raise HTTPException(status_code=404, detail="Option list not found")

    items_map = {it.id: it for it in opt_list.items}
    for idx, item_id in enumerate(req.ordered_item_ids):
        if item_id in items_map:
            items_map[item_id].priority_order = idx + 1

    db.add(CetResearchEvent(
        user_id=user.id,
        event_type="option_reordered",
        event_data={"total_items": len(req.ordered_item_ids)}
    ))
    db.commit()
    return get_option_list(user=user, db=db)

@router.delete("/option-list/item/{item_id}")
def delete_option_item(
    item_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Removes a choice from the student's option-entry list."""
    item = db.query(OptionEntryItem).join(OptionEntryList).filter(
        OptionEntryItem.id == item_id,
        OptionEntryList.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    opt_list_id = item.option_list_id
    db.delete(item)
    db.commit()

    # Re-normalize priority numbers
    remaining = db.query(OptionEntryItem).filter(
        OptionEntryItem.option_list_id == opt_list_id
    ).order_by(OptionEntryItem.priority_order.asc()).all()

    for idx, it in enumerate(remaining):
        it.priority_order = idx + 1

    db.commit()
    return {"status": "removed"}

@router.get("/career-branches/{career_id}")
def get_branches_for_career(career_id: str):
    """Maps a DISHA career recommendation into relevant undergraduate CET branches."""
    return {
        "career_id": career_id,
        "recommended_academic_branches": map_career_to_cet_branches(career_id)
    }

@router.post("/log-event")
def log_cet_event(
    event_type: str,
    data: dict,
    user: Optional[User] = Depends(get_current_user_optional),
    db: Session = Depends(get_db)
):
    """Logs CET research and navigation events for research analysis."""
    ev = CetResearchEvent(
        user_id=user.id if user else None,
        event_type=event_type,
        event_data=data
    )
    db.add(ev)
    db.commit()
    return {"status": "logged"}
