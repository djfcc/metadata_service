"""This is the router for the resource API."""

from fastapi import APIRouter, HTTPException
from collections.abc import Sequence
from sqlmodel import select
from metadata_service.models import database, put
from metadata_service.db import SessionDep

router = APIRouter()


@router.get("/resources", response_model=Sequence[database.Resource | None])
async def get_resources(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[database.Resource | None]:
    """This endpoint gets resources metadata.

    Args:
        session (SessionDep): The database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Resource).offset(skip).limit(limit)
            )

            return result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.get("/resources/{id}", response_model=database.Resource | None)
async def get_resource(session: SessionDep, id: int) -> database.Resource | None:
    """This endpoint gets resource metadata.

    Args:
        session (SessionDep): The database session.
        id (int): The ID of the resource to retrieve.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Resource).where(database.Resource.id == id)
            )
            resource: database.Resource | None = result.scalars().one_or_none()

            if resource:
                return resource
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/resource", response_model=database.Resource | None)
async def create_resource(
    session: SessionDep, resource: database.Resource
) -> database.Resource | None:
    """This endpoint creates resource metadata.

    Args:
        session (SessionDep): The database session.
        resource (Resource): The resource to create.
    """
    try:
        async with session.begin():
            session.add(resource)
            await session.flush()
            await session.refresh(resource)
            return resource
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.put("/resource/{id}", response_model=database.Resource | None)
async def update_resource(
    id: int, resource: put.RequestResource, session: SessionDep
) -> database.Resource | None:
    """This endpoint updates resource metadata.

    Args:
        id (int): The ID of the resource to update.
        resource (Resource): The resource to update.
        session (SessionDep): The database session.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Resource).where(database.Resource.id == id)
            )
            resource_to_update: database.Resource | None = (
                result.scalars().one_or_none()
            )
            if resource_to_update:
                resource_to_update.name = resource.name or resource_to_update.name
                resource_to_update.type = resource.type or resource_to_update.type
                resource_to_update.lifecycle_status = (
                    resource.lifecycle_status or resource_to_update.lifecycle_status
                )
                resource_to_update.description = (
                    resource.description or resource_to_update.description
                )
                resource_to_update.owner = resource.owner or resource_to_update.owner
                session.add(resource_to_update)
                await session.flush()
                await session.refresh(resource_to_update)
                return resource_to_update
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/resource/{id}", response_model=dict[str, int | str])
async def delete_resource(id: int, session: SessionDep) -> dict[str, int | str]:
    """This endpoint delets resource metadata.

    Args:
        id (int): The ID of the resource to delete.
        session (SessionDep): The database session.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Resource).where(database.Resource.id == id)
            )
            resource: database.Resource | None = result.scalars().one_or_none()

            if resource:
                await session.delete(resource)
                await session.flush()
                return {"id": id, "name": resource.name, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")
