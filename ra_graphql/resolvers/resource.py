from ariadne import QueryType
from crud.resource import (
    get_all_resources_count_in_db,
    get_all_resources_in_db
)

resource_query = QueryType()


@resource_query.field("resources")
async def resolve_resources(
    _,
    info,
    current_user=None,
    **kwargs
):
    resources = await get_all_resources_in_db(
        kwargs["offset"],
        kwargs["limit"]
    )
    total_count = await get_all_resources_count_in_db()
    resources = [dict(resource) for resource in resources]
    return {
        "resources": resources,
        "total_count": total_count
    }
