# backend/app/schemas/__init__.py
from app.schemas.auth import UserRegister, UserLogin, Token, UserResponse
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse, ProfileAnalysisResponse, SkillItem
from app.schemas.career import CareerBase, CareerCandidate, CareerDetail, CareerDiscoverRequest, CareerDiscoverResponse
from app.schemas.scoring import ScoreBreakdown, FactorTag
from app.schemas.what_if import WhatIfRequest, WhatIfResponse, ScenarioDelta
from app.schemas.comparison import CompareRequest, CompareResponse, CareerComparisonItem
from app.schemas.skill_gap import SkillGapItem, SkillGapResponse
from app.schemas.roadmap import RoadmapCreateRequest, RoadmapTaskUpdate, RoadmapResponse, RoadmapTaskSchema
from app.schemas.memory import MemoryEntryCreate, MemoryItem, JourneyResponse, JourneyTimelineEvent
from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse
from app.schemas.research import EventLogRequest, ConfidenceRatingRequest, ResearchMetricsResponse

__all__ = [
    "UserRegister", "UserLogin", "Token", "UserResponse",
    "ProfileCreate", "ProfileUpdate", "ProfileResponse", "ProfileAnalysisResponse", "SkillItem",
    "CareerBase", "CareerCandidate", "CareerDetail", "CareerDiscoverRequest", "CareerDiscoverResponse",
    "ScoreBreakdown", "FactorTag",
    "WhatIfRequest", "WhatIfResponse", "ScenarioDelta",
    "CompareRequest", "CompareResponse", "CareerComparisonItem",
    "SkillGapItem", "SkillGapResponse",
    "RoadmapCreateRequest", "RoadmapTaskUpdate", "RoadmapResponse", "RoadmapTaskSchema",
    "MemoryEntryCreate", "MemoryItem", "JourneyResponse", "JourneyTimelineEvent",
    "ChatMessage", "ChatRequest", "ChatResponse",
    "EventLogRequest", "ConfidenceRatingRequest", "ResearchMetricsResponse"
]
