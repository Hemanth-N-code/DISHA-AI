# backend/app/recommendation/what_if.py
from copy import deepcopy
from typing import List, Any
from app.schemas.what_if import WhatIfRequest, WhatIfResponse, ScenarioDelta
from app.recommendation.diversity import select_diversity_aware_candidates
from app.recommendation.engine import calculate_career_score

class VirtualProfile:
    """A transient representation of StudentProfile for counterfactual analysis."""
    def __init__(self, base_profile: Any):
        self.stream = getattr(base_profile, "stream", "Science (PCM)")
        self.interests = list(getattr(base_profile, "interests", []) or [])
        self.skills = deepcopy(getattr(base_profile, "skills", []) or [])
        self.preferences = list(getattr(base_profile, "preferences", []) or [])
        self.goals = list(getattr(base_profile, "goals", []) or [])
        self.constraints = list(getattr(base_profile, "constraints", []) or [])
        self.programming_preference = getattr(base_profile, "programming_preference", "moderate")
        self.mathematics_preference = getattr(base_profile, "mathematics_preference", "moderate")
        self.creativity_level = getattr(base_profile, "creativity_level", "moderate")
        self.people_interaction_preference = getattr(base_profile, "people_interaction_preference", "balanced")
        self.favorite_subjects = list(getattr(base_profile, "favorite_subjects", []) or [])

def evaluate_what_if_scenario(
    base_profile: Any,
    all_careers: List[Any],
    what_if: WhatIfRequest
) -> WhatIfResponse:
    """
    Simulates counterfactual parameter shifts without mutating database state.
    Calculates Current Top Careers vs What-If Top Careers and derives deltas.
    """
    # 1. Evaluate current baseline
    current_candidates, cdi_current, _ = select_diversity_aware_candidates(all_careers, base_profile, limit=8)
    current_map = {c.career_id: c.score_breakdown.overall_score for c in current_candidates}
    
    # 2. Construct perturbed virtual profile
    virtual_profile = VirtualProfile(base_profile)
    changes_desc = []
    
    if what_if.programming_preference is not None:
        virtual_profile.programming_preference = what_if.programming_preference
        changes_desc.append(f"Programming intensity set to '{what_if.programming_preference}'")
        
    if what_if.mathematics_preference is not None:
        virtual_profile.mathematics_preference = what_if.mathematics_preference
        changes_desc.append(f"Mathematics willingness set to '{what_if.mathematics_preference}'")
        
    if what_if.creativity_level is not None:
        virtual_profile.creativity_level = what_if.creativity_level
        changes_desc.append(f"Creative focus calibrated to '{what_if.creativity_level}'")
        
    if what_if.people_interaction_preference is not None:
        virtual_profile.people_interaction_preference = what_if.people_interaction_preference
        changes_desc.append(f"Interpersonal interaction set to '{what_if.people_interaction_preference}'")
        
    if what_if.added_interests:
        for item in what_if.added_interests:
            if item not in virtual_profile.interests:
                virtual_profile.interests.append(item)
        changes_desc.append(f"Added interests: {', '.join(what_if.added_interests)}")
        
    if what_if.removed_interests:
        virtual_profile.interests = [i for i in virtual_profile.interests if i not in what_if.removed_interests]
        changes_desc.append(f"Excluded interests: {', '.join(what_if.removed_interests)}")

    scenario_description = "; ".join(changes_desc) if changes_desc else "Custom preference exploration"

    # 3. Evaluate What-If scenario
    what_if_candidates, cdi_what_if, _ = select_diversity_aware_candidates(all_careers, virtual_profile, limit=8)
    
    # 4. Compute Deltas & Insights
    deltas: List[ScenarioDelta] = []
    
    # Evaluate score changes across surfaced careers
    eval_ids = set([c.career_id for c in what_if_candidates] + [c.career_id for c in current_candidates])
    career_by_id = {c.career_id: c for c in all_careers}
    
    for cid in eval_ids:
        c_obj = career_by_id.get(cid)
        if not c_obj:
            continue
            
        prev_score = current_map.get(cid)
        if prev_score is None:
            prev_score = calculate_career_score(base_profile, c_obj).overall_score
            
        new_score = calculate_career_score(virtual_profile, c_obj).overall_score
        diff = round(new_score - prev_score, 1)
        
        if diff >= 8.0:
            status = "surged"
            reason = f"Significantly favored by {scenario_description}"
        elif diff <= -8.0:
            status = "declined"
            reason = f"Penalized by constraint shift ({scenario_description})"
        elif cid not in current_map and new_score >= 65.0:
            status = "newly_unlocked"
            reason = "Emerged as an attractive alternative under new constraints"
        else:
            status = "stable"
            reason = "Maintains consistent compatibility across scenarios"
            
        deltas.append(ScenarioDelta(
            career_id=cid,
            career_name=c_obj.career_name,
            domain=c_obj.domain,
            previous_score=prev_score,
            new_score=new_score,
            score_change=diff,
            status=status,
            reason=reason
        ))
        
    # Sort deltas by magnitude of score change
    deltas.sort(key=lambda d: abs(d.score_change), reverse=True)
    
    # Generate human-readable explanation
    surged_names = [d.career_name for d in deltas if d.score_change > 5][:3]
    declined_names = [d.career_name for d in deltas if d.score_change < -5][:3]
    
    explanation_parts = []
    if surged_names:
        explanation_parts.append(f"Under this counterfactual scenario, options like {', '.join(surged_names)} gained prominence.")
    if declined_names:
        explanation_parts.append(f"Paths requiring heavy reliance on previous constraints ({', '.join(declined_names)}) shifted down.")
    explanation = " ".join(explanation_parts) or "The career landscape shifted modestly while maintaining foundational core fits."

    return WhatIfResponse(
        scenario_description=scenario_description,
        current_top_careers=current_candidates,
        what_if_top_careers=what_if_candidates,
        deltas=deltas[:8],
        explanation=explanation,
        diversity_index_current=cdi_current,
        diversity_index_what_if=cdi_what_if
    )
