# cymap

## Description
A work-in-progress prototype of a web app I developed for processing time-series metrics.
The goals are to create a Python API that utilizes the high-performance TimescaleDB extension for PostgreSQL, and learn the fundamentals of RESTful API development, Docker containerization, and Microsoft Entra ID access management.

## Commands

Deploy containers:
```
cd backend
docker compose up [-d]
```

Optionally, open a shell in the container and/or interact with a database
```
docker exec -it cymap-timescale-1 /bin/bash
psql -d ts_db -U ts-user
```


## TODO
- Set up testing framework
- Write unit tests
- Set up database migrations
- Implement a React frontend

## References
https://github.com/ThomasAitken/demo-fastapi-async-sqlalchemy/

https://github.com/gpkc/fastapi-sqlalchemy-pytest

https://medium.com/@navinsharma9376319931/mastering-fastapi-crud-operations-with-async-sqlalchemy-and-postgresql-3189a28d06a2

https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

https://github.com/astral-sh/uv-docker-example

https://github.com/Intility/fastapi-azure-auth

https://github.com/timescale/timescaledb

https://github.com/dorosch/sqlalchemy-timescaledb