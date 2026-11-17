# backend/app/schemas/comparison.py
from pydantic import BaseModel
from typing import List, Dict, Any
from app.schemas.scoring import ScoreBreakdown

class CareerComparisonItem(BaseModel):
    career_id: str
    career_name: str
    domain: str
    description: str
    education_duration: str
    typical_work: str
    score_breakdown: ScoreBreakdown
    key_skills_required: List[str]
    missing_skills_count: int
    future_readiness_score: float
    work_characteristics: Dict[str, str]
    learning_curve_complexity: str  # Moderate | High | Steep
    sample_entry_role: str

class CompareRequest(BaseModel):
    career_ids: List[str]  # 2 to 4 career ids

class CompareResponse(BaseModel):
    compared_careers: List[CareerComparisonItem]
    neutral_observations: List[str]
    tradeoff_insights: Dict[str, str]
