from application import database
from application import ps


async def startup():
    await database.connect()
    ps.setup(exclude_tables=["alembic_version"])


async def shutdown():
    await database.disconnect()
