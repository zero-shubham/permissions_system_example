from ariadne import SchemaDirectiveVisitor
from utils.funcs import (
    extract_token_from_context,
    get_current_user,
    UserHasResourcePermission
)


class AuthDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        original_resolver = field.resolve

        async def authorization(obj, info, **kwargs):
            token = extract_token_from_context(info.context)
            user, error_msg = await get_current_user(token)
            if user:
                kwargs["current_user"] = user
                result = await original_resolver(obj, info, **kwargs)
            else:
                return {
                    "error": error_msg
                }
            return result

        field.resolve = authorization
        return field


class PermsDirective(SchemaDirectiveVisitor):
    def visit_field_definition(self, field, object_type):
        resource = self.args.get("resource")
        permission = self.args.get("permission")
        original_resolver = field.resolve
        user_has_req_perms = UserHasResourcePermission(resource, permission)

        async def has_required_perms(obj, info, **kwargs):
            token = extract_token_from_context(info.context)
            has_perms, error_msg = await user_has_req_perms(token)
            if has_perms:
                user, error_msg = await get_current_user(token)
                kwargs["current_user"] = user
                result = await original_resolver(obj, info, **kwargs)
            else:
                return {
                    "error": error_msg
                }
            return result

        field.resolve = has_required_perms
        return field
