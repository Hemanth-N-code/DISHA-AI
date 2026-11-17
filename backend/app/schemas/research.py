# backend/app/schemas/research.py
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class EventLogRequest(BaseModel):
    event_type: str  # career_viewed | career_saved | career_rejected | career_compared | what_if_used | alternative_explored | roadmap_created | roadmap_task_completed | confidence_rated
    session_id: Optional[str] = None
    event_data: Dict[str, Any] = {}

class ConfidenceRatingRequest(BaseModel):
    stage: str  # pre_exploration | post_exploration
    confidence_score: float  # 1.0 to 5.0
    feedback_notes: Optional[str] = None

class ResearchMetricsResponse(BaseModel):
    total_students: int
    total_explorations: int
    total_comparisons: int
    total_what_if_queries: int
    total_roadmaps_created: int
    average_career_diversity_index: float
    average_pre_confidence: float
    average_post_confidence: float
    confidence_delta: float
    domain_coverage_distribution: Dict[str, int]
    top_counterfactual_shifts: List[Dict[str, Any]]
    recent_events_sample: List[Dict[str, Any]]
