# backend/app/models/profile.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    # Academic Info
    education_level = Column(String(100), default="12th / Intermediate / PUC")
    stream = Column(String(100), nullable=False)
    subjects = Column(JSON, default=list)
    marks_percentage = Column(Float, default=75.0)
    favorite_subjects = Column(JSON, default=list)
    
    # Core Dimension Vectors
    interests = Column(JSON, default=list)
    skills = Column(JSON, default=list)  # list of {"skill": "name", "level": 1-5}
    preferences = Column(JSON, default=list)
    goals = Column(JSON, default=list)
    constraints = Column(JSON, default=list)
    
    # Specific Calibration Dimensions
    programming_preference = Column(String(50), default="moderate")  # none | low | moderate | high
    mathematics_preference = Column(String(50), default="moderate")   # low | moderate | high
    creativity_level = Column(String(50), default="moderate")         # low | moderate | high
    people_interaction_preference = Column(String(50), default="balanced") # low | balanced | high
    
    # AI-Synthesized Archetype Summary
    profile_summary = Column(Text, nullable=True)
    academic_strengths = Column(JSON, default=list)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="profile")
