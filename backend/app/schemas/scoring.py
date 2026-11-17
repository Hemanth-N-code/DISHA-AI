# backend/app/schemas/scoring.py
from pydantic import BaseModel
from typing import List

class FactorTag(BaseModel):
    positive: bool
    text: str

class ScoreBreakdown(BaseModel):
    overall_score: float
    interest_fit: float
    academic_fit: float
    skill_fit: float
    preference_fit: float
    goal_fit: float
    factor_tags: List[FactorTag] = []
    explanation: str
