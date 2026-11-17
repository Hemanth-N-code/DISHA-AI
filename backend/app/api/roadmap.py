# backend/app/api/roadmap.py
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User
from app.models.career import Career
from app.models.profile import StudentProfile
from app.models.roadmap import Roadmap, RoadmapTask
from app.schemas.roadmap import RoadmapCreateRequest, RoadmapResponse, RoadmapTaskUpdate, RoadmapTaskSchema
from app.api.deps import get_current_user
from app.agents.roadmap_agent import roadmap_agent
from app.memory.service import memory_service

router = APIRouter(prefix="/roadmap", tags=["Roadmap"])

@router.post("/generate", response_model=RoadmapResponse)
def generate_roadmap_endpoint(
    req: RoadmapCreateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == user.id).first()
    if not profile:
        raise HTTPException(status_code=400, detail="Student profile required to generate a personalized roadmap.")

    career = db.query(Career).filter(Career.career_id == req.career_id).first()
    if not career:
        raise HTTPException(status_code=404, detail="Career not found.")

    # Remove existing roadmap for this career if regenerating, or update
    existing_roadmap = db.query(Roadmap).filter(
        Roadmap.user_id == user.id,
        Roadmap.career_id == req.career_id
    ).first()
    if existing_roadmap:
        db.delete(existing_roadmap)
        db.commit()

    # Generate phased tasks using Roadmap Agent
    tasks_data = roadmap_agent.generate_roadmap(profile, career, horizon_months=req.target_horizon_months)

    roadmap = Roadmap(
        user_id=user.id,
        career_id=career.career_id,
        career_name=career.career_name,
        target_horizon_months=req.target_horizon_months,
        overall_progress=0.0
    )
    db.add(roadmap)
    db.commit()
    db.refresh(roadmap)

    for t in tasks_data:
        task = RoadmapTask(
            roadmap_id=roadmap.id,
            title=t["title"],
            description=t["description"],
            category=t["category"],
            stage_index=t["stage_index"],
            estimated_weeks=t["estimated_weeks"],
            status="not_started",
            portfolio_artifact=t.get("portfolio_artifact")
        )
        db.add(task)

    db.commit()
    db.refresh(roadmap)

    memory_service.log_event(db, user.id, "roadmap_created", {"career_id": career.career_id, "tasks": len(tasks_data)})
    return roadmap

@router.get("", response_model=List[RoadmapResponse])
def get_user_roadmaps(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roadmaps = db.query(Roadmap).filter(Roadmap.user_id == user.id).all()
    return roadmaps

@router.get("/{career_id}", response_model=RoadmapResponse)
def get_roadmap_by_career(
    career_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roadmap = db.query(Roadmap).filter(
        Roadmap.user_id == user.id,
        Roadmap.career_id == career_id
    ).first()
    if not roadmap:
        raise HTTPException(status_code=404, detail="No active roadmap found for this career.")
    return roadmap

@router.put("/tasks/{task_id}", response_model=RoadmapTaskSchema)
def update_task_status(
    task_id: int,
    req: RoadmapTaskUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    task = db.query(RoadmapTask).filter(RoadmapTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Roadmap task not found.")

    roadmap = db.query(Roadmap).filter(Roadmap.id == task.roadmap_id).first()
    if not roadmap or roadmap.user_id != user.id:
        raise HTTPException(status_code=403, detail="Unauthorized access to roadmap task.")

    if req.status:
        task.status = req.status
        if req.status == "completed":
            task.completed_at = datetime.now(timezone.utc)
            memory_service.log_event(db, user.id, "roadmap_task_completed", {"task_id": task.id, "title": task.title})
        else:
            task.completed_at = None

    if req.portfolio_artifact is not None:
        task.portfolio_artifact = req.portfolio_artifact

    db.commit()

    # Recalculate overall roadmap progress
    all_tasks = db.query(RoadmapTask).filter(RoadmapTask.roadmap_id == roadmap.id).all()
    if all_tasks:
        completed_count = sum(1 for t in all_tasks if t.status == "completed")
        roadmap.overall_progress = round((completed_count / len(all_tasks)) * 100.0, 1)
        db.commit()

    db.refresh(task)
    return task
