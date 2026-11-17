# backend/app/main.py
import json
import os
import logging
from typing import Optional
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.session import Base, engine, SessionLocal
from app.models import User, StudentProfile, Career, Roadmap, RoadmapTask, StudentMemory, ResearchEvent
from app.rag.career_rag import index_careers_for_rag

# Import API routers
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router
from app.api.careers import router as careers_router
from app.api.what_if import router as what_if_router
from app.api.skill_gap import router as skill_gap_router
from app.api.roadmap import router as roadmap_router
from app.api.memory import router as memory_router
from app.api.chat import router as chat_router
from app.api.research import router as research_router
from app.api.cet import router as cet_router
from app.models.cet import Exam, CetDomain, College, Course, CollegeBranch, HistoricalCutoff, CollegePlacement, OptionEntryItem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("disha_backend")

def seed_database_if_empty(db: Session):
    career_count = db.query(Career).count()
    if career_count > 0:
        logger.info(f"Database already contains {career_count} careers. Skipping initial seed.")
        return

    # Check for careers JSON
    json_paths = [
        "data/careers/careers.json",
        "../data/careers/careers.json",
        os.path.join(os.path.dirname(__file__), "../../../data/careers/careers.json")
    ]
    data_file = None
    for p in json_paths:
        if os.path.exists(p):
            data_file = p
            break

    if not data_file:
        logger.warning("No careers.json file found for initial seeding.")
        return

    logger.info(f"Seeding Career Knowledge Base from {data_file}...")
    with open(data_file, "r", encoding="utf-8") as f:
        careers_data = json.load(f)

    for item in careers_data:
        career = Career(
            career_id=item["career_id"],
            career_name=item["career_name"],
            domain=item["domain"],
            description=item["description"],
            typical_work=item["typical_work"],
            education_paths=item.get("education_paths", []),
            eligibility=item.get("eligibility", "12th / Intermediate"),
            required_skills=item.get("required_skills", []),
            soft_skills=item.get("soft_skills", []),
            related_careers=item.get("related_careers", []),
            alternative_careers=item.get("alternative_careers", []),
            adjacent_careers=item.get("adjacent_careers", []),
            entry_level_roles=item.get("entry_level_roles", []),
            higher_study_options=item.get("higher_study_options", []),
            certifications=item.get("certifications", []),
            projects=item.get("projects", []),
            portfolio_requirements=item.get("portfolio_requirements", []),
            internship_options=item.get("internship_options", []),
            future_skills=item.get("future_skills", []),
            technology_changes=item.get("technology_changes", ""),
            ai_impact=item.get("ai_impact", {}),
            pathway=item.get("pathway", ""),
            sources=item.get("sources", [])
        )
        db.add(career)

    db.commit()
    logger.info(f"Successfully seeded {len(careers_data)} careers into database.")

def seed_cet_database_if_empty(db: Session, max_cutoffs: Optional[int] = None):
    college_count = db.query(College).count()
    has_dsu = db.query(College).filter(College.id == "dsu").first() is not None
    if college_count >= 59 and has_dsu:
        logger.info(f"CET Database already fully populated with {college_count} colleges (including DSU). Skipping seed.")
        return

    json_paths = [
        "data/cet/kcet_seed_data.json",
        "../data/cet/kcet_seed_data.json",
        os.path.join(os.path.dirname(__file__), "../../../data/cet/kcet_seed_data.json")
    ]
    data_file = None
    for p in json_paths:
        if os.path.exists(p):
            data_file = p
            break

    if not data_file:
        logger.warning("No kcet_seed_data.json file found for initial CET seeding.")
        return

    logger.info(f"Expanding/Upgrading CET Knowledge Base to 55+ colleges from {data_file}...")
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Clean existing CET tables if upgrading from smaller dataset
    if college_count > 0:
        logger.info("Upgrading previous smaller CET dataset to full 55+ colleges knowledge base...")
        db.query(OptionEntryItem).delete()
        db.query(HistoricalCutoff).delete()
        db.query(CollegePlacement).delete()
        db.query(CollegeBranch).delete()
        db.query(College).delete()
        db.query(Course).delete()
        db.query(CetDomain).delete()
        db.query(Exam).delete()
        db.commit()

    # 1. Exams
    for ex in data.get("exams", []):
        db.add(Exam(**ex))

    # 2. Domains
    for d in data.get("domains", []):
        db.add(CetDomain(**d))

    # 3. Courses
    for c in data.get("courses", []):
        db.add(Course(**c))

    # 4. Colleges & Placements
    for col in data.get("colleges", []):
        placement_info = col.pop("placement", None)
        college_obj = College(**col)
        db.add(college_obj)
        if placement_info:
            db.add(CollegePlacement(college_id=col["id"], **placement_info))

    # 5. Branches
    for b in data.get("branches", []):
        db.add(CollegeBranch(**b))

    db.commit()

    # 6. Historical Cutoffs
    cutoffs = data.get("historical_cutoffs", [])
    if max_cutoffs:
        cutoffs = cutoffs[:max_cutoffs]
    chunk_size = 500
    for i in range(0, len(cutoffs), chunk_size):
        chunk = cutoffs[i:i + chunk_size]
        for c_item in chunk:
            db.add(HistoricalCutoff(**c_item))
        db.commit()

    logger.info(f"Successfully seeded CET database: {len(data.get('colleges', []))} colleges, {len(data.get('branches', []))} branches, {len(cutoffs)} cutoffs.")

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.getenv("TESTING"):
        logger.info("Initializing database schema...")
        Base.metadata.create_all(bind=engine)
        
        db = SessionLocal()
        try:
            seed_database_if_empty(db)
            seed_cet_database_if_empty(db)
            all_careers = db.query(Career).all()
            logger.info(f"Indexing {len(all_careers)} careers for RAG vector search...")
            index_careers_for_rag(all_careers)
        finally:
            db.close()
        
    yield
    logger.info("DISHA AI backend shutting down.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="DISHA AI: An Agentic AI Framework for Career Decision Exploration and Personalized Guidance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers under /api/v1
app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(profile_router, prefix=settings.API_V1_STR)
app.include_router(careers_router, prefix=settings.API_V1_STR)
app.include_router(what_if_router, prefix=settings.API_V1_STR)
app.include_router(skill_gap_router, prefix=settings.API_V1_STR)
app.include_router(roadmap_router, prefix=settings.API_V1_STR)
app.include_router(memory_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(research_router, prefix=settings.API_V1_STR)
app.include_router(cet_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "disha-backend"}

# Mount frontend/dist for seamless single-port full-stack deployment
frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist"))
if not os.path.exists(frontend_dist):
    frontend_dist = os.path.abspath(os.path.join(os.path.dirname(__file__), "dist"))

if os.path.exists(frontend_dist):
    assets_dir = os.path.join(frontend_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path in ("docs", "redoc", "openapi.json"):
            return None
        target_file = os.path.join(frontend_dist, full_path)
        if full_path and os.path.isfile(target_file):
            return FileResponse(target_file)
        return FileResponse(os.path.join(frontend_dist, "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "project": "DISHA AI",
            "tagline": "Discover Your Direction. Shape Your Future.",
            "status": "online",
            "docs_url": "/docs"
        }
