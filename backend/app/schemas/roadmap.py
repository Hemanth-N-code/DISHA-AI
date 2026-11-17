# backend/app/schemas/roadmap.py
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class RoadmapTaskSchema(BaseModel):
    id: int
    roadmap_id: int
    title: str
    description: str
    category: str  # Foundation | Core Skills | Projects | Portfolio | Internship
    stage_index: int
    estimated_weeks: int
    status: str  # not_started | in_progress | completed
    portfolio_artifact: Optional[str] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class RoadmapCreateRequest(BaseModel):
    career_id: str
    target_horizon_months: int = 6

class RoadmapTaskUpdate(BaseModel):
    status: Optional[str] = None  # not_started | in_progress | completed
    portfolio_artifact: Optional[str] = None

class RoadmapResponse(BaseModel):
    id: int
    user_id: int
    career_id: str
    career_name: str
    target_horizon_months: int
    overall_progress: float
    created_at: datetime
    tasks: List[RoadmapTaskSchema]

    class Config:
        from_attributes = True
