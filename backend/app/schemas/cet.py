# backend/app/schemas/cet.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
from datetime import datetime

class ExamResponse(BaseModel):
    id: str
    name: str
    authority: str
    state: str
    is_active: bool

    class Config:
        from_attributes = True

class CetDomainResponse(BaseModel):
    id: str
    exam_id: str
    name: str
    course_group: str
    is_active: bool

    class Config:
        from_attributes = True

class CollegePlacementSchema(BaseModel):
    year: int
    placement_rate: Optional[float] = None
    median_package_lpa: Optional[float] = None
    average_package_lpa: Optional[float] = None
    highest_package_lpa: Optional[float] = None
    top_recruiters: List[str] = []
    source: str
    is_official: bool

    class Config:
        from_attributes = True

class CollegeBranchItem(BaseModel):
    id: int
    course_id: str
    branch_name: str
    branch_code: str
    intake: int
    tuition_fee_annual: Optional[float] = None

    class Config:
        from_attributes = True

class CollegeDetailResponse(BaseModel):
    id: str
    code: str
    name: str
    short_name: str
    location: str
    city: str
    district: str
    college_type: str
    website: Optional[str] = None
    established_year: Optional[int] = None
    accreditation: Optional[str] = None
    campus_area_acres: Optional[float] = None
    hostel_facility: bool = True
    description: Optional[str] = None
    source: str
    source_url: Optional[str] = None
    branches: List[CollegeBranchItem] = []
    placement: Optional[CollegePlacementSchema] = None

    class Config:
        from_attributes = True

class StudentCetProfileCreate(BaseModel):
    exam_id: str = "kcet"
    domain_id: str = "engineering"
    rank: int = Field(..., ge=1, le=500000)
    category: str = "GM"
    sub_category: Optional[str] = None
    gender: str = "All"
    preferred_branches: List[str] = []
    preferred_locations: List[str] = []
    preferences: List[str] = []

class StudentCetProfileResponse(BaseModel):
    id: int
    user_id: int
    exam_id: str
    domain_id: str
    rank: int
    category: str
    sub_category: Optional[str] = None
    gender: str
    preferred_branches: List[str]
    preferred_locations: List[str]
    preferences: List[str]
    updated_at: datetime

    class Config:
        from_attributes = True

class CetAnalyzeRequest(BaseModel):
    rank: int = Field(..., ge=1, le=500000)
    category: str = "GM"
    domain_id: str = "engineering"
    preferred_branches: Optional[List[str]] = None
    preferred_locations: Optional[List[str]] = None
    preferences: Optional[List[str]] = None
    round_num: int = 1
    sort_by: Optional[str] = "match_score"

class CetOptionMatchItem(BaseModel):
    college_id: str
    college_code: str
    college_name: str
    college_short_name: str
    city: str
    college_type: str
    branch_id: int
    branch_name: str
    branch_code: str
    tuition_fee_annual: Optional[float] = None
    historical_match_label: str
    match_badge_color: str
    historical_explanation: str
    match_score: float
    closing_ranks: Dict[int, int]
    most_recent_closing_rank: Optional[int] = None
    placement: Optional[Dict[str, Any]] = None
    source: str
    source_url: Optional[str] = None

class CetAnalyzeResponse(BaseModel):
    student_rank: int
    category: str
    round_num: int
    total_options_evaluated: int
    strong_matches_count: int
    possible_matches_count: int
    safer_matches_count: int
    competitive_matches_count: int
    options: List[CetOptionMatchItem]
    disclaimer: str

class CutoffTrendResponse(BaseModel):
    college_id: str
    branch_code: str
    category: str
    round: int
    trend_points: List[Dict[str, Any]]
    direction: str
    available_years: List[int]

class CollegeCompareRequest(BaseModel):
    college_ids: List[str]
    branch_code: str = "CS"
    category: str = "GM"

class OptionItemCreate(BaseModel):
    college_branch_id: int
    historical_category: str = "Historically Compatible"
    student_notes: Optional[str] = None

class OptionItemResponse(BaseModel):
    id: int
    option_list_id: int
    college_branch_id: int
    priority_order: int
    historical_category: str
    student_notes: Optional[str] = None
    college_name: str
    college_short_name: str
    branch_name: str
    branch_code: str
    city: str

    class Config:
        from_attributes = True

class OptionListResponse(BaseModel):
    id: int
    user_id: int
    title: str
    notes: Optional[str] = None
    items: List[OptionItemResponse]
    disclaimer: str

class OptionListReorderRequest(BaseModel):
    ordered_item_ids: List[int]
