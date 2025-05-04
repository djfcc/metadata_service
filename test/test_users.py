"""Test the users endpoints."""

from fastapi import testclient
from fastapi_test import main

client = testclient.TestClient(main.app)


def test_get_users():
    """Test the get_users endpoint."""
    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "name": "david"},
        {"id": 2, "name": "james"},
    ]


def test_get_user():
    """Test the get_user endpoint."""
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "david"}

    response = client.get("/users/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_user():
    """Test the create_user endpoint.

    Test creating a new user.
    Test creating a new user with an existing name.

    Both tests should succeed.
    """
    response = client.post(
        "/user",
        json={
            "name": "new_user",
            "email": "new_user@fake.com",
            "company_id": 1,
            "teams": [1],
        },
    )
    assert response.status_code == 200
    assert response.json() == {"id": 3, "name": "new_user", "status": "created"}

    response = client.post(
        "/user",
        json={
            "name": "david",
            "email": "david@fake.com",
            "company_id": 1,
            "teams": [1],
        },
    )
    assert response.status_code == 200
    assert response.json() == {"id": 4, "name": "david", "status": "created"}


def test_update_user():
    """Test the update_user endpoint.

    Test updating an existing user.
    Test updating a user that doesn't exist.

    Both tests should succeed.
    """
    response = client.put(
        "/user/1",
        json={
            "name": "david_updated",
            "email": "david@fake.com",
            "company_id": 1,
            "teams": [1],
        },
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "david_updated", "status": "updated"}

    response = client.put(
        "/user/10",
        json={
            "name": "user_not_found",
            "email": "user@fake.com",
            "company_id": 1,
            "teams": [1],
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_user():
    """Test the delete_user endpoint.

    Test deleting an existing user.
    Test deleting a user that doesn't exist.

    Both tests should succeed.
    """
    response = client.delete("/user/2")
    assert response.status_code == 200
    assert response.json() == {"id": 2, "name": "james", "status": "deleted"}

    response = client.delete("/user/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
