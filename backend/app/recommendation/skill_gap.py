# backend/app/recommendation/skill_gap.py
from typing import List, Dict, Any
from app.schemas.skill_gap import SkillGapItem, SkillGapResponse

def analyze_skill_gap(profile: Any, career: Any) -> SkillGapResponse:
    user_skills = {}
    for item in (getattr(profile, "skills", []) or []):
        if isinstance(item, dict):
            s_name = item.get("skill", "").lower().strip()
            s_level = int(item.get("level", 3))
            user_skills[s_name] = s_level
        else:
            s_name = getattr(item, "skill", "").lower().strip()
            s_level = int(getattr(item, "level", 3))
            user_skills[s_name] = s_level

    required_skills = getattr(career, "required_skills", []) or []
    breakdown: List[SkillGapItem] = []
    
    total_skills = max(len(required_skills), 1)
    matched_count = 0
    gap_count = 0
    total_readiness_pts = 0
    max_readiness_pts = 0

    priority_focus = []

    for req in required_skills:
        req_name = req.get("skill", "Core Competency")
        req_clean = req_name.lower().strip()
        req_level = int(req.get("level", 3))
        importance = req.get("importance", "High")
        
        current_level = 0
        for u_skill, u_lvl in user_skills.items():
            if u_skill in req_clean or req_clean in u_skill:
                current_level = max(current_level, u_lvl)

        gap = max(0, req_level - current_level)
        max_readiness_pts += req_level
        total_readiness_pts += min(current_level, req_level)

        if current_level >= req_level:
            category = "existing"
            priority = "Low"
            action = f"Maintain and leverage proficiency in projects ({current_level}/5)"
            matched_count += 1
        elif current_level > 0:
            category = "partially_developed"
            if importance == "Critical" or gap >= 2:
                priority = "High"
                priority_focus.append(req_name)
            else:
                priority = "Medium"
            action = f"Elevate proficiency from level {current_level} to {req_level} via intermediate capstone projects"
            gap_count += 1
        else:
            category = "missing"
            if importance in ["Critical", "High"]:
                priority = "Critical"
                priority_focus.append(req_name)
            else:
                priority = "High"
            action = f"Initiate structured foundational coursework from zero to reach level {req_level}"
            gap_count += 1

        breakdown.append(SkillGapItem(
            skill_name=req_name,
            current_level=current_level,
            required_level=req_level,
            gap=gap,
            category=category,
            priority=priority,
            recommended_action=action
        ))

    priority_order = {"Critical": 0, "High": 1, "Medium": 2, "Low": 3}
    breakdown.sort(key=lambda x: priority_order.get(x.priority, 4))

    readiness_percentage = round((total_readiness_pts / float(max_readiness_pts)) * 100.0, 1) if max_readiness_pts > 0 else 50.0
    
    total_gap_points = sum(item.gap for item in breakdown)
    estimated_months = max(2, min(12, int(round(total_gap_points * 0.75))))

    return SkillGapResponse(
        career_id=career.career_id,
        career_name=career.career_name,
        total_skills_evaluated=len(required_skills),
        matched_skills_count=matched_count,
        gap_skills_count=gap_count,
        readiness_percentage=readiness_percentage,
        skills_breakdown=breakdown,
        top_priority_focus_areas=priority_focus[:4],
        estimated_upskilling_months=estimated_months
    )
