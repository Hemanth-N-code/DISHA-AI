# backend/app/models/career.py
from sqlalchemy import Column, Integer, String, Text, JSON
from app.database.session import Base

class Career(Base):
    __tablename__ = "careers"
    
    id = Column(Integer, primary_key=True, index=True)
    career_id = Column(String(100), unique=True, index=True, nullable=False)
    career_name = Column(String(255), nullable=False)
    domain = Column(String(100), index=True, nullable=False)
    
    description = Column(Text, nullable=False)
    typical_work = Column(Text, nullable=False)
    education_paths = Column(JSON, default=list)
    eligibility = Column(String(255), nullable=False)
    
    required_skills = Column(JSON, default=list)  # [{"skill": "Python", "level": 4, "importance": "Critical"}]
    soft_skills = Column(JSON, default=list)
    
    related_careers = Column(JSON, default=list)
    alternative_careers = Column(JSON, default=list)
    adjacent_careers = Column(JSON, default=list)
    
    entry_level_roles = Column(JSON, default=list)
    higher_study_options = Column(JSON, default=list)
    certifications = Column(JSON, default=list)
    projects = Column(JSON, default=list)
    portfolio_requirements = Column(JSON, default=list)
    internship_options = Column(JSON, default=list)
    
    future_skills = Column(JSON, default=list)
    technology_changes = Column(Text, nullable=True)
    ai_impact = Column(JSON, default=dict)  # {"automated_tasks": [], "augmented_tasks": [], "human_skills": []}
    pathway = Column(Text, nullable=True)
    sources = Column(JSON, default=list)
