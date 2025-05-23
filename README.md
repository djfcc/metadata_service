# Metadata Service 
This proof of concept solution centrally records environment metadata to provide service discovery for users and systems. 

## Design decisions
1. The FastApi framework was picked for the POC because of its popularity and because it's asynchronous out of the box.
1. A relational database has been used for the proof of concept as this provides maximum flexibility while learning which access patterns are more commonly required. A Document or Key Value database might be better in the future once the access pattern are understood.
1. UUID should be used for all identifiers of the entities so entities are globally unique and identifiable throughout the system and can be generated by distributed systems. For example, a system that creates database resources should be able to generate the UUID and add it to the metadata database for lookups. 

    Currently, IDs are generated in the metadata database for the purposes of building the system. If a relational database is used then the UUID version should support indexing to ensure performant lookups. 
1. The Api models have been seperated out into database and put request models. Database models ensure POST requests do not accept IDs, PUT requests models are less strict allowing any entity attribute to be empty.
1. Alembic is designed for database schema migrations, but not seed/test data, so seed/test data has been added manually.

## Improvements/Todo
1. Add Routes to add and remove users from teams. 
1. Update team and user response models to include team member and team data.
1. Add unit testing for all routes.
1. the unit tests could be asynchronous but unless we are testing the async functionality specifically it probably isn't worth it.
1. Add logging 
1. Add Metrics 
1. Add tracing
1. Remove the hard coded environment variables and load them from the environment or environment files.  

## Bill of Materials
- Recommended IDE [Visual Studio Code](https://code.visualstudio.com/)
- [Dev Container Extensions](https://code.visualstudio.com/docs/devcontainers/containers)
- [Docker](https://www.docker.com/)
- Package Manager [uv](https://docs.astral.sh/uv/guides) 
- [Pytest](https://docs.pytest.org/en/stable/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [Ruff](https://docs.astral.sh/ruff/)
- [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html)
- [SQLLite](https://www.sqlite.org/)
- [SQLModel](https://sqlmodel.tiangolo.com)
- [FastApi](https://fastapi.tiangolo.com/)

## Run Development API Server 
1. Build VS Code dev container
1. `uv run fastapi dev ./src/metadata_service/main.py`

## Run Unit Tests
1. `uv run pytest`

Or

1. `Testing` primary side bar

## Add DB migration Script
1. 'alembic revision -m '<Enter migration description>`
1. Go to `/alembic/versions/<hash_migration_description>.py` and add migration
