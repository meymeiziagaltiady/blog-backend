import pytest
from fastapi.testclient import TestClient

from app.src.jwt.jwt_handler import get_user_data
from app.src.main import app


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


# TEST DATA


@pytest.fixture
def user_admin_data():
    return {"username": "test_admin", "password": "test_admin"}


@pytest.fixture
def user1_data():
    return {"username": "test_user1", "password": "test_user1"}


@pytest.fixture
def user2_data():
    return {"username": "test_user2", "password": "test_user2"}


@pytest.fixture
def new_user_data():
    return {"username": "test_new_user", "password": "test_new_user", "role": "user"}


@pytest.fixture
def content_data():
    return {"title": "Test  Content", "body": "This is content test Create"}


@pytest.fixture
def content_update_data():
    return {"title": "Updated Title"}


# auth and get token test users


@pytest.fixture()
def admin_token(client, user_admin_data):
    res = client.post("/token", json=user_admin_data)

    return res.json()["access_token"]


@pytest.fixture()
def user1_token(client, user1_data):
    res = client.post("/token", json=user1_data)

    return res.json()["access_token"]


@pytest.fixture()
def user2_token(client, user2_data):
    res = client.post("/token", json=user2_data)

    return res.json()["access_token"]


# get user data from token


@pytest.fixture
def user2_data_from_token(user2_token):
    return get_user_data(user2_token)
