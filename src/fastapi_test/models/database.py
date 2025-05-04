"""Database models for the application."""

from sqlmodel import Field, SQLModel


class Company(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str
    company_id: int = Field(foreign_key="company.id")


class Team(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    company_id: int = Field(foreign_key="company.id")
    description: str


class UserTeam(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    team_id: int = Field(foreign_key="team.id", primary_key=True)


class Resource(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    type: str
    lifecycle_status: str
    description: str
    owner: int = Field(foreign_key="team.id")
    company_id: int = Field(foreign_key="company.id")
