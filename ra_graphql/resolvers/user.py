from ariadne import (
    QueryType,
    ScalarType
)
from crud.user import (
    get_all_users,
    find_user_by_id,
    get_all_users_count,
    find_user_by_email
)

user_query = QueryType()
UUID_scalar = ScalarType("UUID")
datetime_scalar = ScalarType("Datetime")


@datetime_scalar.serializer
def serialize_datetime(value):
    return value.isoformat()


@UUID_scalar.serializer
def serialize_uuid(value):
    return str(value)


@user_query.field("users")
async def resolve_users(
    _,
    info,
    current_user=None,
    **kwargs
):
    users = await get_all_users(**kwargs)
    total_count = await get_all_users_count()
    users = [dict(user) for user in users]
    return {
        "users": users,
        "total_count": total_count
    }


@user_query.field("user")
async def resolve_user(
    _,
    info,
    current_user=None,
    **kwargs
):
    email = kwargs.get("email", None)
    user_id = kwargs.get("id", None)
    resp = {
        "error": "No User found with specified details.",
        "user": None
    }
    if email:
        user = await find_user_by_email(email)
        resp.update(user=user, error="" if user else resp["error"])
    elif user_id:
        user = await find_user_by_id(user_id)
        resp.update(user=user, error="" if user else resp["error"])
    else:
        resp.update(error="id or email parameter required")

    return resp
