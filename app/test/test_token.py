def test_login_admin_success(client, user_admin_data):
    res = client.post("/token", json=user_admin_data)
    assert res.status_code == 200


def test_login_user_success(client, user1_data):
    res = client.post("/token", json=user1_data)
    assert res.status_code == 200


def test_login_wrong_password(client, user1_data):
    wrong = {"username": user1_data["username"], "password": "wrong"}
    res = client.post("/token", json=wrong)
    assert res.status_code == 401


def test_login_unknown_username(client):
    res = client.post("/token", json={"username": "noone", "password": "x"})
    assert res.status_code == 401


def test_missing_token(client):
    res = client.get("/content/")
    assert res.status_code == 401


def test_invalid_token(client):
    headers = {"Authorization": "Bearer invalidtokenhere"}
    res = client.get("/content/", headers=headers)
    assert res.status_code == 401
