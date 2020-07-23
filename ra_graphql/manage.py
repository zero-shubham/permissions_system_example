import asyncio
import sys
from email_validator import validate_email
from utils.app_event_funcs import startup, shutdown
from crud.user import create_new_user
from crud.group import (
    add_new_group,
    get_user_group_by_name
)
from utils.funcs import random_string

_exception_msg = "\n Something went wrong, get hold of the developer! \n"


async def create_super_user():
    print("Enter SuperAdmin email: ")
    email = input()
    try:
        email = validate_email(email)["email"]
    except Exception as excep:
        print(excep, "\n Not a valid email.")
        return
    print("Enter SuperAdmin password: ")
    password = input()
    creation_success = await create_new_user(
        obj_in={
            "user_name": email,
            "group": "super_admin",
            "password": password
        }
    )

    if creation_success:
        print("\n *** Super Admin was successfully created. *** \n")
    else:
        print(_exception_msg)


async def add_client_group():
    print("Enter client group: (Info: `_client` will be suffixed to this)")
    client_group = input()
    client_group = f"{client_group}_client"
    try:
        await add_new_group(client_group)
        print("\n *** Client group added *** \n")
    except Exception as e:
        print(_exception_msg)


async def add_client_account():
    print("Enter client group: ")
    client_group = input()
    client_key = random_string()
    print("Enter client secret :")
    client_secret = input()

    try:
        group_exists = await get_user_group_by_name(client_group)
        if not group_exists:
            print("\n Client group does not exists.")
            return

        creation_success = await create_new_user(
            obj_in={
                "user_name": client_key,
                "group": client_group,
                "password": client_secret
            }
        )
    except Exception as e:
        print(_exception_msg)
    if creation_success:
        print(
            f"\n *** Client was successfully created. client key -> {client_key} *** \n")
    else:
        print(_exception_msg)


async def main():
    arguments = sys.argv
    await startup()
    if arguments[1] == "createsuperadmin":
        await create_super_user()
    elif arguments[1] == "addclientgroup":
        await add_client_group()
    elif arguments[1] == "createclient":
        await add_client_account()

    await shutdown()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_until_complete(asyncio.sleep(2.0))
    finally:
        loop.close()
