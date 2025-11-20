from fastapi import status

# create test


def test_user_can_create_content(client, user1_token, content_data):
    res = client.post(
        "/content/",
        json=content_data,
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert res.status_code == status.HTTP_201_CREATED


# get test


def test_user_can_list_own_content(client, user1_token):
    res = client.get("/content/", headers={"Authorization": f"Bearer {user1_token}"})
    assert res.status_code == status.HTTP_200_OK


def test_user_can_retrieve_one_owned_content(client, user1_token):
    c = client.post(
        "/content/",
        json={"title": "x", "body": "y"},
        headers={"Authorization": f"Bearer {user1_token}"},
    ).json()["data"]

    res = client.get(
        f"/content/{c['id']}", headers={"Authorization": f"Bearer {user1_token}"}
    )
    assert res.status_code == status.HTTP_200_OK


def test_user_cannot_retrieve_others_content(client, admin_token, user1_token):
    # test admin creates
    c = client.post(
        "/content/",
        json={"title": "retrieve x", "body": "yy"},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()["data"]

    # test user tries to retrieve
    res = client.put(
        f"/content/{c['id']}",
        json={"title": "zz"},
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_get_unexist_content(client, admin_token):
    res = client.get(
        "/content/99999", headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND


# update test


def test_user_can_update_own_content(client, user1_token, content_update_data):
    c = client.post(
        "/content/",
        json={"title": "x", "body": "y"},
        headers={"Authorization": f"Bearer {user1_token}"},
    ).json()["data"]

    # update
    res = client.put(
        f"/content/{c['id']}",
        json=content_update_data,
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert res.status_code == status.HTTP_200_OK


def test_user_cannot_update_others_content(client, admin_token, user1_token):
    # test admin creates
    c = client.post(
        "/content/",
        json={"title": "update x", "body": "yy"},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()["data"]

    # test user tries to update
    res = client.put(
        f"/content/{c['id']}",
        json={"title": "zz"},
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN


# delete test


def test_user_can_delete_own_content(client, user1_token, content_update_data):
    c = client.post(
        "/content/",
        json={"title": "x", "body": "y"},
        headers={"Authorization": f"Bearer {user1_token}"},
    ).json()["data"]

    # delete
    res = client.delete(
        f"/content/{c['id']}",
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert res.status_code == status.HTTP_200_OK


def test_user_cannot_delete_others_content(client, admin_token, user1_token):
    # test admin creates
    c = client.post(
        "/content/",
        json={"title": "delete x", "body": "yy"},
        headers={"Authorization": f"Bearer {admin_token}"},
    ).json()["data"]

    # test user tries to delete
    res = client.delete(
        f"/content/{c['id']}",
        headers={"Authorization": f"Bearer {user1_token}"},
    )
    assert res.status_code == status.HTTP_403_FORBIDDEN


def test_delete_unexist_content(client, admin_token):
    res = client.delete(
        "/content/99999",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert res.status_code == status.HTTP_404_NOT_FOUND
