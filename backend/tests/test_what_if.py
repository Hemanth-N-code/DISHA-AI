# backend/tests/test_what_if.py
from app.recommendation.what_if import evaluate_what_if_scenario
from app.schemas.profile import ProfileCreate, SkillItem
from app.schemas.what_if import WhatIfRequest
from tests.test_recommendation import MockCareer

def test_what_if_perturbation():
    profile = ProfileCreate(
        stream="Science (PCM)",
        interests=["technology"],
        skills=[SkillItem(skill="Python", level=2)],
        programming_preference="high",
        creativity_level="low"
    )
    
    pool = [
        MockCareer("swe", "Software Engineer", "Engineering & Technology", [{"skill": "Python", "level": 4}]),
        MockCareer("ux", "UX Designer", "Design", [{"skill": "Figma", "level": 4}]),
        MockCareer("ds", "Data Scientist", "AI & Data", [{"skill": "Statistics", "level": 4}])
    ]
    
    # Counterfactual: Student changes mind to dislike programming and want creative design
    what_if = WhatIfRequest(
        programming_preference="none",
        creativity_level="high"
    )
    
    res = evaluate_what_if_scenario(profile, pool, what_if)
    assert res.scenario_description != ""
    assert len(res.deltas) > 0
    
    # SWE score should drop, UX score should rise
    swe_delta = next((d for d in res.deltas if d.career_id == "swe"), None)
    ux_delta = next((d for d in res.deltas if d.career_id == "ux"), None)
    
    if swe_delta:
        assert swe_delta.score_change < 0
    if ux_delta:
        assert ux_delta.score_change > 0
