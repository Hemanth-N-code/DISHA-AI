# backend/tests/test_auth.py
def test_register_and_login(client):
    email = "student_test@disha.edu"
    password = "StrongPassword123!"
    
    # 1. Register
    reg_resp = client.post("/api/v1/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Aarav Sharma"
    })
    assert reg_resp.status_code == 200, reg_resp.text
    reg_data = reg_resp.json()
    assert "access_token" in reg_data
    assert reg_data["email"] == email
    token = reg_data["access_token"]
    
    # 2. Get Me
    me_resp = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_resp.status_code == 200
    me_data = me_resp.json()
    assert me_data["full_name"] == "Aarav Sharma"
    
    # 3. Login
    login_resp = client.post("/api/v1/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    assert "access_token" in login_data
