import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

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
        console.print("Failed to get users.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print("Users", response.status_code, style="bold green")

    users = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12, justify="center")
    table.add_column("Name", justify="center")
    table.add_column("Username", justify="center")
    table.add_column("E-mail", justify="center")
    table.add_column("Is Active", justify="center")

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
        console.print("Failed to get user.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print("User", response.status_code, style="bold green")

    user = response.json()

    if user:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Fields")
        table.add_column("Values", justify="right")
        table.add_row("ID", str(user['id']))
        table.add_row("Name", user['name'])
        table.add_row("Username", user['username'])
        table.add_row("E-mail", user['email'])
        table.add_row("Is Active", str(user['is_active']))
        table.add_row("Created At", user['created_at'])
        if user['creator']:
            table.add_row("Creator", f"{user['creator']['name']} ({user['creator']['username']})")
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
        console.print("Failed to create user.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print("User Create", response.status_code, style="bold green")

    console.print(f"The new user id: {response.json()['id']}")


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
        console.print("Failed to update user.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print("User Update", response.status_code, style="bold green")


def delete_user(user_id: int):
    response = httpx.delete(
        f"{read_server_url()}/users/{user_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print("Failed to delete user.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print("User Delete", response.status_code, style="bold green")
