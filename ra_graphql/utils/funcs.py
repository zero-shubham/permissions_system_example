import random
import string
from jwt import PyJWTError, ExpiredSignatureError
import jwt
from pydantic import BaseModel
from core.config import SECRET_KEY
from core.jwt import ALGORITHM
from crud.user import find_user_by_id
from crud.token import check_token_in_db
from permissions_system.constants import PermissionTypesEnum
from application import ps


class Token(BaseModel):
    user_id: str
    group: str
    exp: int
    sub: str


class TokenPayload(BaseModel):
    user_id: str
    group: str


def random_string():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(16))


def extract_token_from_context(context):
    headers = context["request"].headers
    token = headers.get("authorization").replace("Bearer ", "")
    return token


async def get_current_user(token: str):
    error_msg = None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = Token(**payload)

    except PyJWTError as e:
        if type(e) is ExpiredSignatureError:
            error_msg = "Token expired"
            return (None, error_msg)
        else:
            error_msg = "Could not validate credentials"
            return (None, error_msg)

    token_is_valid = await check_token_in_db(token_data.user_id, token)
    if not token_is_valid:
        error_msg = "Could not validate credentials"
        return (None, error_msg)
    user = await find_user_by_id(user_id=token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return (user, error_msg)


class UserHasResourcePermission:

    def __init__(
        self,
        resource: str,
        permission_type: PermissionTypesEnum
    ):
        self.resource = resource
        self.permission_type = permission_type

    async def __call__(self, token: str):
        result = None
        error_msg = None
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            token_data = Token(**payload)

        except PyJWTError as e:
            if type(e) is ExpiredSignatureError:
                error_msg = "Token expired"
            else:
                error_msg = "Could not validate credentials"
            return (None, error_msg)

        token_is_valid = await check_token_in_db(token_data.user_id, token)
        if not token_is_valid:
            error_msg = "Could not validate credentials"
            return (None, error_msg)
        try:
            result = ps.user_has_permissions(
                token_data.user_id, self.resource, self.permission_type)

        except AttributeError as e:
            error_msg = "Required permissions not found."
            return (None, error_msg)
        finally:
            if not result:
                error_msg = "Required permissions not found."
                return (None, error_msg)
        return (result, error_msg)
