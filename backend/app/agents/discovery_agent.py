# backend/app/agents/discovery_agent.py
from typing import List, Any
from app.schemas.career import CareerDiscoverResponse
from app.recommendation.diversity import select_diversity_aware_candidates

class CareerDiscoveryAgent:
    """
    AGENT 2: Career Discovery Agent
    Orchestrates the discovery pipeline:
    Profile -> Retrieval -> Transparent 5-Pillar Scoring -> Diversity Adjustment (CDI) -> Ranked Explainable Candidates.
    """
    def discover_careers(
        self,
        profile: Any,
        all_careers: List[Any],
        apply_diversity: bool = True,
        domain_filter: str = None,
        limit: int = 15
    ) -> CareerDiscoverResponse:
        filtered_pool = all_careers
        if domain_filter:
            filtered_pool = [c for c in all_careers if c.domain.lower() == domain_filter.lower()]
            if not filtered_pool:
                filtered_pool = all_careers

        candidates, cdi, strategy = select_diversity_aware_candidates(
            all_careers=filtered_pool,
            profile=profile,
            limit=limit,
            diversity_enabled=apply_diversity
        )

        domains_rep = list(dict.fromkeys([c.domain for c in candidates]))

        return CareerDiscoverResponse(
            total_careers_in_universe=len(all_careers),
            domains_represented=domains_rep,
            career_diversity_index=cdi,
            candidates=candidates,
            discovery_strategy=strategy
        )

discovery_agent = CareerDiscoveryAgent()
