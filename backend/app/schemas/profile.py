# backend/app/schemas/profile.py
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class SkillItem(BaseModel):
    skill: Optional[str] = None
    name: Optional[str] = None
    level: int = 3  # 1 to 5
    verified: Optional[bool] = False

    def model_post_init(self, __context: Any) -> None:
        if not self.skill and self.name:
            self.skill = self.name
        elif not self.name and self.skill:
            self.name = self.skill
        if not self.skill:
            self.skill = "General Skill"

class ProfileCreate(BaseModel):
    education_level: str = "12th / Intermediate / PUC"
    stream: str  # Science (PCM), Science (PCB), Commerce, Arts/Humanities, Vocational
    subjects: List[str] = []
    marks_percentage: float = 75.0
    favorite_subjects: List[str] = []
    interests: List[str] = []
    skills: List[SkillItem] = []
    preferences: List[str] = []
    goals: List[str] = []
    constraints: List[str] = []
    programming_preference: str = "moderate"  # none | low | moderate | high
    mathematics_preference: str = "moderate"   # low | moderate | high
    creativity_level: str = "moderate"         # low | moderate | high
    people_interaction_preference: str = "balanced" # low | balanced | high

class ProfileUpdate(BaseModel):
    education_level: Optional[str] = None
    stream: Optional[str] = None
    subjects: Optional[List[str]] = None
    marks_percentage: Optional[float] = None
    favorite_subjects: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    skills: Optional[List[SkillItem]] = None
    preferences: Optional[List[str]] = None
    goals: Optional[List[str]] = None
    constraints: Optional[List[str]] = None
    programming_preference: Optional[str] = None
    mathematics_preference: Optional[str] = None
    creativity_level: Optional[str] = None
    people_interaction_preference: Optional[str] = None

class ProfileResponse(BaseModel):
    id: int
    user_id: int
    education_level: str
    stream: str
    subjects: List[str]
    marks_percentage: float
    favorite_subjects: List[str]
    interests: List[str]
    skills: List[Dict[str, Any]]
    preferences: List[str]
    goals: List[str]
    constraints: List[str]
    programming_preference: str
    mathematics_preference: str
    creativity_level: str
    people_interaction_preference: str
    profile_summary: Optional[str] = None
    academic_strengths: List[str] = []

    class Config:
        from_attributes = True

class ProfileAnalysisResponse(BaseModel):
    profile_summary: str
    academic_strengths: List[str]
    archetype: str
    suggested_domain_focus: List[str]
    potential_challenges: List[str]
