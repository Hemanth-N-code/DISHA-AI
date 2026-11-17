# backend/app/api/memory.py
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.schemas.memory import JourneyResponse
from app.api.deps import get_current_user
from app.memory.service import memory_service

router = APIRouter(prefix="/memory", tags=["Student Memory & Journey"])

class SaveCareerRequest(BaseModel):
    career_id: str
    career_name: str

class RejectCareerRequest(BaseModel):
    career_id: str
    career_name: str
    reason: str

@router.get("/journey", response_model=JourneyResponse)
def get_student_decision_journey(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    journey = memory_service.get_student_journey(db, user.id)
    return journey

@router.post("/save-career")
def toggle_save_career(
    req: SaveCareerRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    is_saved = memory_service.toggle_saved_career(db, user.id, req.career_id, req.career_name)
    return {"career_id": req.career_id, "is_saved": is_saved}

@router.post("/reject-career")
def reject_career(
    req: RejectCareerRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    memory_service.record_rejected_career(db, user.id, req.career_id, req.career_name, req.reason)
    return {"status": "success", "career_id": req.career_id, "reason": req.reason}
