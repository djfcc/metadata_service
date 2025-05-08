"""Database models for the application."""

from sqlmodel import Field, SQLModel


class Company(SQLModel, table=True):
    """Database model for a company."""

    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=100)


class Team_Members(SQLModel, table=True):
    """Database model for team members."""

    team_id: int | None = Field(default=None, foreign_key="team.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", primary_key=True)


class Team(SQLModel, table=True):
    """Database model for a team."""

    id: int | None = Field(default=None, primary_key=True, gt=0)
    name: str = Field(index=True, max_length=100)
    company_id: int = Field(foreign_key="company.id", gt=0)
    description: str = Field(max_length=255)


class User(SQLModel, table=True):
    """Database model for a user."""

    id: int | None = Field(default=None, primary_key=True, gt=0)
    name: str = Field(index=True, max_length=50)
    email: str = Field(max_length=100)
    company_id: int = Field(foreign_key="company.id", gt=0)


class Resource(SQLModel, table=True):
    """Database model for a resource."""

    id: int = Field(default=None, primary_key=True, gt=0)
    name: str = Field(index=True, max_length=100)
    type: str = Field(max_length=50)
    lifecycle_status: str = Field(max_length=50)
    description: str = Field(max_length=255)
    owner: int = Field(foreign_key="team.id", gt=0)
