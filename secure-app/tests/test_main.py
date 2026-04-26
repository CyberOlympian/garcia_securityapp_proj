from app.main import app, is_valid_age


def test_valid_age():
    assert is_valid_age(25) is True


def test_invalid_underage_fails_due_to_bug():
    # This should be False for underage users, but currently fails because of a logic bug.
    assert is_valid_age(16) is False


def test_register_endpoint_rejects_underage():
    client = app.test_client()
    response = client.post("/register", json={"username": "alice", "age": 16})
    assert response.status_code == 400
