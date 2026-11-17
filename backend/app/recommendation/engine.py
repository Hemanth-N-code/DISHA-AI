# backend/app/recommendation/engine.py
from typing import Dict, Any, List, Tuple
from app.core.config import settings
from app.schemas.scoring import ScoreBreakdown, FactorTag

STREAM_DOMAIN_AFFINITIES = {
    "Science (PCM)": ["Engineering & Technology", "AI & Data", "Cybersecurity", "Emerging Careers", "Environment", "Business & Finance", "Skilled/Vocational", "Design"],
    "Science (PCB)": ["Healthcare", "Agriculture", "Environment", "Psychology", "Emerging Careers", "Education", "Design"],
    "Commerce": ["Business & Finance", "Law", "Hospitality & Tourism", "AI & Data", "Education", "Design"],
    "Arts/Humanities": ["Media & Film", "Design", "Psychology", "Fine Arts", "Law", "Education", "Hospitality & Tourism", "Fashion"],
    "Vocational / General": ["Skilled/Vocational", "Hospitality & Tourism", "Design", "Agriculture", "Fashion"]
}

INTEREST_DOMAIN_MAP = {
    "technology": ["Engineering & Technology", "AI & Data", "Cybersecurity", "Emerging Careers"],
    "ai/data": ["AI & Data", "Emerging Careers", "Engineering & Technology"],
    "design": ["Design", "Fine Arts", "Fashion", "Media & Film"],
    "business": ["Business & Finance", "Hospitality & Tourism", "Law"],
    "arts": ["Fine Arts", "Media & Film", "Fashion", "Design"],
    "psychology": ["Psychology", "Healthcare", "Education"],
    "healthcare": ["Healthcare", "Psychology"],
    "law": ["Law", "Business & Finance"],
    "media": ["Media & Film", "Design", "Education"],
    "research": ["AI & Data", "Environment", "Agriculture", "Education", "Healthcare"],
    "nature": ["Environment", "Agriculture"],
    "social": ["Psychology", "Education", "Healthcare", "Law"]
}

