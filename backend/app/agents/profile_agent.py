# backend/app/agents/profile_agent.py
from typing import Dict, Any, List
from app.schemas.profile import ProfileCreate, ProfileAnalysisResponse
from app.services.llm_service import llm_service

class ProfileAgent:
    """
    AGENT 1: Profile Agent
    Converts raw onboarding answers into a structured multidimensional student profile.
    Analyzes academic strengths, latent affinities, and synthesizes a student archetype.
    """
    def process_profile(self, data: ProfileCreate) -> Dict[str, Any]:
        # 1. Identify Academic Strengths
        strengths = []
        if data.marks_percentage >= 85:
            strengths.append(f"High academic distinction ({data.marks_percentage}%)")
        elif data.marks_percentage >= 70:
            strengths.append(f"Solid academic foundation ({data.marks_percentage}%)")
            
        for fav in data.favorite_subjects:
            strengths.append(f"Pronounced affinity for {fav}")

        # 2. Determine Student Archetype & Focus
        archetype = "The Multidisciplinary Explorer"
        interests_lower = [i.lower() for i in data.interests]
        stream_lower = data.stream.lower()
        
        has_tech = any("tech" in i or "ai" in i for i in interests_lower)
        has_design = any("design" in i or "art" in i for i in interests_lower)
        has_social = any("psych" in i or "people" in i or "social" in i for i in interests_lower)
        has_quant = "math" in stream_lower or data.mathematics_preference == "high"
        
        if has_tech and has_design:
            archetype = "The Creative Technologist (Product & Design Engineering)"
            focus = ["Design", "Engineering & Technology", "Media & Film", "Emerging Careers"]
        elif has_tech and has_quant:
            archetype = "The Analytical Problem Solver (Data & Systems Architecture)"
            focus = ["AI & Data", "Engineering & Technology", "Cybersecurity", "Business & Finance"]
        elif has_design:
            archetype = "The Visual Storyteller & Experience Creator"
            focus = ["Design", "Fine Arts", "Fashion", "Media & Film"]
        elif has_social:
            archetype = "The Human-Centric Advocate & Educator"
            focus = ["Psychology", "Education", "Healthcare", "Law"]
        else:
            archetype = f"The {data.stream} Specialist"
            focus = ["Engineering & Technology", "Business & Finance", "Environment"]

        # 3. Formulate Archetype Summary
        summary = (
            f"Student profile calibrated as '{archetype}'. Shows {data.stream} background "
            f"with key interest in {', '.join(data.interests[:3]) if data.interests else 'exploring new fields'}. "
            f"Prefers {data.programming_preference} programming intensity and {data.creativity_level} creative engagement. "
            f"Goal orientation leans toward {', '.join(data.goals[:2]) if data.goals else 'career readiness'}."
        )

        challenges = []
        if data.programming_preference in ["none", "low"] and has_tech:
            challenges.append("Navigating technology fields while deliberately filtering out heavy low-level coding")
        if data.mathematics_preference == "low" and has_quant:
            challenges.append("Strengthening statistical confidence for data-intensive tracks")

        return {
            "profile_summary": summary,
            "academic_strengths": strengths,
            "archetype": archetype,
            "suggested_domain_focus": focus,
            "potential_challenges": challenges
        }

profile_agent = ProfileAgent()
