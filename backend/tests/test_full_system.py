# backend/tests/test_full_system.py
import pytest
from fastapi.testclient import TestClient

def test_career_graph(client: TestClient, auth_headers: dict):
    # Ensure profile exists
    res_list = client.get("/api/v1/careers", headers=auth_headers)
    assert res_list.status_code == 200
    careers = res_list.json()
    assert len(careers) > 0

    first_id = careers[0]["career_id"]
    res_graph = client.get(f"/api/v1/careers/{first_id}/graph", headers=auth_headers)
    assert res_graph.status_code == 200
    graph = res_graph.json()
    assert "nodes" in graph
    assert "edges" in graph
    assert graph["total_nodes"] >= 1
    assert graph["center_career_id"] == first_id

def test_career_comparison(client: TestClient, auth_headers: dict):
    res_comp = client.post(
        "/api/v1/careers/compare",
        json={"career_ids": ["ux_designer", "data_scientist"]},
        headers=auth_headers
    )
    assert res_comp.status_code == 200
    data = res_comp.json()
    assert len(data["compared_careers"]) == 2
    assert len(data["neutral_observations"]) > 0
    assert "tradeoff_insights" in data

def test_memory_and_decision_trace(client: TestClient, auth_headers: dict):
    # Save a career
    res_save = client.post(
        "/api/v1/memory/save-career",
        json={"career_id": "ux_ui_designer", "career_name": "UI/UX Designer"},
        headers=auth_headers
    )
    assert res_save.status_code == 200

    # Reject a career with rationale
    res_rej = client.post(
        "/api/v1/memory/reject-career",
        json={
            "career_id": "software_engineer",
            "career_name": "Software Engineer",
            "reason": "Avoid 8 hours of solitary syntax coding"
        },
        headers=auth_headers
    )
    assert res_rej.status_code == 200

    # Fetch journey trace
    res_journey = client.get("/api/v1/memory/journey", headers=auth_headers)
    assert res_journey.status_code == 200
    j_data = res_journey.json()
    assert "UI/UX Designer" in j_data["saved_careers"]
    assert any(r["career_name"] == "Software Engineer" for r in j_data["rejected_careers_with_reasons"])
    assert len(j_data["timeline"]) > 0

def test_research_metrics_and_evaluation(client: TestClient, auth_headers: dict):
    # Rate confidence
    res_rate = client.post(
        "/api/v1/research/confidence",
        json={"stage": "pre_exploration", "confidence_score": 5.0},
        headers=auth_headers
    )
    assert res_rate.status_code == 200

    res_rate_post = client.post(
        "/api/v1/research/confidence",
        json={"stage": "post_exploration", "confidence_score": 9.0},
        headers=auth_headers
    )
    assert res_rate_post.status_code == 200

    # Fetch research metrics
    res_metrics = client.get("/api/v1/research/metrics", headers=auth_headers)
    assert res_metrics.status_code == 200
    metrics = res_metrics.json()
    assert "average_career_diversity_index" in metrics
    assert "domain_coverage_distribution" in metrics
    assert metrics["average_career_diversity_index"] > 0
