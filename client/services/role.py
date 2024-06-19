import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

SERVER_URL = read_server_url()
ACCESS_TOKEN = read_access_token()

console = Console()


def switch(args):
    if args.action == "list":
        select_roles()
    if args.action == "info":
        select_role(args.role_id)
    if args.action == "create":
        create_role(args.name, args.scopes)
    if args.action == "update":
        update_role(args.role_id, args.key, args.value)
    if args.action == "delete":
        delete_role(args.role_id)


def select_roles():
    roles = []
    title_color = "bold red"
    response = httpx.get(
        f"{SERVER_URL}/roles/",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    if response.status_code == 200:
        title_color = "bold green"
        roles = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Name")
    table.add_column("Scopes")

    for role in roles:
        table.add_row(
            str(role["id"]),
            role["name"],
            ", ".join(role["scopes"]),
        )

    console.print("Roles", response.status_code, style=title_color)
    console.print(table)


def select_role(role_id: int):
    role = {}
    title_color = "bold red"
    response = httpx.get(
        f"{SERVER_URL}/roles/{role_id}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    if response.status_code == 200:
        title_color = "bold green"
        role = response.json()

    console.print("Role", response.status_code, style=title_color)

    if role:
        console.print(role['id'])
        console.print(role['name'])
        console.print(", ".join(role['scopes']))
        console.print(role['created_at'])

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Fields")
        table.add_column("Values")
        table.add_row("ID", str(role['id']))
        table.add_row("Name", role['name'])
        table.add_row("Scopes", ", ".join(role['scopes']))
        table.add_row("Created At", role['created_at'])
        table.add_row("Creator", f"{role['creator']['id']} {role['creator']['username']}")

        console.print(table)


def create_role(name: str, scopes: str):
    create_form = {
        "name": name,
        "scopes": scopes.split(","),
    }
    response = httpx.post(
        f"{SERVER_URL}/roles/",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=create_form,
    )
    if response.status_code == 200:
        console.print("Role created successfully.", style="bold green")
    else:
        console.print("Failed to create role.", style="bold red")


def update_role(role_id: int, key: str, value: str):
    if value == "null":
        value = None
    update_form = [
        {
            "key": key,
            "value": value,
        }
    ]
    response = httpx.put(
        f"{SERVER_URL}/roles/{role_id}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=update_form,
    )
    if response.status_code == 200:
        console.print("Role updated successfully.", style="bold green")
    else:
        console.print("Failed to update role.", style="bold red")


def delete_role(role_id):
    response = httpx.delete(
        f"{SERVER_URL}/roles/{role_id}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    if response.status_code == 200:
        console.print("Role deleted successfully.", style="bold green")
    else:
        console.print("Failed to delete role.", style="bold red")
