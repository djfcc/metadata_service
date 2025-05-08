"""DB engine and session management for database operations."""

from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi import Depends

# TODO: These values should be replaced with environment variables.
sqlite_file_name = "metadata.db"
sqlite_url = f"sqlite+aiosqlite:///db/{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_async_engine(sqlite_url, connect_args=connect_args)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    """Get a session for database operations."""
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