def calculate_career_score(profile: Any, career: Any) -> ScoreBreakdown:
    factor_tags: List[FactorTag] = []
    
    # 1. Interest Fit (0 - 100)
    user_interests = [str(i).lower().strip() for i in (profile.interests or [])]
    career_domain = str(career.domain).lower()
    career_desc = (str(career.description) + " " + str(career.career_name)).lower()
    
    interest_matches = 0
    total_interests = max(len(user_interests), 1)
    
    for interest in user_interests:
        matched = False
        for keyword, domains in INTEREST_DOMAIN_MAP.items():
            if keyword in interest:
                if any(d.lower() in career_domain for d in domains):
                    interest_matches += 1
                    matched = True
                    break
        if not matched and (interest in career_desc or interest in career_domain):
            interest_matches += 1
            matched = True
        
        if matched:
            factor_tags.append(FactorTag(positive=True, text=f"Strong interest alignment in {interest.capitalize()}"))
            
    interest_fit = min(100.0, (interest_matches / total_interests) * 100.0 if user_interests else 60.0)
    if interest_fit >= 50:
        interest_fit = min(100.0, interest_fit + 20)

    # 2. Academic Fit (0 - 100)
    user_stream = getattr(profile, "stream", "")
    eligible_domains = STREAM_DOMAIN_AFFINITIES.get(user_stream, [])
    
    academic_fit = 65.0
    elig_text = str(getattr(career, "eligibility", "")).lower()
    
    if any(d.lower() in career_domain for d in eligible_domains) or "pcm" in elig_text or "any" in elig_text:
        academic_fit = 85.0
        factor_tags.append(FactorTag(positive=True, text=f"High academic stream fit with {user_stream}"))
    else:
        academic_fit = 55.0
        factor_tags.append(FactorTag(positive=False, text=f"May require bridge coursework outside {user_stream}"))

    # Favorite subjects boost
    fav_subjects = [str(s).lower() for s in (profile.favorite_subjects or [])]
    for sub in fav_subjects:
        if sub in career_desc or sub in elig_text:
            academic_fit = min(100.0, academic_fit + 10)
            factor_tags.append(FactorTag(positive=True, text=f"Favorite subject {sub.capitalize()} directly utilized"))

    # 3. Skill Fit (0 - 100)
    user_skills_dict = {}
    for item in (profile.skills or []):
        if isinstance(item, dict):
            s_k = item.get("skill", "").lower().strip()
            s_v = float(item.get("level", 3))
            user_skills_dict[s_k] = s_v
        else:
            s_k = getattr(item, "skill", "").lower().strip()
            s_v = float(getattr(item, "level", 3))
            user_skills_dict[s_k] = s_v
    
    career_req_skills = career.required_skills or []
    skill_score_sum = 0.0
    evaluated_skills_count = max(len(career_req_skills), 1)
    
    for req in career_req_skills:
        req_name = req.get("skill", "").lower().strip()
        req_level = float(req.get("level", 3))
        
        matched_level = 0.0
        for user_sk, user_lvl in user_skills_dict.items():
            if user_sk in req_name or req_name in user_sk:
                matched_level = max(matched_level, user_lvl)
        
        if matched_level > 0:
            ratio = min(1.0, matched_level / req_level)
            skill_score_sum += ratio * 100.0
            if ratio >= 0.8:
                factor_tags.append(FactorTag(positive=True, text=f"Solid foundation in {req.get('skill')} ({int(matched_level)}/5)"))
        else:
            skill_score_sum += 40.0
            
    skill_fit = min(100.0, skill_score_sum / evaluated_skills_count)

    # 4. Preference Fit (0 - 100)
    preference_fit = 70.0
    prog_pref = str(getattr(profile, "programming_preference", "moderate")).lower()
    math_pref = str(getattr(profile, "mathematics_preference", "moderate")).lower()
    creat_pref = str(getattr(profile, "creativity_level", "moderate")).lower()
    people_pref = str(getattr(profile, "people_interaction_preference", "balanced")).lower()
    
    # Check Programming Intensity
    c_ident = (str(career.career_id) + " " + str(career.career_name)).lower()
    is_heavy_coding = any(k in c_ident for k in ["software", "swe", "devops", "embedded", "nlp", "ai_engineer", "mlops"])
    if is_heavy_coding:
        if prog_pref in ["none", "low"]:
            preference_fit -= 35.0
            factor_tags.append(FactorTag(positive=False, text="Requires high programming while your preference is low"))
        elif prog_pref == "high":
            preference_fit += 20.0
            factor_tags.append(FactorTag(positive=True, text="Matches strong preference for hands-on programming"))
    else:
        if prog_pref in ["none", "low"]:
            preference_fit += 15.0
            factor_tags.append(FactorTag(positive=True, text="Minimal coding intensity aligned with preference"))
            
    # Check Math Intensity
    is_heavy_math = any(k in c_ident for k in ["quant", "actuary", "data_scientist", "quantum", "aerospace"])
    if is_heavy_math:
        if math_pref == "low":
            preference_fit -= 30.0
            factor_tags.append(FactorTag(positive=False, text="Heavy quantitative focus while math comfort is modest"))
        elif math_pref == "high":
            preference_fit += 20.0
            factor_tags.append(FactorTag(positive=True, text="Leverages high quantitative mathematical willingness"))

    # Check Creativity
    is_creative = any(d.lower() in career_domain for d in ["design", "fine arts", "fashion", "media"])
    if is_creative and creat_pref == "high":
        preference_fit += 18.0
        factor_tags.append(FactorTag(positive=True, text="High artistic and creative expression alignment"))
        
    # Check People Interaction
    is_people_heavy = any(d.lower() in career_domain for d in ["psychology", "education", "hospitality", "law"]) or "ux_researcher" in c_ident
    if is_people_heavy and people_pref == "high":
        preference_fit += 15.0
        factor_tags.append(FactorTag(positive=True, text="High direct human interaction alignment"))

    preference_fit = max(15.0, min(100.0, preference_fit))

    # 5. Goal Fit (0 - 100)
    goal_fit = 75.0
    user_goals = [str(g).lower() for g in (profile.goals or [])]
    for goal in user_goals:
        if "higher studies" in goal and any(opt in str(career.higher_study_options).lower() for opt in ["m.", "ms", "ph.d"]):
            goal_fit += 10.0
            factor_tags.append(FactorTag(positive=True, text="Abundant higher study & research specialization pathways"))
            break
        if "creative" in goal and is_creative:
            goal_fit += 15.0
            factor_tags.append(FactorTag(positive=True, text="Direct vehicle for creative career ambition"))
            break
        if "job" in goal and career.entry_level_roles:
            goal_fit += 8.0
            factor_tags.append(FactorTag(positive=True, text="Strong immediate entry-level industry demand"))
            break
            
    goal_fit = min(100.0, goal_fit)

    # 5-Pillar Weighted Overall Score
    overall_score = (
        settings.WEIGHT_INTEREST * interest_fit +
        settings.WEIGHT_ACADEMIC * academic_fit +
        settings.WEIGHT_SKILL * skill_fit +
        settings.WEIGHT_PREFERENCE * preference_fit +
        settings.WEIGHT_GOAL * goal_fit
    )
    overall_score = round(max(15.0, min(98.5, overall_score)), 1)
    
    pos_tags = [t.text for t in factor_tags if t.positive][:3]
    neg_tags = [t.text for t in factor_tags if not t.positive][:2]
    
    explanation = f"Potential fit ({overall_score}% compatibility). "
    if pos_tags:
        explanation += "Key positive alignment: " + "; ".join(pos_tags) + ". "
    if neg_tags:
        explanation += "Points to consider: " + "; ".join(neg_tags) + "."
    else:
        explanation += "Strong continuous progression potential."

    return ScoreBreakdown(
        overall_score=overall_score,
        interest_fit=round(interest_fit, 1),
        academic_fit=round(academic_fit, 1),
        skill_fit=round(skill_fit, 1),
        preference_fit=round(preference_fit, 1),
        goal_fit=round(goal_fit, 1),
        factor_tags=factor_tags,
        explanation=explanation
    )
