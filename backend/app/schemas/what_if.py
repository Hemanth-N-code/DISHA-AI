# backend/app/schemas/what_if.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.schemas.career import CareerCandidate

class WhatIfRequest(BaseModel):
    programming_preference: Optional[str] = None  # none | low | moderate | high
    mathematics_preference: Optional[str] = None   # low | moderate | high
    creativity_level: Optional[str] = None         # low | moderate | high
    people_interaction_preference: Optional[str] = None # low | balanced | high
    added_interests: Optional[List[str]] = None
    removed_interests: Optional[List[str]] = None
    constraint_relaxation: Optional[str] = None
    save_as_permanent: bool = False

class ScenarioDelta(BaseModel):
    career_id: str
    career_name: str
    domain: str
    previous_score: float
    new_score: float
    score_change: float
    status: str  # "surged" | "declined" | "newly_unlocked" | "stable"
    reason: str

class WhatIfResponse(BaseModel):
    scenario_description: str
    current_top_careers: List[CareerCandidate]
    what_if_top_careers: List[CareerCandidate]
    deltas: List[ScenarioDelta]
    explanation: str
    diversity_index_current: float
    diversity_index_what_if: float
