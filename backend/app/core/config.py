# backend/app/core/config.py
import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings

# Proactively load .env from backend/ or project root
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_dotenv_backend = _BACKEND_DIR / ".env"
_dotenv_root = _BACKEND_DIR.parent / ".env"

if _dotenv_backend.exists():
    load_dotenv(_dotenv_backend)
if _dotenv_root.exists():
    load_dotenv(_dotenv_root)
load_dotenv()

# Canonical absolute SQLite path to backend/disha.db
_canonical_db_path = (_BACKEND_DIR / "disha.db").resolve().as_posix()
_default_sqlite_url = f"sqlite:///{_canonical_db_path}"

class Settings(BaseSettings):
    PROJECT_NAME: str = "DISHA AI"
    API_V1_STR: str = "/api/v1"
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "disha-ai-secret-key-super-secure-change-in-production-2026")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database (always points to canonical backend/disha.db)
    DATABASE_URL: str = _default_sqlite_url
    USE_SQLITE_FALLBACK: bool = True

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def resolve_canonical_db_path(cls, v: str) -> str:
        if v.startswith("sqlite") and "disha.db" in v:
            return _default_sqlite_url
        return v
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://localhost:8000"
    ]
    
    # Recommendation 5-Pillar Configurable Weights
    WEIGHT_INTEREST: float = 0.25
    WEIGHT_ACADEMIC: float = 0.25
    WEIGHT_SKILL: float = 0.20
    WEIGHT_PREFERENCE: float = 0.15
    WEIGHT_GOAL: float = 0.15
    
    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "gemini")  # mock | openai | gemini | anthropic
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    class Config:
        env_file = [str(_dotenv_backend), str(_dotenv_root), ".env"]
        extra = "allow"

settings = Settings()
