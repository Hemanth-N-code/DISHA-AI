# backend/app/api/skill_gap.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.profile import StudentProfile
from app.models.career import Career
from app.schemas.skill_gap import SkillGapResponse
from app.api.deps import get_current_user
from app.recommendation.skill_gap import analyze_skill_gap

router = APIRouter(prefix="/skill-gap", tags=["Skill Gap Analysis"])

@router.get("/{career_id}", response_model=SkillGapResponse)
def get_skill_gap_for_career(
    career_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Student profile required for skill gap analysis.")

    career = db.query(Career).filter(Career.career_id == career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found.")

    res = analyze_skill_gap(profile, career)
    return res
