# backend/app/models/research.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base

class ResearchEvent(Base):
    __tablename__ = "research_events"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    session_id = Column(String(100), index=True, nullable=True)
    event_type = Column(String(100), index=True, nullable=False)
    # career_viewed | career_saved | career_rejected | career_compared | what_if_used | alternative_explored | roadmap_created | roadmap_task_completed | confidence_rated
    
    event_data = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
    
    user = relationship("User", back_populates="research_events")

class ResearchMetricSnapshot(Base):
    __tablename__ = "research_metric_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    pre_decision_confidence = Column(Float, nullable=True)   # 1 to 5
    post_decision_confidence = Column(Float, nullable=True)  # 1 to 5
    career_diversity_index = Column(Float, default=0.0)      # CDI
    domains_explored_count = Column(Integer, default=0)
    unknown_careers_discovered_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
