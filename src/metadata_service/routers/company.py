"""This is the router for company API requests."""

from fastapi import APIRouter, HTTPException
from collections.abc import Sequence
from sqlmodel import select
from metadata_service.models import database
from metadata_service.db import SessionDep

router = APIRouter()


@router.get("/companies", response_model=Sequence[database.Company | None])
async def get_companies(
    session: SessionDep,
    skip: int = 0,
    limit: int = 10,
) -> Sequence[database.Company | None]:
    """This endpoint gets companies metadata.

    Args:
        session (SessionDep): The database session.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Company).offset(skip).limit(limit)
            )
            response: Sequence[database.Company] = result.scalars().all()

            return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.get("/companies/{id}", response_model=database.Company | None)
async def get_company(session: SessionDep, id: int) -> database.Company | None:
    """This endpoint gets company metadata.

    Args:
        session (SessionDep): The database session.
        id (int): The ID of the company to retrieve.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Company).where(database.Company.id == id)
            )
            company: database.Company | None = result.scalars().one_or_none()

            if company:
                return company
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")


@router.post("/company", response_model=database.Company | None)
async def create_company(
    session: SessionDep, company: database.Company
) -> database.Company | None:
    """This endpoint create company metadata.

    Args:
        session (SessionDep): The database session.
        company (Company): The company to create.
    """
    try:
        async with session.begin():
            session.add(company)
            await session.flush()
            await session.refresh(company)
            return company
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")


@router.put("/company/{id}", response_model=database.Company | None)
async def update_company(
    id: int, company: database.Company, session: SessionDep
) -> database.Company | None:
    """This endpoint updates company metadata.

    Args:
        id (int): The ID of the company to update.
        company (Company): The company to update.
        session (SessionDep): The database session.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Company).where(database.Company.id == id)
            )
            company_to_update: database.Company | None = result.scalars().one_or_none()
            if company_to_update:
                company_to_update.name = company.name or company_to_update.name
                session.add(company_to_update)
                await session.flush()
                await session.refresh(company_to_update)
                return company_to_update
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")


@router.delete("/company/{id}", response_model=dict[str, int | str])
async def delete_company(id: int, session: SessionDep) -> dict[str, int | str]:
    """This endpoint deletes company metadata.

    Args:
        id (int): The ID of the company to delete.
        session (SessionDep): The database session.
    """
    try:
        async with session.begin():
            result = await session.execute(
                select(database.Company).where(database.Company.id == id)
            )
            company: database.Company | None = result.scalars().one_or_none()

            if company:
                await session.delete(company)
                await session.flush()
                return {"id": id, "name": company.name, "status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {e}")
    raise HTTPException(status_code=404, detail="Item not found")
