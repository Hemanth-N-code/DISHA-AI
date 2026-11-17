# backend/app/agents/analysis_agent.py
from typing import Dict, Any
from app.recommendation.engine import calculate_career_score
from app.recommendation.skill_gap import analyze_skill_gap

class CareerAnalysisAgent:
    """
    AGENT 3: Career Analysis Agent
    Performs multidimensional deep-dive analysis on a selected career.
    Maintains student agency using non-prescriptive supportive phrasing.
    """
    def analyze_career_path(
        self,
        profile: Any,
        career: Any,
        memory_context: str = ""
    ) -> Dict[str, Any]:
        score_breakdown = calculate_career_score(profile, career)
        gap_analysis = analyze_skill_gap(profile, career)

        # Build reflective questions the student should consider
        questions_to_consider = [
            f"How excited are you to engage with the daily tasks of {career.career_name} (e.g., {career.typical_work[:70]}...)?",
            f"Are you comfortable pursuing {career.education_paths[0] if career.education_paths else 'specialized coursework'}?",
            f"Given your current skills, are you willing to invest {gap_analysis.estimated_upskilling_months} months to master {', '.join(gap_analysis.top_priority_focus_areas[:2]) if gap_analysis.top_priority_focus_areas else 'key technical tools'}?"
        ]

        fit_summary = (
            f"Potential fit because of your {profile.stream} background, "
            f"compatibility with {career.domain}, and alignment with your preference for "
            f"{profile.programming_preference} programming intensity. "
            f"DISHA views this pathway not as an irrevocable conclusion, but as a rich starting point for exploration."
        )

        return {
            "career_id": career.career_id,
            "career_name": career.career_name,
            "domain": career.domain,
            "fit_summary": fit_summary,
            "score_breakdown": score_breakdown,
            "academic_requirements": career.eligibility,
            "education_paths": career.education_paths,
            "skill_gap_analysis": gap_analysis,
            "alternative_careers": career.alternative_careers,
            "related_careers": career.related_careers,
            "pathway_milestones": career.pathway,
            "technology_transformation": {
                "changes": career.technology_changes,
                "ai_impact": career.ai_impact,
                "future_resilient_skills": career.future_skills
            },
            "questions_to_consider": questions_to_consider,
            "sources": career.sources
        }

analysis_agent = CareerAnalysisAgent()
