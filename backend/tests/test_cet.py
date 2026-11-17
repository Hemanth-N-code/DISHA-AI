# backend/tests/test_cet.py
import pytest
from fastapi.testclient import TestClient

def test_get_supported_exams_and_domains(client: TestClient):
    res = client.get("/api/v1/cet/exams")
    assert res.status_code == 200
    exams = res.json()
    assert len(exams) >= 1
    assert any(e["id"] == "kcet" for e in exams)

    res_dom = client.get("/api/v1/cet/domains?exam_id=kcet")
    assert res_dom.status_code == 200
    domains = res_dom.json()
    assert len(domains) >= 1
    assert any(d["id"] == "engineering" for d in domains)

def test_cet_profile_creation_and_retrieval(client: TestClient, auth_headers: dict):
    payload = {
        "exam_id": "kcet",
        "domain_id": "engineering",
        "rank": 28000,
        "category": "2A",
        "sub_category": "None",
        "gender": "All",
        "preferred_branches": ["CS", "IS", "EC"],
        "preferred_locations": ["Bengaluru"],
        "preferences": ["placement", "campus"]
    }
    res_post = client.post("/api/v1/cet/profile", json=payload, headers=auth_headers)
    assert res_post.status_code == 200
    data = res_post.json()
    assert data["rank"] == 28000
    assert data["category"] == "2A"

    res_get = client.get("/api/v1/cet/profile", headers=auth_headers)
    assert res_get.status_code == 200
    assert res_get.json()["rank"] == 28000

def test_cet_analyze_options(client: TestClient):
    payload = {
        "rank": 28000,
        "category": "2A",
        "domain_id": "engineering",
        "preferred_branches": ["CS", "IS", "EC"],
        "preferred_locations": ["Bengaluru"],
        "round_num": 1
    }
    res = client.post("/api/v1/cet/analyze", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["student_rank"] == 28000
    assert data["category"] == "2A"
    assert data["total_options_evaluated"] > 0
    assert len(data["options"]) > 0

    # Ensure match labels are valid categories
    valid_labels = {
        "Strong historical match",
        "Possible match",
        "Competitive option",
        "Lower historical cutoff / safer option",
        "Insufficient historical evidence"
    }
    for opt in data["options"]:
        assert opt["historical_match_label"] in valid_labels
        assert "closing_ranks" in opt
        assert "Historical cutoff data is indicative only" in data["disclaimer"]

def test_cet_colleges_and_detail(client: TestClient):
    res = client.get("/api/v1/cet/colleges")
    assert res.status_code == 200
    colleges = res.json()
    assert len(colleges) >= 10

    # Fetch RVCE or BMSCE
    col_id = colleges[0]["id"]
    res_det = client.get(f"/api/v1/cet/colleges/{col_id}")
    assert res_det.status_code == 200
    det = res_det.json()
    assert det["id"] == col_id
    assert len(det["branches"]) > 0

def test_cutoff_trend(client: TestClient):
    res = client.get("/api/v1/cet/college/rvce/trend?branch=CS&category=GM&round_num=1")
    assert res.status_code == 200
    data = res.json()
    assert data["college_id"] == "rvce"
    assert data["branch_code"] == "CS"
    assert len(data["trend_points"]) >= 2
    assert "direction" in data

def test_college_comparison(client: TestClient):
    payload = {
        "college_ids": ["rvce", "bmsce"],
        "branch_code": "CS",
        "category": "GM"
    }
    res = client.post("/api/v1/cet/compare", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["compared_colleges"]) == 2
    assert "disclaimer" in data

def test_option_entry_list_workflow(client: TestClient, auth_headers: dict):
    # 1. Fetch colleges to get a branch ID
    res_col = client.get("/api/v1/cet/colleges/bmsce")
    assert res_col.status_code == 200
    branches = res_col.json()["branches"]
    assert len(branches) > 0
    branch_id_1 = branches[0]["id"]

    res_col2 = client.get("/api/v1/cet/colleges/msrit")
    assert res_col2.status_code == 200
    branch_id_2 = res_col2.json()["branches"][0]["id"]

    # 2. Add first choice
    res_add1 = client.post(
        "/api/v1/cet/option-list/item",
        json={"college_branch_id": branch_id_1, "historical_category": "Strong historical match"},
        headers=auth_headers
    )
    assert res_add1.status_code == 200
    item1_id = res_add1.json()["item_id"]

    # 3. Add second choice
    res_add2 = client.post(
        "/api/v1/cet/option-list/item",
        json={"college_branch_id": branch_id_2, "historical_category": "Possible match"},
        headers=auth_headers
    )
    assert res_add2.status_code == 200
    item2_id = res_add2.json()["item_id"]

    # 4. Get list
    res_list = client.get("/api/v1/cet/option-list", headers=auth_headers)
    assert res_list.status_code == 200
    items = res_list.json()["items"]
    assert len(items) >= 2

    # 5. Reorder: put item 2 first
    res_reorder = client.put(
        "/api/v1/cet/option-list/reorder",
        json={"ordered_item_ids": [item2_id, item1_id]},
        headers=auth_headers
    )
    assert res_reorder.status_code == 200

    res_list_after = client.get("/api/v1/cet/option-list", headers=auth_headers)
    assert res_list_after.json()["items"][0]["id"] == item2_id

    # 6. Delete item
    res_del = client.delete(f"/api/v1/cet/option-list/item/{item1_id}", headers=auth_headers)
    assert res_del.status_code == 200

def test_career_to_branch_mapping(client: TestClient):
    res = client.get("/api/v1/cet/career-branches/data_scientist")
    assert res.status_code == 200
    data = res.json()
    assert data["career_id"] == "data_scientist"
    assert len(data["recommended_academic_branches"]) > 0
