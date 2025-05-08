"""This is the FastAPI router for team-related endpoints."""

from fastapi import APIRouter, HTTPException
from collections.abc import Sequence
from sqlmodel import select
from metadata_service.models import database, put
from metadata_service.db import SessionDep

router = APIRouter()


@router.get("/teams", response_model=Sequence[database.Team | None])
async def get_teams(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[database.Team | None]:
    """This endpoint gets teams metadata.

    Args:
        session (SessionDep): The database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Team).offset(skip).limit(limit)
            )
            response: Sequence[database.Team] = result.scalars().all()

            return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.get("/teams/{id}", response_model=database.Team | None)
async def get_team(session: SessionDep, id: int) -> database.Team | None:
    """This endpoint gets team metadata.

    Args:
        session (SessionDep): The database session.
        id (int): The ID of the team to retrieve.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Team).where(database.Team.id == id)
            )
            team: database.Team | None = result.scalars().one_or_none()

            if team:
                return team
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/team", response_model=database.Team | None)
async def create_team(session: SessionDep, team: database.Team) -> database.Team | None:
    """This endpoint creates team metadata.

    Args:
        session (SessionDep): The database session.
        team (Team): The team to create.
    """
    try:
        async with session.begin():
            db_team: database.Team = database.Team(
                name=team.name,
                company_id=team.company_id,
                description=team.description,
            )

            session.add(db_team)
            await session.flush()
            await session.refresh(db_team)
            return db_team
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.put("/team/{id}", response_model=database.Team | None)
async def update_team(
    id: int, team: put.RequestTeam, session: SessionDep
) -> database.Team | None:
    """This endpoint updates team metadata.

    Args:
        id (int): The ID of the team to update.
        team (Team): The team to update.
        session (SessionDep): The database session.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Team).where(database.Team.id == id)
            )
            team_to_update: database.Team | None = result.scalars().one_or_none()
            if team_to_update:
                team_to_update.name = team.name or team_to_update.name
                team_to_update.company_id = team.company_id or team_to_update.company_id
                team_to_update.description = (
                    team.description or team_to_update.description
                )
                session.add(team_to_update)
                await session.flush()
                await session.refresh(team_to_update)
                return team_to_update
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/team/{id}", response_model=dict[str, int | str])
async def delete_team(id: int, session: SessionDep) -> dict[str, int | str]:
    """This endpoint deletes a team's metadata.

    Args:
        id (int): The ID of the team to delete.
        session (SessionDep): The database session.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Team).where(database.Team.id == id)
            )
            team: database.Team | None = result.scalars().one_or_none()

            if team:
                await session.delete(team)
                await session.flush()
                return {"id": id, "name": team.name, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")
