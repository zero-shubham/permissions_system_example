from ariadne import (
    MutationType
)
from crud.user import (
    find_user_by_email
)
from core.security import (
    verify_password
)
from core.jwt import (
    create_access_token
)
from crud.token import (
    add_token_in_db,
    remove_token_in_db
)


auth_mutation = MutationType()


@auth_mutation.field("login")
async def resolve_login(_, info, **kwargs):
    user = await find_user_by_email(kwargs["email"])

    if not user:
        return {
            "error": "User with that email not found"
        }

    password_matched = verify_password(kwargs["password"], user["password"])
    if not password_matched:
        return {
            "error": "Incorrect credentials combination."
        }

    encoded_jwt, expire = create_access_token(
        data={
            "user_id":  str(user["id"]),
            "group": user["group"]
        }
    )
    added_token_in_db = await add_token_in_db(
        user_id=str(user["id"]),
        token=encoded_jwt.decode("utf-8")
    )

    return {
        "token": {
            "access_token": encoded_jwt.decode("utf-8"),
            "token_type": "bearer"
        }
    }


@auth_mutation.field("logout")
async def resolve_logout(
    _,
    info,
    current_user=None,
    **kwargs
):
    resp = {
        "error": "User was not logged out",
        "logged_out": False
    }

    logged_out = await remove_token_in_db(current_user["id"])
    if logged_out:
        resp.update(logged_out=True, error="")
    return resp
