"""Test the user endpoints."""

import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from pytest_mock import MockerFixture

from fastapi import testclient
from metadata_service.main import app
from metadata_service.db import get_session
from metadata_service.models import database


@pytest.fixture(autouse=True)
def client():
    """Create a fixture for the FastAPI test client."""
    return testclient.TestClient(app)


def test_get_users(client: testclient.TestClient, mocker: MockerFixture):
    """Test the get_users endpoint."""

    async def session_override():
        mock_context_manager = mocker.MagicMock(AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalars.return_value.all.return_value = [
            database.User(
                id=1,
                name="test",
                email="test@test.com",
                company_id=1,
            ),
            database.User(
                id=2,
                name="test2",
                email="test2@test.com",
                company_id=2,
            ),
        ]
        mock_context_manager.execute.return_value = mock_result
        yield mock_context_manager

    app.dependency_overrides[get_session] = session_override

    response = client.get("/users")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "test",
            "email": "test@test.com",
            "company_id": 1,
        },
        {
            "id": 2,
            "name": "test2",
            "email": "test2@test.com",
            "company_id": 2,
        },
    ]


def test_get_user_success(client: testclient.TestClient, mocker: MockerFixture):
    """Test the get_user endpoint."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = database.User(
            id=1,
            name="test",
            email="test@test.com",
            company_id=1,
        )
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "test",
        "email": "test@test.com",
        "company_id": 1,
    }


def test_get_user_not_found(client: testclient.TestClient, mocker: MockerFixture):
    """Test the get_user endpoint returns 404 not found if the user doesn't exist."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = None
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.get("/users/300")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_user_new(client: testclient.TestClient, mocker: MockerFixture):
    """Test the create_user endpoint. Test creating a new user."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        def mock_refresh(user: database.User):
            user.id = 3

        mock_context_manager.refresh.side_effect = mock_refresh

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.post(
        "/user",
        json={
            "name": "new_user",
            "email": "new_user@fake.com",
            "company_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "company_id": 1,
        "email": "new_user@fake.com",
        "name": "new_user",
    }


def test_update_user(client: testclient.TestClient, mocker: MockerFixture):
    """Test the update_user endpoint. Test updating an existing user."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = database.User(
            id=1,
            name="david",
            email="david@fake.com",
            company_id=1,
        )
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.put(
        "/user/1",
        json={"name": "david_updated", "email": "david@fake.com", "company_id": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "company_id": 1,
        "id": 1,
        "name": "david_updated",
        "email": "david@fake.com",
    }


def test_update_user_not_found(client: testclient.TestClient, mocker: MockerFixture):
    """Test the update_user endpoint returns 404 not found if the user doesn't exist."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = None
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.put(
        "/user/10",
        json={"name": "user_not_found", "email": "user@fake.com", "company_id": 1},
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_user_success(client: testclient.TestClient, mocker: MockerFixture):
    """Test the delete_user endpoint. Test deleting an existing user."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = database.User(
            id=1,
            name="david",
            email="test@fake.com",
            company_id=1,
        )
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.delete("/user/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "david", "status": "deleted"}


def test_delete_user_not_found(client: testclient.TestClient, mocker: MockerFixture):
    """Test the delete_user endpoint. Test deleting a user that doesn't exist."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = None
        mock_context_manager.execute.return_value = mock_result
        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.delete("/user/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
