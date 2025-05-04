"""Models for the applications response requests."""

from . import base
from typing import Annotated
from pydantic import Field


class Company(base.Company):
    """Company model."""

    id: Annotated[int, Field(gt=0)]


class User(base.User):
    """User model."""

    id: Annotated[int, Field(gt=0)]


class Team(base.Team):
    """Team model."""

    id: Annotated[int, Field(gt=0)]


class Resource(base.Resource):
    """Resource model."""

    id: Annotated[int, Field(gt=0)]
