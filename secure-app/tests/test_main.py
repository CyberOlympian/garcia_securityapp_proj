import pytest

from app.main import create_app


@pytest.fixture()
def client():
    app = create_app()
    app.config.update({"TESTING": True})
    return app.test_client()


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_echo_success(client):
    response = client.post("/api/v1/echo", json={"message": "  secure hello  "})

    assert response.status_code == 200
    assert response.get_json() == {"message": "secure hello", "length": 12}


def test_echo_rejects_non_string_message(client):
    response = client.post("/api/v1/echo", json={"message": 123})

    assert response.status_code == 400
    assert response.get_json() == {"error": "'message' must be a string"}


def test_echo_rejects_empty_message(client):
    response = client.post("/api/v1/echo", json={"message": "   "})

    assert response.status_code == 400
    assert response.get_json() == {"error": "'message' cannot be empty"}


def test_echo_rejects_too_long_message(client):
    response = client.post("/api/v1/echo", json={"message": "a" * 201})

    assert response.status_code == 400
    assert response.get_json() == {"error": "'message' exceeds max length of 200"}


def test_echo_rejects_invalid_json(client):
    response = client.post(
        "/api/v1/echo",
        data="not-json",
        headers={"Content-Type": "application/json"},
    )

    assert response.status_code == 400
    assert response.get_json() == {"error": "Invalid JSON body"}
