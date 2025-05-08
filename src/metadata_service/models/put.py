"""Database models for the application."""

from pydantic import BaseModel, Field


class RequestTeam(BaseModel):
    """API Request model for a team."""

    id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, max_length=100)
    company_id: int | None = Field(default=None, gt=0)
    description: str | None = Field(default=None, max_length=255)


class RequestUser(BaseModel):
    """API Request model for a user."""

    id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, max_length=50)
    email: str | None = Field(default=None, max_length=100)
    company_id: int | None = Field(default=None, gt=0)


class RequestResource(BaseModel):
    """API Request model for a resource."""

    id: int | None = Field(default=None, gt=0)
    name: str | None = Field(default=None, max_length=100)
    type: str | None = Field(default=None, max_length=50)
    lifecycle_status: str | None = Field(default=None, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    owner: int | None = Field(default=None, gt=0)
