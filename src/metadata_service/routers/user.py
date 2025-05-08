"""This module contains the FastAPI router for user-related endpoints."""
# TODO: Add a functions to add users to a team, remove users from a team and list users in a team

from fastapi import APIRouter, HTTPException
from collections.abc import Sequence
from sqlmodel import select
from metadata_service.models import database, put
from metadata_service.db import SessionDep

router = APIRouter()


@router.get("/users", response_model=Sequence[database.User | None])
async def get_users(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[database.User | None]:
    """This endpoint gets users metadata.

    Args:
        session (SessionDep): The database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.User).offset(skip).limit(limit)
            )
            response: Sequence[database.User] = result.scalars().all()

            return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.get("/users/{id}", response_model=database.User | None)
async def get_user(session: SessionDep, id: int) -> database.User | None:
    """This endpoint gets user metadata.

    Args:
        session (SessionDep): The database session.
        id (int): The ID of the user to retrieve.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.User).where(database.User.id == id)
            )
            user: database.User | None = result.scalars().one_or_none()

            if user:
                return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/user", response_model=database.User | None)
async def create_user(session: SessionDep, user: database.User) -> database.User | None:
    """This endpoint creates user metadata.

    Args:
        session (SessionDep): The database session.
        user (User): The user to create.
    """
    try:
        async with session.begin():
            session.add(user)
            await session.flush()
            await session.refresh(user)
            return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.put("/user/{id}", response_model=database.User | None)
async def update_user(
    id: int, user: put.RequestUser, session: SessionDep
) -> database.User | None:
    """This endpoint updates user metadata.

    Args:
        id (int): The ID of the user to update.
        user (User): The user to update.
        session (SessionDep): The database session.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.User).where(database.User.id == id)
            )
            user_to_update: database.User | None = result.scalars().one_or_none()
            if user_to_update:
                user_to_update.name = user.name or user_to_update.name
                user_to_update.email = user.email or user_to_update.email
                user_to_update.company_id = user.company_id or user_to_update.company_id

                session.add(user_to_update)
                await session.flush()
                await session.refresh(user_to_update)
                return user_to_update
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/user/{id}", response_model=dict[str, int | str])
async def delete_user(id: int, session: SessionDep) -> dict[str, int | str]:
    """This endpoint deletes user metadata.

    Args:
        id (int): The ID of the user to delete.
        session (SessionDep): The database session.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.User).where(database.User.id == id)
            )
            user: database.User | None = result.scalars().one_or_none()

            if user:
                await session.delete(user)
                await session.flush()
                return {"id": id, "name": user.name, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")
