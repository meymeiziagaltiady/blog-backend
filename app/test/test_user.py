import pytest
from fastapi import status

# creation test


def test_admin_can_create_user(client, admin_token, new_user_data):
    res = client.post(
        "/users/",
        json=new_user_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    data = res.json()["data"]

    assert res.status_code == status.HTTP_201_CREATED

    res = client.delete(
        f"/users/{data['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )


def test_user_cannot_create_user(client, user1_token, new_user_data):
    res = client.post(
        "/users/",
        json=new_user_data,
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_create_user_duplicate_username(client, admin_token, new_user_data):
    res = client.post(
        "/users/",
        json=new_user_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    res = client.post(
        "/users/",
        json=new_user_data,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_create_user_missing_token(client, new_user_data):
    res = client.post(
        "/users/",
        json=new_user_data,
    )
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


# get test


def test_admin_can_get_user(client, admin_token):
    res = client.get("/users/1", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == status.HTTP_200_OK


def test_user_cannot_get_user(client, user1_token):
    res = client.get("/users/1", headers={"Authorization": f"Bearer {user1_token}"})
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_get_unknown_user(client, admin_token):
    res = client.get("/users/99999", headers={"Authorization": f"Bearer {admin_token}"})
    assert res.status_code == status.HTTP_404_NOT_FOUND


# update test
@pytest.mark.parametrize(
    "username, password, role",
    [
        ("test_updated_user", None, None),  # update username only
        (None, "test_updated_user", None),  # update password only
        (None, None, "admin"),  # update role only
        ("test_full_update_user", "test_updated_user", "user"),  # update all
    ],
)
def test_admin_can_update_user(client, admin_token, username, password, role):
    res = client.post(
        "/users/",
        json={"username": "test_update", "password": "test_update"},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()["data"]

    user_id = res["id"]

    payload = {}
    if username:
        payload["username"] = username
    if password:
        payload["password"] = password
    if role:
        payload["role"] = role

    res = client.put(
        f"/users/{user_id}",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert res.status_code == status.HTTP_200_OK

    # validate returned data
    data = res.json()["data"]
    if username:
        assert data["username"] == username
    if role:
        assert data["role"] == role

    res = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )


def test_user_cannot_update_user(client, user1_token, user2_data_from_token):
    user_id = user2_data_from_token.id

    res = client.put(
        f"/users/{user_id}",
        json={"username": "user2_new"},
        headers={"Authorization": f"Bearer {user1_token}"},
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN


# deletion test
def test_admin_can_delete_user(client, admin_token):
    res = client.post(
        "/users/",
        json={"username": "test_delete", "password": "test_delete"},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()["data"]

    res = client.delete(
        f"/users/{res['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )

    assert res.status_code == status.HTTP_200_OK


def test_user_cannot_delete_user(client, user1_token, user2_data_from_token):
    user_id = user2_data_from_token.id

    res = client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {user1_token}"},
    )

    assert res.status_code == status.HTTP_403_FORBIDDEN

def test_delete_unknown_user(client, admin_token):
    res = client.delete(
        "/users/999999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND