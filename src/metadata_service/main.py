"""A prototype for an API that maintains company metadata."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from metadata_service.routers import company, resource, team, user


app = FastAPI()
app.include_router(user.router)
app.include_router(team.router)
app.include_router(resource.router)
app.include_router(company.router)


# TODO: Add middleware for metrics and logging.
@app.get("/health/check")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(content={"status": "ok"}, status_code=200)
