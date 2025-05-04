"""Models for the application post requests."""

from pydantic import BaseModel, ConfigDict


class Company(BaseModel):
    """Company model."""

    name: str

    model_config = ConfigDict(extra="forbid")


class User(BaseModel):
    """User model."""

    name: str
    email: str
    company_id: int
    teams: list[int]

    model_config = ConfigDict(extra="forbid")


class Team(BaseModel):
    """Team model."""

    name: str
    company_id: int
    description: str
    members: list[User]

    model_config = ConfigDict(extra="forbid")


class Resource(BaseModel):
    """Resource model."""

    name: str
    type: str
    lifecycle_status: str
    description: str
    owner: int
    company_id: int

    model_config = ConfigDict(extra="forbid")
