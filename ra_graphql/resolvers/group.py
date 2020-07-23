from ariadne import (
    MutationType,
    QueryType
)
from crud.group import (
    add_new_group,
    get_all_groups,
    get_all_groups_count,
    get_user_group_by_id
)

group_mutation = MutationType()
group_query = QueryType()


@group_mutation.field("create_group")
async def resolve_create_group(
    _,
    info,
    current_user=None,
    **kwargs
):
    resp = {
        "error": "Group not added",
        "group": None
    }

    group = await add_new_group(kwargs["group"])
    resp.update(group=group, error="" if group else resp["error"])
    return resp


@group_query.field("groups")
async def resolve_groups(
    _,
    info,
    current_user=None,
    **kwargs
):
    groups = await get_all_groups(
        kwargs["offset"], kwargs["limit"])
    total_count = await get_all_groups_count()
    groups = [dict(group) for group in groups]
    return {
        "groups": groups,
        "total_count": total_count
    }


@group_query.field("group")
async def resolve_group(
    _,
    info,
    current_user=None,
    **kwargs
):
    group = await get_user_group_by_id(kwargs["id"])
    return {
        "group": dict(group),
        "error": "Group not found for specified ID" if not group else ""
    }
