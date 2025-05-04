"""A prototype for an API that maintains company metadata."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi_test.routers import users, teams, resources, companies


app = FastAPI()
app.include_router(users.router)
app.include_router(teams.router)
app.include_router(resources.router)
app.include_router(companies.router)


# TODO: Add middleware for metrics and logging.
@app.get("/health/check")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(content={"status": "ok"}, status_code=200)
