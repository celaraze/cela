import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

from ..util import trans

console = Console()


def switch(args):
    if args.action == "list":
        select_users()
    if args.action == "info":
        select_user(args.user_id)
    if args.action == "create":
        create_user(args)
    if args.action == "update":
        update_user(args.user_id, args.key, args.value)
    if args.action == "delete":
        delete_user(args.user_id)


def select_users():
    response = httpx.get(
        f"{read_server_url()}/users/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("user.selects_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("user.list"), response.status_code, style="bold green")

    users = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(trans("user.columns.id"), style="dim", width=12, justify="center")
    table.add_column(trans("user.columns.name"), justify="center")
    table.add_column(trans("user.columns.username"), justify="center")
    table.add_column(trans("user.columns.email"), justify="center")
    table.add_column(trans("user.columns.is_active"), justify="center")

    for user in users:
        table.add_row(
            str(user["id"]),
            user["name"],
            user["username"],
            user["email"],
            str(user["is_active"]),
        )

    console.print(table)


def select_user(user_id: int):
    response = httpx.get(
        f"{read_server_url()}/users/{user_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("user.select_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("user.info"), response.status_code, style="bold green")

    user = response.json()

    if user:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(trans("table.fields"))
        table.add_column(trans("table.values"), justify="right")
        table.add_row(trans("user.columns.id"), str(user['id']))
        table.add_row(trans("user.columns.name"), user['name'])
        table.add_row(trans("user.columns.username"), user['username'])
        table.add_row(trans("user.columns.email"), user['email'])
        table.add_row(trans("user.columns.is_active"), str(user['is_active']))
        table.add_row(trans("user.columns.created_at"), user['created_at'])
        if user['creator']:
            table.add_row(trans("user.columns.creator"), f"{user['creator']['name']} ({user['creator']['username']})")
        console.print(table)


def create_user(args):
    create_form = {
        "name": args.name,
        "username": args.username,
        "email": args.email,
        "password": args.password,
    }
    response = httpx.post(
        f"{read_server_url()}/users/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=create_form,
    )
    if response.status_code != 200:
        console.print(trans("user.create_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("user.create"), response.status_code, style="bold green")

    console.print(f"{trans('user.new_id')}{response.json()['id']}")


def update_user(user_id: int, key: str, value: str):
    if value == "null":
        value = None
    update_form = [
        {
            "key": key,
            "value": value,
        }
    ]
    response = httpx.put(
        f"{read_server_url()}/users/{user_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=update_form,
    )
    if response.status_code != 200:
        console.print(trans("user.update_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("user.update"), response.status_code, style="bold green")


def delete_user(user_id: int):
    response = httpx.delete(
        f"{read_server_url()}/users/{user_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print(trans("user.delete_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("user.delete"), response.status_code, style="bold green")
