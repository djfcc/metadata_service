"""This is the router for the companies API."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Any

router = APIRouter()

# TODO: Replace with a database.
companies: list[dict[Any, Any]] = [{"id": 1, "name": "devcompany"}]


@router.get("/companies")
async def get_companies(skip: int = 0, limit: int = 10) -> JSONResponse:
    """This endpoint is used to get company metadata that support pagenation."""
    # TODO: This should be replaced with a range query on the database.
    if skip > len(companies):
        return JSONResponse([])

    if skip + limit > len(companies):
        limit = len(companies)

    return JSONResponse(companies[skip:limit])


@router.get("/companies/{id}")
async def get_company(id: int) -> JSONResponse:
    """This is the root of the FastApi demo."""
    try:
        return JSONResponse(companies[id - 1])
    except IndexError:
        return JSONResponse(content={"status_code": 404}, status_code=404)


@router.post("/company")
async def create_company() -> JSONResponse:
    """This endpoint is used to create company metadata.

    200 company has been created successfully.
    Any other value the company hasn't been created.
    """
    return JSONResponse({"status_code": 200})


@router.delete("/company/{id}")
async def delete_company(id: int) -> JSONResponse:
    """This endpoint is used to delete company metadata.

    200 company has been deleted successfully.
    Any other value the company hasn't been deleted.
    """
    if companies[id - 1]:
        company = companies.pop(id - 1)
        return JSONResponse(
            content={"id": id, "name": company.get("name"), "status": "deleted"},
            status_code=200,
        )
    return JSONResponse(content={"status_code": 404}, status_code=404)
