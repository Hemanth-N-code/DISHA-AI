# backend/app/schemas/memory.py
from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

class MemoryEntryCreate(BaseModel):
    memory_type: str  # preference | explored_career | saved_career | rejected_career | what_if_scenario | insight
    key: str
    value_json: Dict[str, Any] = {}

class MemoryItem(BaseModel):
    id: int
    memory_type: str
    key: str
    value_json: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class JourneyTimelineEvent(BaseModel):
    timestamp: datetime
    event_type: str
    title: str
    description: str
    metadata: Dict[str, Any] = {}

class JourneyResponse(BaseModel):
    total_careers_explored: int
    saved_careers: List[str]
    rejected_careers_with_reasons: List[Dict[str, Any]]
    active_what_if_scenarios: List[Dict[str, Any]]
    learned_preferences: Dict[str, Any]
    timeline: List[JourneyTimelineEvent]
