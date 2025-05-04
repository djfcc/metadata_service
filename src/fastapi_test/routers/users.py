"""This module contains the FastAPI router for user-related endpoints."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from typing import Any
from ..models.base import User as BaseUser
from ..models.identity_models import User as IdentityUser


router = APIRouter()

# TODO: Replace with a database.
users: list[dict[Any, Any]] = [
    {"id": 1, "name": "david"},
    {"id": 2, "name": "james"},
]


@router.get("/users")
async def get_users(skip: int = 0, limit: int = 10) -> JSONResponse:
    """This endpoint is used to get user metadata that support pagenation."""
    # TODO: This should be replaced with a range query on the database.
    if skip > len(users):
        return JSONResponse([])

    if skip + limit > len(users):
        limit = len(users)

    return JSONResponse(users[skip:limit])


@router.get("/users/{id}")
async def get_user(id: int) -> JSONResponse:
    """This is the root of the FastApi demo."""
    try:
        return JSONResponse(users[id - 1])
    except IndexError:
        raise HTTPException(status_code=404, detail="Item not found")


@router.post("/user")
async def create_user(user: BaseUser) -> JSONResponse:
    """This endpoint is used to create user metadata.

    200 user has been created successfully.
    Any other value the user hasn't been created.
    """
    user = IdentityUser(id=len(users) + 1, **user.model_dump())
    users.append(user.model_dump())
    return JSONResponse(
        content={"id": user.id, "name": user.name, "status": "created"},
        status_code=200,
    )


@router.put("/user/{id}")
async def update_user(id: int, user: BaseUser) -> JSONResponse:
    """This endpoint is used to update user metadata.

    200 user has been updated successfully.
    Any other value the user hasn't been updated.
    """
    try:
        if users[id - 1]:
            users[id - 1] = user.model_dump()
            return JSONResponse(
                content={"id": id, "name": user.name, "status": "updated"},
                status_code=200,
            )
    except IndexError:
        # TODO: This should log something.
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(content={"status_code": 404}, status_code=404)


@router.delete("/user/{id}")
async def delete_user(id: int) -> JSONResponse:
    """This endpoint is used to delete user metadata.

    200 user has been deleted successfully.
    Any other value the user hasn't been deleted.
    """
    user = {}
    try:
        if users[id - 1]:
            user = users.pop(id - 1)
    except IndexError:
        # TODO: This should log something.
        raise HTTPException(status_code=404, detail="Item not found")
    return JSONResponse(
        content={"id": id, "name": user.get("name"), "status": "deleted"},
        status_code=200,
    )
