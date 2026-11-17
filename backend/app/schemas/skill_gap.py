# backend/app/schemas/skill_gap.py
from pydantic import BaseModel
from typing import List

class SkillGapItem(BaseModel):
    skill_name: str
    current_level: int       # 0 to 5
    required_level: int      # 1 to 5
    gap: int                 # required - current (min 0)
    category: str            # "existing" | "partially_developed" | "missing"
    priority: str            # "Critical" | "High" | "Medium"
    recommended_action: str

class SkillGapResponse(BaseModel):
    career_id: str
    career_name: str
    total_skills_evaluated: int
    matched_skills_count: int
    gap_skills_count: int
    readiness_percentage: float
    skills_breakdown: List[SkillGapItem]
    top_priority_focus_areas: List[str]
    estimated_upskilling_months: int
