"""Test the team endpoints."""

import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from pytest_mock import MockerFixture

from fastapi import testclient
from metadata_service.main import app
from metadata_service.db import get_session
from metadata_service.models import database


def test_get_teams(client: testclient.TestClient, mocker: MockerFixture):
    """Test the get_teams endpoint."""

    async def session_override():
        mock_context_manager = mocker.MagicMock(AsyncSession)
        mock_result = mocker.Mock()
        mock_result.scalars.return_value.all.return_value = [
            database.Team(
                id=1,
                name="test team",
                description="test description",
                company_id=1,
            ),
            database.Team(
                id=2,
                name="test team 2",
                description="test description",
                company_id=1,
            ),
        ]
        mock_context_manager.execute.return_value = mock_result
        yield mock_context_manager

    app.dependency_overrides[get_session] = session_override

    response = client.get("/teams")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "test team",
            "company_id": 1,
            "description": "test description",
        },
        {
            "id": 2,
            "name": "test team 2",
            "company_id": 1,
            "description": "test description",
        },
    ]


def test_get_team_success(client: testclient.TestClient, mocker: MockerFixture):
    """Test the get_team endpoint."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = database.Team(
            id=1,
            name="test team",
            description="test description",
            company_id=1,
        )
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.get("/teams/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "test team",
        "company_id": 1,
        "description": "test description",
    }


def test_get_team_not_found(client: testclient.TestClient, mocker: MockerFixture):
    """Test the get_team endpoint returns 404 not found if the team doesn't exist."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = None
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.get("/teams/300")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_create_team_new(client: testclient.TestClient, mocker: MockerFixture):
    """Test the create_team endpoint. Test creating a new team."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        def mock_refresh(team: database.Team):
            team.id = 3

        mock_context_manager.refresh.side_effect = mock_refresh

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.post(
        "/team",
        json={
            "company_id": 1,
            "description": "bills team",
            "name": "new_team",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "company_id": 1,
        "description": "bills team",
        "name": "new_team",
    }


def test_update_team(client: testclient.TestClient, mocker: MockerFixture):
    """Test the update_team endpoint. Test updating an existing team."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = database.Team(
            id=1,
            name="davids team",
            description="test description",
            company_id=1,
        )
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.put(
        "/team/1",
        json={"name": "david_updated", "description": "super team", "company_id": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "company_id": 1,
        "id": 1,
        "name": "david_updated",
        "description": "super team",
    }


def test_update_team_not_found(client: testclient.TestClient, mocker: MockerFixture):
    """Test the update_team endpoint returns 404 not found if the team doesn't exist."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = None
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.put(
        "/team/10",
        json={
            "name": "team_not_found",
            "description": "new description",
            "company_id": 1,
        },
    )
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}


def test_delete_team_success(client: testclient.TestClient, mocker: MockerFixture):
    """Test the delete_team endpoint. Test deleting an existing team."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = database.Team(
            id=1,
            name="teamx",
            description="test description",
            company_id=1,
        )
        mock_context_manager.execute.return_value = mock_result

        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.delete("/team/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "teamx", "status": "deleted"}


def test_delete_team_not_found(client: testclient.TestClient, mocker: MockerFixture):
    """Test the delete_team endpoint. Test deleting a team that doesn't exist."""

    async def get_session_override():
        mocker = MockerFixture(pytest)
        mock_context_manager = mocker.MagicMock(AsyncSession)

        mock_result = mocker.Mock()
        mock_result.scalars.return_value.one_or_none.return_value = None
        mock_context_manager.execute.return_value = mock_result
        yield mock_context_manager

    app.dependency_overrides[get_session] = get_session_override

    response = client.delete("/team/100")
    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
