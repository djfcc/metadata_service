"""This is the FastAPI router for team-related endpoints."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Any

router = APIRouter()

# TODO: Replace with a database.
teams: list[dict[Any, Any]] = [{"id": 1, "name": "Database Reliability"}]


@router.get("/teams")
async def get_teams(skip: int = 0, limit: int = 10) -> JSONResponse:
    """This endpoint is used to get team metadata that support pagenation."""
    if skip > len(teams):
        return JSONResponse([])

    if skip + limit > len(teams):
        limit = len(teams)

    return JSONResponse(teams[skip:limit])


@router.get("/teams/{id}")
async def get_team(id: int) -> JSONResponse:
    """This is the root of the FastApi demo."""
    try:
        return JSONResponse(teams[id - 1])
    except IndexError:
        return JSONResponse(content={"status_code": 404}, status_code=404)


@router.post("/team")
async def create_team() -> JSONResponse:
    """This endpoint is used to create team metadata.

    200 team has been created successfully.
    Any other value the team hasn't been created.
    """
    return JSONResponse(content={"status_code": 200}, status_code=200)


@router.delete("/team/{id}")
async def delete_team(id: int) -> JSONResponse:
    """This endpoint is used to delete team metadata.

    200 team has been deleted successfully.
    Any other value the team hasn't been deleted.
    """
    if teams[id - 1]:
        team = teams.pop(id - 1)
        return JSONResponse(
            content={"id": id, "name": team.get("name"), "status": "deleted"},
            status_code=200,
        )
    return JSONResponse(content={"status_code": 404}, status_code=404)
