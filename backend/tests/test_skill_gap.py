# backend/tests/test_skill_gap.py
from app.recommendation.skill_gap import analyze_skill_gap
from app.schemas.profile import ProfileCreate, SkillItem
from tests.test_recommendation import MockCareer

def test_skill_gap_analysis():
    profile = ProfileCreate(
        stream="Science (PCM)",
        skills=[
            SkillItem(skill="Python", level=2),
            SkillItem(skill="Communication", level=4)
        ]
    )
    
    career = MockCareer(
        cid="software_engineer",
        name="Software Engineer",
        domain="Engineering & Technology",
        req_skills=[
            {"skill": "Python", "level": 4, "importance": "Critical"},
            {"skill": "Communication", "level": 3, "importance": "High"},
            {"skill": "System Design", "level": 3, "importance": "High"}
        ]
    )
    
    res = analyze_skill_gap(profile, career)
    assert res.career_id == "software_engineer"
    assert res.total_skills_evaluated == 3
    
    # Python gap = 4 - 2 = 2
    py_gap = next((s for s in res.skills_breakdown if "python" in s.skill_name.lower()), None)
    assert py_gap is not None
    assert py_gap.gap == 2
    assert py_gap.category == "partially_developed"
    
    # Communication gap = max(0, 3 - 4) = 0
    comm_gap = next((s for s in res.skills_breakdown if "communication" in s.skill_name.lower()), None)
    assert comm_gap is not None
    assert comm_gap.gap == 0
    assert comm_gap.category == "existing"
    
    # System Design gap = 3 - 0 = 3 (missing)
    sys_gap = next((s for s in res.skills_breakdown if "system" in s.skill_name.lower()), None)
    assert sys_gap is not None
    assert sys_gap.gap == 3
    assert sys_gap.category == "missing"
