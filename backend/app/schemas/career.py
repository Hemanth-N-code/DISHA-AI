# backend/app/schemas/career.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.schemas.scoring import ScoreBreakdown

class CareerRequiredSkill(BaseModel):
    skill: str
    level: int
    importance: str

class AIImpactDetail(BaseModel):
    automated_tasks: List[str] = []
    augmented_tasks: List[str] = []
    human_skills: List[str] = []

class CareerBase(BaseModel):
    career_id: str
    career_name: str
    domain: str
    description: str
    typical_work: str
    eligibility: str

class CareerCandidate(CareerBase):
    score_breakdown: ScoreBreakdown
    is_diversity_highlight: bool = False
    diversity_domain: str

class CareerDetail(CareerBase):
    id: int
    education_paths: List[str]
    required_skills: List[Dict[str, Any]]
    soft_skills: List[str]
    related_careers: List[str]
    alternative_careers: List[str]
    adjacent_careers: List[str]
    entry_level_roles: List[str]
    higher_study_options: List[str]
    certifications: List[str]
    projects: List[str]
    portfolio_requirements: List[str]
    internship_options: List[str]
    future_skills: List[str]
    technology_changes: Optional[str]
    ai_impact: Dict[str, Any]
    pathway: Optional[str]
    sources: List[str]

    class Config:
        from_attributes = True

class CareerDiscoverRequest(BaseModel):
    apply_diversity: bool = True
    domain_filter: Optional[str] = None
    limit: int = 15

class CareerDiscoverResponse(BaseModel):
    total_careers_in_universe: int
    domains_represented: List[str]
    career_diversity_index: float
    candidates: List[CareerCandidate]
    discovery_strategy: str
