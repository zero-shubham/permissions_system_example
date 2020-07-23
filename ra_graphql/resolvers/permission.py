from ariadne import (
    QueryType,
    MutationType
)
from crud.permission import (
    add_new_permission,
    update_permissions_by_id,
    get_all_permissions_count_in_db,
    get_all_permissions_in_db,
    get_permission_by_id
)

permission_query = QueryType()
permission_mutation = MutationType()


@permission_mutation.field("create_permission")
async def resolve_create_permission(
    _,
    info,
    current_user=None,
    **kwargs
):
    details = kwargs["details"]
    added_permission = await add_new_permission(details)
    return {
        "permission": dict(added_permission)
    }


@permission_mutation.field("update_permission")
async def resolve_update_permission(
    _,
    info,
    current_user=None,
    **kwargs
):
    details = kwargs["details"]
    _id = details["id"]
    del details["id"]
    updated_permission = await update_permissions_by_id(
        _id,
        details
    )
    return {
        "permission": dict(updated_permission)
    }


@permission_query.field("permissions")
async def resolve_permissions(
    _,
    info,
    current_user=None,
    **kwargs
):
    permissions = await get_all_permissions_in_db(
        kwargs["offset"],
        kwargs["limit"]
    )
    total_count = await get_all_permissions_count_in_db()
    permissions = [dict(permission) for permission in permissions]
    return {
        "permissions": permissions,
        "total_count": total_count
    }


@permission_query.field("permission")
async def resolve_permission(
    _,
    info,
    current_user=None,
    **kwargs
):
    permission = await get_permission_by_id(kwargs["id"])
    return {
        "permission": dict(permission),
        "error": "Permission not found for specified ID" if not permission else ""
    }
