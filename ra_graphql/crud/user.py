from typing import List
from uuid import uuid4, UUID
from application import database, ps
from core.security import get_password_hash
from crud.group import (
    get_user_group_by_id
)


async def create_new_user(obj_in) -> UUID:
    hashed_pass = get_password_hash(obj_in["password"])
    user_id = uuid4()
    created_user_id = ps.create_user(
        user_id=user_id,
        user_name=obj_in["user_name"],
        password=hashed_pass,
        user_group=obj_in["group"]
    )
    return created_user_id


async def find_user_by_id(user_id: UUID):
    query = ps.User.select().where(ps.User.columns.id == user_id)
    user = await database.fetch_one(query)
    if user:
        return dict(user.items())


async def find_user_by_email(email: str):
    query = ps.User.select().where(ps.User.columns.user_name == email)
    user = await database.fetch_one(query)
    if user:
        return dict(user.items())


async def get_all_users(offset: int = 0, limit: int = 10):
    query = ps.User.select().offset(offset).limit(limit)
    users = await database.fetch_all(query)
    return users


async def get_all_users_count() -> int:
    query = ps.User.count()
    count = await database.execute(query)
    return count


async def update_user_in_db(user_id: UUID, obj_in):
    query = ps.User.update().where(
        ps.User.columns.id == user_id).values(**obj_in.dict(skip_defaults=True))
    await database.execute(query)
    updated_user = await find_user_by_id(user_id)
    return dict(updated_user.items())


async def delete_user_in_db(user_id: UUID) -> bool:
    query = ps.User.delete().where(
        ps.User.columns.id == user_id
    )
    await database.execute(query)
    exists = await find_user_by_id(user_id)
    return True if not exists else False
