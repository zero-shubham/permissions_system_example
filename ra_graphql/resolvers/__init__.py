from resolvers.user import (
    user_query,
    UUID_scalar,
    datetime_scalar
)
from resolvers.auth import (
    auth_mutation
)
from resolvers.author import (
    author_mutation,
    author_query
)
from resolvers.group import (
    group_mutation,
    group_query
)
from resolvers.permission import (
    permission_mutation,
    permission_query
)
from resolvers.resource import (
    resource_query
)

resolvers = [
    user_query,
    auth_mutation,
    UUID_scalar,
    author_mutation,
    group_mutation,
    group_query,
    author_query,
    datetime_scalar,
    permission_mutation,
    permission_query,
    resource_query
]
