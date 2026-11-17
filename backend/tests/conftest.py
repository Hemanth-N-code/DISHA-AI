# backend/tests/conftest.py
import pytest
import os
import sys
import json

os.environ["TESTING"] = "1"

# Ensure backend root is on sys.path for direct pytest invocation from any directory
_backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.database.session import Base, get_db
from app.models import User, Career, StudentProfile
from app.main import app, seed_database_if_empty, seed_cet_database_if_empty

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    Base.metadata.create_all(bind=engine)
    
    Session = sessionmaker(bind=engine)
    db = Session()
    seed_database_if_empty(db)
    seed_cet_database_if_empty(db, max_cutoffs=50)
    db.close()
    
    yield engine

@pytest.fixture(scope="function")
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture(scope="function")
def client(db_engine):
    Session = sessionmaker(bind=db_engine)

    def override_get_db():
        session = Session()
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def auth_headers(client):
    email = f"user_{os.urandom(4).hex()}@disha.edu"
    password = "TestPassword123!"
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Test Student"
    })
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create profile
    client.post("/api/v1/profile", json={
        "education_level": "12th_standard",
        "stream": "Science (PCM)",
        "marks_percentage": 88,
        "subjects": ["Physics", "Chemistry", "Mathematics"],
        "interests": ["UI/UX Design", "Technology"],
        "skills": [{"skill": "Wireframing", "level": 3}, {"skill": "Analytical Reasoning", "level": 4}],
        "programming_preference": "low",
        "mathematics_preference": "moderate",
        "creativity_level": "high",
        "people_interaction_preference": "balanced"
    }, headers=headers)
    
    return headers
