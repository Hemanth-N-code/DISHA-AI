# backend/app/agents/roadmap_agent.py
from typing import List, Dict, Any
from app.recommendation.skill_gap import analyze_skill_gap

class RoadmapAgent:
    """
    AGENT 4: Roadmap Agent
    Converts career interest and diagnosed skill gaps into an actionable, editable,
    portfolio-centric milestone DAG across 5 progressive stages:
    1. Foundation
    2. Core Skills
    3. Practical Projects
    4. Portfolio Showcase
    5. Internship & Industry Readiness
    """
    def generate_roadmap(
        self,
        profile: Any,
        career: Any,
        horizon_months: int = 6
    ) -> List[Dict[str, Any]]:
        gap_data = analyze_skill_gap(profile, career)
        tasks: List[Dict[str, Any]] = []
        
        # Stage 1: Education & Foundation (Month 1)
        tasks.append({
            "stage_index": 0,
            "category": "Foundation",
            "title": f"Academic Alignment & Core Fundamentals in {career.domain}",
            "description": f"Master foundational principles relevant to {career.career_name}. Understand fundamental theories, terminology, and tools.",
            "estimated_weeks": 3,
            "portfolio_artifact": "Curated study notes repository and conceptual synthesis document"
        })
        
        # Stage 2: Core Priority Skills (Month 2-3)
        priority_skills = [item.skill_name for item in gap_data.skills_breakdown if item.gap > 0][:3]
        if not priority_skills:
            priority_skills = [s.get("skill", "") for s in (career.required_skills or [])][:2]
            
        for idx, skill in enumerate(priority_skills, start=1):
            tasks.append({
                "stage_index": idx,
                "category": "Core Skills",
                "title": f"Skill Mastery: {skill}",
                "description": f"Targeted deep-dive into {skill} to bridge diagnosed gap. Complete structured hands-on modules.",
                "estimated_weeks": 3,
                "portfolio_artifact": f"Verified code/design exercise repository for {skill}"
            })
            
        # Stage 3: Real-World Applied Projects (Month 4)
        sample_projs = career.projects or [f"Build a production-grade prototype for {career.career_name}"]
        tasks.append({
            "stage_index": len(tasks),
            "category": "Projects",
            "title": f"Capstone Project: {sample_projs[0]}",
            "description": f"Design, build, and deploy an end-to-end practical solution demonstrating real-world competence.",
            "estimated_weeks": 4,
            "portfolio_artifact": "Public GitHub/Behance project demo with architectural README"
        })
        
        # Stage 4: Portfolio & Review (Month 5)
        sample_port = career.portfolio_requirements or ["Comprehensive project case study"]
        tasks.append({
            "stage_index": len(tasks),
            "category": "Portfolio",
            "title": "Portfolio Showcase & Artifact Curation",
            "description": f"Compile project case studies into an interactive online portfolio: {sample_port[0]}.",
            "estimated_weeks": 2,
            "portfolio_artifact": "Hosted live portfolio link or public dossier"
        })
        
        # Stage 5: Internship & Career Readiness (Month 6)
        sample_intern = career.internship_options or ["Industry internship"]
        tasks.append({
            "stage_index": len(tasks),
            "category": "Internship",
            "title": "Internship Search & Technical Interview Preparation",
            "description": f"Target entry-level opportunities and internships ({sample_intern[0]}). Refine resume and practice mock interviews.",
            "estimated_weeks": 3,
            "portfolio_artifact": "Target application tracking sheet and tailored resume"
        })
        
        return tasks

roadmap_agent = RoadmapAgent()
