# backend/app/recommendation/graph.py
from typing import Dict, Any, List

def build_career_graph(
    center_career: Any,
    all_careers_map: Dict[str, Any],
    depth: int = 1
) -> Dict[str, Any]:
    """
    Builds a directed React Flow graph representation centered on a focal career.
    Constructs nodes (Careers, Domains, Skill Clusters) and typed edges with weights.
    """
    nodes = []
    edges = []
    visited = set()
    
    center_id = center_career.career_id
    visited.add(center_id)
    
    # 1. Add center node
    nodes.append({
        "id": center_id,
        "type": "careerNode",
        "data": {
            "label": center_career.career_name,
            "domain": center_career.domain,
            "isCenter": True,
            "description": center_career.description[:100] + "...",
            "careerId": center_id
        },
        "position": {"x": 350, "y": 250}
    })
    
    # 2. Add Alternative Careers (Primary Lateral Pivots)
    alternatives = center_career.alternative_careers or []
    # Layout alternatives in an arc around the center
    import math
    n_alt = len(alternatives)
    for i, alt_id in enumerate(alternatives):
        alt_career = all_careers_map.get(alt_id)
        if not alt_career:
            continue
            
        angle = (2 * math.pi / max(n_alt, 1)) * i - (math.pi / 2)
        radius = 280
        x = 350 + int(radius * math.cos(angle))
        y = 250 + int(radius * math.sin(angle))
        
        if alt_id not in visited:
            visited.add(alt_id)
            nodes.append({
                "id": alt_id,
                "type": "careerNode",
                "data": {
                    "label": alt_career.career_name,
                    "domain": alt_career.domain,
                    "isCenter": False,
                    "relationType": "Alternative Pathway",
                    "description": alt_career.description[:90] + "...",
                    "careerId": alt_id
                },
                "position": {"x": x, "y": y}
            })
            
        edges.append({
            "id": f"edge-{center_id}-{alt_id}",
            "source": center_id,
            "target": alt_id,
            "label": "Alternative Pivot",
            "animated": True,
            "style": {"stroke": "#4f46e5", "strokeWidth": 2}
        })
        
    # 3. Add Related / Adjacent Careers
    related = center_career.related_careers or []
    for j, rel_id in enumerate(related):
        if rel_id in visited:
            continue
        rel_career = all_careers_map.get(rel_id)
        if not rel_career:
            continue
            
        visited.add(rel_id)
        rx = 350 + (j - len(related)//2) * 220
        ry = 550
        
        nodes.append({
            "id": rel_id,
            "type": "careerNode",
            "data": {
                "label": rel_career.career_name,
                "domain": rel_career.domain,
                "isCenter": False,
                "relationType": "Adjacent Specialization",
                "description": rel_career.description[:90] + "...",
                "careerId": rel_id
            },
            "position": {"x": rx, "y": ry}
        })
        
        edges.append({
            "id": f"edge-{center_id}-{rel_id}",
            "source": center_id,
            "target": rel_id,
            "label": "Adjacent Specialization",
            "style": {"stroke": "#0891b2", "strokeDasharray": "5,5", "strokeWidth": 1.5}
        })

    return {
        "nodes": nodes,
        "edges": edges,
        "center_career_id": center_id,
        "total_nodes": len(nodes),
        "total_edges": len(edges)
    }
