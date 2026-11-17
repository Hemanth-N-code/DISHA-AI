# backend/app/graph/orchestrator.py
from typing import TypedDict, Dict, Any, List, Optional
from langgraph.graph import StateGraph, END
from app.agents.profile_agent import profile_agent
from app.agents.discovery_agent import discovery_agent
from app.agents.analysis_agent import analysis_agent
from app.agents.roadmap_agent import roadmap_agent

class DishaGraphState(TypedDict):
    user_id: int
    raw_profile_input: Dict[str, Any]
    structured_profile: Dict[str, Any]
    memory_context: str
    all_careers_pool: List[Any]
    discovered_candidates: List[Any]
    selected_career_id: Optional[str]
    career_analysis: Optional[Dict[str, Any]]
    generated_roadmap: Optional[List[Dict[str, Any]]]
    workflow_step: str

def profile_node(state: DishaGraphState) -> Dict[str, Any]:
    """Processes raw profile into archetype & strengths."""
    raw = state["raw_profile_input"]
    # Synthesize using Profile Agent
    from app.schemas.profile import ProfileCreate
    p_obj = ProfileCreate(**raw)
    result = profile_agent.process_profile(p_obj)
    return {
        "structured_profile": result,
        "workflow_step": "profile_processed"
    }

def discovery_node(state: DishaGraphState) -> Dict[str, Any]:
    """Runs diversity-aware candidate discovery."""
    from app.schemas.profile import ProfileCreate
    p_obj = ProfileCreate(**state["raw_profile_input"])
    pool = state["all_careers_pool"]
    
    discovery_result = discovery_agent.discover_careers(
        profile=p_obj,
        all_careers=pool,
        apply_diversity=True,
        limit=10
    )
    return {
        "discovered_candidates": discovery_result.candidates,
        "workflow_step": "careers_discovered"
    }

def analysis_node(state: DishaGraphState) -> Dict[str, Any]:
    """Analyzes selected career if present, otherwise picks top discovered candidate."""
    selected_id = state.get("selected_career_id")
    candidates = state.get("discovered_candidates") or []
    
    if not selected_id and candidates:
        selected_id = candidates[0].career_id

    pool = state["all_careers_pool"]
    target_career = next((c for c in pool if c.career_id == selected_id), None)
    
    analysis_res = None
    if target_career:
        from app.schemas.profile import ProfileCreate
        p_obj = ProfileCreate(**state["raw_profile_input"])
        analysis_res = analysis_agent.analyze_career_path(
            profile=p_obj,
            career=target_career,
            memory_context=state.get("memory_context", "")
        )
        
    return {
        "selected_career_id": selected_id,
        "career_analysis": analysis_res,
        "workflow_step": "career_analyzed"
    }

def roadmap_node(state: DishaGraphState) -> Dict[str, Any]:
    """Generates milestone roadmap for selected career."""
    selected_id = state.get("selected_career_id")
    pool = state["all_careers_pool"]
    target_career = next((c for c in pool if c.career_id == selected_id), None)
    
    roadmap_tasks = []
    if target_career:
        from app.schemas.profile import ProfileCreate
        p_obj = ProfileCreate(**state["raw_profile_input"])
        roadmap_tasks = roadmap_agent.generate_roadmap(p_obj, target_career, horizon_months=6)
        
    return {
        "generated_roadmap": roadmap_tasks,
        "workflow_step": "completed"
    }

# Build the LangGraph State Machine
builder = StateGraph(DishaGraphState)
builder.add_node("profile_agent", profile_node)
builder.add_node("discovery_agent", discovery_node)
builder.add_node("analysis_agent", analysis_node)
builder.add_node("roadmap_agent", roadmap_node)

builder.set_entry_point("profile_agent")
builder.add_edge("profile_agent", "discovery_agent")
builder.add_edge("discovery_agent", "analysis_agent")
builder.add_edge("analysis_agent", "roadmap_agent")
builder.add_edge("roadmap_agent", END)

disha_langgraph_app = builder.compile()
