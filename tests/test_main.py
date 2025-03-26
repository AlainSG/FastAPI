# test_main.py
import pytest
from fastapi.testclient import TestClient

from src.main import app, fake_users_db


@pytest.fixture
def reset_db():
    original_db = {"1": {"name": "Alice", "age": 25}, "2": {"name": "Bob", "age": 30}}
    fake_users_db.clear()
    fake_users_db.update(original_db)


client = TestClient(app)


def test_get_users(reset_db):
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_user(reset_db):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_user_not_found(reset_db):
    response = client.get("/users/99")
    assert response.status_code == 404


def test_create_user(reset_db):
    new_user = {"name": "Charlie", "age": 35}
    response = client.post("/users", json=new_user)
    assert response.status_code == 200
    assert response.json()["name"] == "Charlie"


def test_delete_user(reset_db):
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted"


def test_delete_user_not_found(reset_db):
    response = client.delete("/users/99")
    assert response.status_code == 404


def test_upload_file():
    file_content = b"dummy content"
    files = {"file": ("test.txt", file_content, "text/plain")}
    response = client.post("/upload", files=files)
    assert response.status_code == 200
    assert response.json()["filename"] == "test.txt"


def test_secure_data():
    headers = {"Authorization": "Bearer fake-token"}
    response = client.get("/secure-data", headers=headers)
    assert response.status_code == 200
    assert "token_data" in response.json()


def test_secure_data_invalid_token():
    headers = {"Authorization": "Bearer invalid-token"}
    response = client.get("/secure-data", headers=headers)
    assert response.status_code == 401
