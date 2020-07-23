from ariadne import (
    MutationType,
    QueryType
)
from uuid import uuid4
from crud.author import (
    create_author,
    get_all_authors,
    get_all_authors_count,
    find_author_by_id,
    find_author_by_email
)
from crud.user import (
    create_new_user
)

author_mutation = MutationType()
author_query = QueryType()


@author_mutation.field("create_author")
async def resolve_create_author(
    _,
    info,
    current_user=None,
    **kwargs
):
    details = kwargs["details"]
    resp = {
        "author": None,
        "error": "Author was not created"
    }
    author_id = await create_new_user(
        obj_in={
            "user_name": details["email"],
            "group": "author",
            "password": details["password"]
        }
    )
    author = await create_author(
        values={
            "id": author_id,
            "email": details["email"],
            "phone": details["phone"]
        }
    )
    resp.update(author=dict(author), error="" if author else resp["error"])
    return resp


@author_query.field("authors")
async def resolve_authors(
    _,
    info,
    current_user=None,
    **kwargs
):
    authors = await get_all_authors(
        kwargs["offset"],
        kwargs["limit"]
    )
    total_count = await get_all_authors_count()
    authors = [dict(author) for author in authors]

    return {
        "authors": authors,
        "total_count": total_count
    }


@author_query.field("author")
async def resolve_author(
    _,
    info,
    current_user=None,
    **kwargs
):
    email = kwargs.get("email", None)
    author_id = kwargs.get("id", None)
    resp = {
        "error": "No author found with specified details.",
        "author": None
    }
    if email:
        author = await find_author_by_email(email)
        resp.update(
            author=author and dict(author),
            error="" if author else resp["error"]
        )
    elif author_id:
        author = await find_author_by_id(author_id)
        resp.update(
            author=author and dict(author),
            error="" if author else resp["error"]
        )
    else:
        resp.update(error="id or email parameter required")

    return resp
