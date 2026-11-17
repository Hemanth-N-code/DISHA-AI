# backend/app/models/cet.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(String, primary_key=True, index=True) # e.g. "kcet", "comedk", "jee_main"
    name = Column(String, nullable=False) # "Karnataka Common Entrance Test"
    authority = Column(String, nullable=False) # "KEA (Karnataka Examination Authority)"
    state = Column(String, nullable=False) # "Karnataka"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    domains = relationship("CetDomain", back_populates="exam", cascade="all, delete-orphan")
    cutoffs = relationship("HistoricalCutoff", back_populates="exam")

class CetDomain(Base):
    __tablename__ = "cet_domains"

    id = Column(String, primary_key=True, index=True) # e.g. "engineering", "b_pharma", "pharma_d", "agriculture"
    exam_id = Column(String, ForeignKey("exams.id"), nullable=False)
    name = Column(String, nullable=False) # "Engineering & Technology"
    course_group = Column(String, nullable=False) # "B.E. / B.Tech"
    is_active = Column(Boolean, default=True)

    exam = relationship("Exam", back_populates="domains")
    courses = relationship("Course", back_populates="domain")

class College(Base):
    __tablename__ = "colleges"

    id = Column(String, primary_key=True, index=True) # e.g. "rvce", "bmsce", "msrit"
    code = Column(String, index=True, nullable=False) # Official KEA code, e.g. "E001"
    name = Column(String, nullable=False)
    short_name = Column(String, nullable=False)
    location = Column(String, nullable=False) # e.g. "Mysuru Road, RV Vidyanikethan Post"
    city = Column(String, index=True, nullable=False) # e.g. "Bengaluru"
    district = Column(String, nullable=False) # e.g. "Bengaluru Urban"
    state = Column(String, default="Karnataka")
    college_type = Column(String, nullable=False) # "Autonomous - Private", "Government", "Aided"
    website = Column(String, nullable=True)
    established_year = Column(Integer, nullable=True)
    accreditation = Column(String, nullable=True) # e.g. "NAAC A++, NBA Accredited"
    campus_area_acres = Column(Float, nullable=True)
    hostel_facility = Column(Boolean, default=True)
    description = Column(Text, nullable=True)
    source = Column(String, default="Official KEA / College Brochure")
    source_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    branches = relationship("CollegeBranch", back_populates="college", cascade="all, delete-orphan")
    cutoffs = relationship("HistoricalCutoff", back_populates="college")
    placements = relationship("CollegePlacement", back_populates="college", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = "courses"

    id = Column(String, primary_key=True, index=True) # e.g. "b_tech_cse"
    domain_id = Column(String, ForeignKey("cet_domains.id"), nullable=False)
    code = Column(String, nullable=False) # "CS"
    name = Column(String, nullable=False) # "Computer Science and Engineering"
    duration_years = Column(Integer, default=4)
    degree_type = Column(String, default="Bachelor of Engineering (B.E.)")

    domain = relationship("CetDomain", back_populates="courses")
    branches = relationship("CollegeBranch", back_populates="course")

class CollegeBranch(Base):
    __tablename__ = "college_branches"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    college_id = Column(String, ForeignKey("colleges.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    branch_name = Column(String, nullable=False) # "Computer Science & Engineering"
    branch_code = Column(String, index=True, nullable=False) # "CS", "IS", "EC", "AI"
    intake = Column(Integer, default=120)
    tuition_fee_annual = Column(Float, nullable=True) # Official government/KEA quota fees
    is_active = Column(Boolean, default=True)

    college = relationship("College", back_populates="branches")
    course = relationship("Course", back_populates="branches")
    cutoffs = relationship("HistoricalCutoff", back_populates="college_branch")
    option_items = relationship("OptionEntryItem", back_populates="college_branch")

class HistoricalCutoff(Base):
    __tablename__ = "historical_cutoffs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exam_id = Column(String, ForeignKey("exams.id"), nullable=False)
    college_id = Column(String, ForeignKey("colleges.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    college_branch_id = Column(Integer, ForeignKey("college_branches.id"), nullable=True)
    branch_code = Column(String, index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False) # 2023, 2024, 2025
    round = Column(Integer, index=True, nullable=False) # 1, 2, 3
    category = Column(String, index=True, nullable=False) # "GM", "2A", "2B", "3A", "3B", "SCG", "STG", etc.
    quota = Column(String, default="General") # "General", "Hyderabad-Karnataka (371J)", "Rural", "Kannada Medium"
    gender = Column(String, default="All") # "All", "Female"
    opening_rank = Column(Integer, nullable=True)
    closing_rank = Column(Integer, nullable=False)
    source = Column(String, nullable=False) # "KEA Official Cutoff Report"
    source_url = Column(String, nullable=True)
    is_verified = Column(Boolean, default=True)
    data_quality = Column(String, default="Official Government Data")
    last_verified = Column(DateTime, default=datetime.utcnow)

    exam = relationship("Exam", back_populates="cutoffs")
    college = relationship("College", back_populates="cutoffs")
    college_branch = relationship("CollegeBranch", back_populates="cutoffs")

class CollegePlacement(Base):
    __tablename__ = "college_placements"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    college_id = Column(String, ForeignKey("colleges.id"), nullable=False)
    year = Column(Integer, nullable=False) # 2024, 2025
    placement_rate = Column(Float, nullable=True) # 92.4%
    median_package_lpa = Column(Float, nullable=True) # In Lakhs per annum, e.g. 10.5
    average_package_lpa = Column(Float, nullable=True) # e.g. 13.2
    highest_package_lpa = Column(Float, nullable=True) # e.g. 54.0
    total_offers = Column(Integer, nullable=True)
    top_recruiters = Column(JSON, default=list) # ["Amazon", "Microsoft", "Cisco", "Bosch"]
    source = Column(String, nullable=False) # "Official NIRF 2024 Report / College Placement Cell"
    source_url = Column(String, nullable=True)
    is_official = Column(Boolean, default=True)
    verified_date = Column(DateTime, default=datetime.utcnow)

    college = relationship("College", back_populates="placements")

class StudentCetProfile(Base):
    __tablename__ = "student_cet_profiles"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    exam_id = Column(String, ForeignKey("exams.id"), default="kcet")
    domain_id = Column(String, ForeignKey("cet_domains.id"), default="engineering")
    rank = Column(Integer, nullable=False)
    category = Column(String, default="GM") # "GM", "2A", "2B", "3A", "3B", "SCG", "STG"
    sub_category = Column(String, nullable=True) # "371J", "Rural", "Kannada Medium", "None"
    gender = Column(String, default="All")
    preferred_branches = Column(JSON, default=list) # ["CS", "IS", "EC", "AI"]
    preferred_locations = Column(JSON, default=list) # ["Bengaluru", "Mysuru"]
    preferences = Column(JSON, default=list) # ["placement", "low_fees", "campus", "research"]
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")
    option_list = relationship("OptionEntryList", back_populates="cet_profile", uselist=False, cascade="all, delete-orphan")

class OptionEntryList(Base):
    __tablename__ = "option_entry_lists"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    cet_profile_id = Column(Integer, ForeignKey("student_cet_profiles.id"), nullable=False)
    title = Column(String, default="My KCET Option Entry Plan")
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")
    cet_profile = relationship("StudentCetProfile", back_populates="option_list")
    items = relationship("OptionEntryItem", back_populates="option_list", cascade="all, delete-orphan", order_by="OptionEntryItem.priority_order")

class OptionEntryItem(Base):
    __tablename__ = "option_entry_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    option_list_id = Column(Integer, ForeignKey("option_entry_lists.id"), nullable=False)
    college_branch_id = Column(Integer, ForeignKey("college_branches.id"), nullable=False)
    priority_order = Column(Integer, nullable=False) # 1, 2, 3...
    historical_category = Column(String, default="Historically Compatible") # "Higher-competition", "Historically compatible", "Lower-cutoff / safer"
    student_notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    option_list = relationship("OptionEntryList", back_populates="items")
    college_branch = relationship("CollegeBranch", back_populates="option_items")

class CetResearchEvent(Base):
    __tablename__ = "cet_research_events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    event_type = Column(String, index=True, nullable=False) # "cet_search_started", "cutoff_viewed", "college_compared", "option_added", "option_reordered", "option_list_saved"
    event_data = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.utcnow)
