from application import database, ps
from sqlalchemy import select
from models.Author import Author
from datetime import datetime
import pytz
from uuid import UUID


async def find_author_by_id(_id: UUID):
    query = select(
        [
            Author,
            ps.User
        ]
    ).select_from(
        Author.join(ps.User)
    ).where(
        Author.columns.id == _id
    )
    author = await database.fetch_one(query)
    return author


async def find_author_by_email(email: str):
    query = select(
        [
            Author,
            ps.User
        ]
    ).select_from(
        Author.join(ps.User)
    ).where(
        Author.columns.email == email
    )
    author = await database.fetch_one(query)
    return author


async def create_author(values: dict):
    query = Author.insert()
    values["created_at"] = datetime.utcnow().replace(tzinfo=pytz.utc)
    values["updated_at"] = values["created_at"]
    await database.execute(query=query, values=values)
    new_author = await find_author_by_id(values["id"])
    return new_author


async def get_all_authors(offset: int = 0, limit: int = 10):
    query = select(
        [
            Author,
            ps.User
        ]
    ).select_from(
        Author.join(ps.User)
    ).offset(offset).limit(limit)
    authors = await database.fetch_all(query)
    return authors


async def get_all_authors_count() -> int:
    query = Author.count()
    count = await database.execute(query)
    return count
