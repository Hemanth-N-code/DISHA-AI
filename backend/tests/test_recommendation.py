# backend/tests/test_recommendation.py
from app.recommendation.engine import calculate_career_score
from app.recommendation.diversity import select_diversity_aware_candidates, calculate_cdi
from app.schemas.profile import ProfileCreate, SkillItem

class MockCareer:
    def __init__(self, cid, name, domain, req_skills, elig="12th with PCM"):
        self.career_id = cid
        self.career_name = name
        self.domain = domain
        self.description = f"Core occupation in {domain}"
        self.typical_work = "Executes core daily tasks"
        self.required_skills = req_skills
        self.eligibility = elig
        self.education_paths = ["Degree in field"]
        self.higher_study_options = ["Master's"]
        self.entry_level_roles = ["Junior Specialist"]

def test_deterministic_scoring():
    profile = ProfileCreate(
        stream="Science (PCM)",
        interests=["technology", "design"],
        skills=[SkillItem(skill="Python", level=2), SkillItem(skill="Figma", level=4)],
        programming_preference="low",
        creativity_level="high",
        goals=["creative career"]
    )
    
    ux_career = MockCareer(
        cid="ux_designer",
        name="UX Designer",
        domain="Design",
        req_skills=[{"skill": "Figma", "level": 4}, {"skill": "User Research", "level": 4}]
    )
    
    swe_career = MockCareer(
        cid="software_engineer",
        name="Software Engineer",
        domain="Engineering & Technology",
        req_skills=[{"skill": "Python", "level": 4}, {"skill": "Data Structures", "level": 4}]
    )
    
    score_ux = calculate_career_score(profile, ux_career)
    score_swe = calculate_career_score(profile, swe_career)
    
    # Because user dislikes heavy coding and loves design, UX score should exceed or compare favorably to SWE
    assert score_ux.overall_score > 60.0
    assert any("design" in t.text.lower() for t in score_ux.factor_tags)
    assert any("programming" in t.text.lower() for t in score_swe.factor_tags)

def test_diversity_aware_cdi():
    profile = ProfileCreate(
        stream="Science (PCM)",
        interests=["technology", "design", "data"],
        skills=[SkillItem(skill="Python", level=3)],
        programming_preference="moderate"
    )
    
    careers_pool = [
        MockCareer("swe_1", "Software Engineer", "Engineering & Technology", [{"skill": "Python", "level": 4}]),
        MockCareer("swe_2", "DevOps Engineer", "Engineering & Technology", [{"skill": "Linux", "level": 4}]),
        MockCareer("swe_3", "Cloud Architect", "Engineering & Technology", [{"skill": "Cloud", "level": 4}]),
        MockCareer("swe_4", "Site Reliability Engineer", "Engineering & Technology", [{"skill": "Go", "level": 4}]),
        MockCareer("ds_1", "Data Scientist", "AI & Data", [{"skill": "Python", "level": 4}]),
        MockCareer("ux_1", "UX Designer", "Design", [{"skill": "Figma", "level": 4}]),
        MockCareer("env_1", "Environmental Scientist", "Environment", [{"skill": "EIA", "level": 4}]),
        MockCareer("fin_1", "Financial Analyst", "Business & Finance", [{"skill": "Excel", "level": 4}])
    ]
    
    baseline_cand, cdi_base, _ = select_diversity_aware_candidates(careers_pool, profile, limit=4, diversity_enabled=False)
    disha_cand, cdi_disha, _ = select_diversity_aware_candidates(careers_pool, profile, limit=4, diversity_enabled=True)
    
    # DISHA diversity-aware candidate selection should have higher or equal CDI than pure top-K baseline
    assert cdi_disha >= cdi_base
    domains_disha = set(c.domain for c in disha_cand)
    assert len(domains_disha) >= 2
