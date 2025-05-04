"""This is the router for the resources API."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from typing import Any

router = APIRouter()


# TODO: Replace with a database.
resources: list[dict[Any, Any]] = [{"id": 1, "name": "devdatabase"}]


@router.get("/resources")
async def get_resources(skip: int = 0, limit: int = 10) -> JSONResponse:
    """This endpoint is used to get resource metadata that supports pagenation."""
    # TODO: This should be replaced with a range query on the database.
    if skip > len(resources):
        return JSONResponse([])

    if skip + limit > len(resources):
        limit = len(resources)

    return JSONResponse(resources[skip:limit])


@router.get("/resources/{id}")
async def get_resource(id: int) -> JSONResponse:
    """This is the root of the FastApi demo."""
    try:
        return JSONResponse(resources[id - 1])
    except IndexError:
        return JSONResponse(content={"status_code": 404}, status_code=404)


@router.post("/resource")
async def create_resource() -> JSONResponse:
    """This endpoint is used to create resource metadata.

    200 resource has been created successfully.
    Any other value the resource hasn't been created.
    """
    return JSONResponse(content={"status_code": 200}, status_code=200)


@router.delete("/resource/{id}")
async def delete_resource(id: int) -> JSONResponse:
    """This endpoint is used to delete resource metadata.

    200 resource has been deleted successfully.
    Any other value the resource hasn't been deleted.
    """
    if resources[id - 1]:
        resource = resources.pop(id - 1)
        return JSONResponse(
            content={"id": id, "name": resource.get("name"), "status": "deleted"},
            status_code=200,
        )
    return JSONResponse(content={"status_code": 404}, status_code=404)
