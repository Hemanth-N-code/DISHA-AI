# backend/app/models/roadmap.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class Roadmap(Base):
    __tablename__ = "roadmaps"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    career_id = Column(String(100), nullable=False)
    career_name = Column(String(255), nullable=False)
    target_horizon_months = Column(Integer, default=6)
    overall_progress = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="roadmaps")
    tasks = relationship("RoadmapTask", back_populates="roadmap", cascade="all, delete-orphan", order_by="RoadmapTask.stage_index")

class RoadmapTask(Base):
    __tablename__ = "roadmap_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    roadmap_id = Column(Integer, ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)  # Foundation | Core Skills | Projects | Portfolio | Internship
    stage_index = Column(Integer, default=0)
    estimated_weeks = Column(Integer, default=2)
    status = Column(String(50), default="not_started")  # not_started | in_progress | completed
    portfolio_artifact = Column(String(255), nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    roadmap = relationship("Roadmap", back_populates="tasks")
