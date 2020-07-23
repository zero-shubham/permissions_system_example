from application import app
from ariadne import (
    make_executable_schema,
    load_schema_from_path
)
from ariadne.asgi import GraphQL
from resolvers import resolvers
from utils.app_event_funcs import (
    shutdown,
    startup
)
from utils.directives import (
    AuthDirective,
    PermsDirective
)


app.add_event_handler("startup", startup)
app.add_event_handler("shutdown", shutdown)


type_defs = load_schema_from_path("./schemas/")

schema = make_executable_schema(type_defs, resolvers, directives={
    "is_authenticated": AuthDirective,
    "has_permission": PermsDirective
})

app.mount("/graphql", GraphQL(schema, debug=True))


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "application:app",
        host="0.0.0.0",
        port=port,
        log_level="info",
        loop="asyncio",
        reload=True,
        lifespan="on"
    )
