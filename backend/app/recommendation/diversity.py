# backend/app/recommendation/diversity.py
import math
from typing import List, Dict, Any, Tuple
from app.schemas.career import CareerCandidate
from app.recommendation.engine import calculate_career_score

def calculate_cdi(candidates: List[CareerCandidate]) -> float:
    """
    Computes the Career Diversity Index (CDI):
    CDI = (Distinct Domains / Total Candidates) * Shannon Entropy of Domain Distribution
    """
    if not candidates:
        return 0.0
        
    domain_counts: Dict[str, int] = {}
    for c in candidates:
        domain_counts[c.domain] = domain_counts.get(c.domain, 0) + 1
        
    total = len(candidates)
    unique_domains = len(domain_counts)
    
    domain_ratio = unique_domains / float(total)
    
    # Shannon Entropy H(D)
    entropy = 0.0
    for count in domain_counts.values():
        p = count / float(total)
        if p > 0:
            entropy -= p * math.log2(p)
            
    # Max possible entropy for uniform distribution across unique domains
    max_entropy = math.log2(unique_domains) if unique_domains > 1 else 1.0
    normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0
    
    cdi = round(domain_ratio * (1.0 + normalized_entropy), 3)
    return cdi

def select_diversity_aware_candidates(
    all_careers: List[Any],
    profile: Any,
    limit: int = 15,
    diversity_enabled: bool = True
) -> Tuple[List[CareerCandidate], float, str]:
    """
    Selects candidate careers using either:
    1. Baseline Recommender (pure descending overall score, prone to single-domain popularity bias)
    2. DISHA Diversity-Aware Optimizer (guarantees cross-domain exposure of high-compatibility paths)
    """
    # 1. Score all careers deterministically
    scored_items: List[Tuple[Any, Any]] = []
    for career in all_careers:
        breakdown = calculate_career_score(profile, career)
        scored_items.append((career, breakdown))
        
    # Sort descending by overall score
    scored_items.sort(key=lambda x: x[1].overall_score, reverse=True)
    
    if not diversity_enabled:
        # BASELINE: Take top-N purely by score
        candidates = []
        for career, score in scored_items[:limit]:
            candidates.append(CareerCandidate(
                career_id=career.career_id,
                career_name=career.career_name,
                domain=career.domain,
                description=career.description,
                typical_work=career.typical_work,
                eligibility=career.eligibility,
                score_breakdown=score,
                is_diversity_highlight=False,
                diversity_domain=career.domain
            ))
        cdi = calculate_cdi(candidates)
        return candidates, cdi, "Baseline (Pure Top-K Similarity Ranking)"
        
    # DISHA DIVERSITY-AWARE DISCOVERY ALGORITHM:
    # 1. Take top 5 pure highest scores regardless of domain (Anchor high relevance)
    # 2. To prevent domain saturation, cap max representation per domain (e.g. max 2 per domain)
    # 3. Deliberately surface best candidate from distinct high-potential adjacent domains
    selected: List[CareerCandidate] = []
    domain_tally: Dict[str, int] = {}
    MAX_PER_DOMAIN = 2
    
    # First pass: Pick up to 5 top anchors
    for career, score in scored_items:
        d = career.domain
        if len(selected) < 5 and domain_tally.get(d, 0) < MAX_PER_DOMAIN:
            domain_tally[d] = domain_tally.get(d, 0) + 1
            selected.append(CareerCandidate(
                career_id=career.career_id,
                career_name=career.career_name,
                domain=career.domain,
                description=career.description,
                typical_work=career.typical_work,
                eligibility=career.eligibility,
                score_breakdown=score,
                is_diversity_highlight=False,
                diversity_domain=career.domain
            ))
            
    selected_ids = {c.career_id for c in selected}
    
    # Second pass: Surface best candidate from non-represented domains having score >= 50.0
    for career, score in scored_items:
        if career.career_id in selected_ids:
            continue
        d = career.domain
        if d not in domain_tally and score.overall_score >= 50.0:
            domain_tally[d] = 1
            selected.append(CareerCandidate(
                career_id=career.career_id,
                career_name=career.career_name,
                domain=career.domain,
                description=career.description,
                typical_work=career.typical_work,
                eligibility=career.eligibility,
                score_breakdown=score,
                is_diversity_highlight=True,
                diversity_domain=career.domain
            ))
            selected_ids.add(career.career_id)
            if len(selected) >= limit:
                break
                
    # Third pass: If still below limit, fill with remaining highest scoring careers adhering to max 2
    if len(selected) < limit:
        for career, score in scored_items:
            if career.career_id in selected_ids:
                continue
            d = career.domain
            if domain_tally.get(d, 0) < 3:
                domain_tally[d] = domain_tally.get(d, 0) + 1
                selected.append(CareerCandidate(
                    career_id=career.career_id,
                    career_name=career.career_name,
                    domain=career.domain,
                    description=career.description,
                    typical_work=career.typical_work,
                    eligibility=career.eligibility,
                    score_breakdown=score,
                    is_diversity_highlight=False,
                    diversity_domain=career.domain
                ))
                selected_ids.add(career.career_id)
                if len(selected) >= limit:
                    break
                    
    cdi = calculate_cdi(selected)
    return selected, cdi, "DISHA Multi-Objective Diversity-Aware Discovery (CDI Optimized)"
