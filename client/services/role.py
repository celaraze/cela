import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

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
    response = httpx.get(
        f"{read_server_url()}/roles/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print("Failed to get roles.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

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

    console.print("Roles", response.status_code, style="bold green")
    console.print(table)


def select_role(role_id: int):
    response = httpx.get(
        f"{read_server_url()}/roles/{role_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print("Failed to get role.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    role = response.json()

    console.print("Role", response.status_code, style="bold green")

    if role:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Fields")
        table.add_column("Values")
        table.add_row("ID", str(role['id']))
        table.add_row("Name", role['name'])
        table.add_row("Scopes", ", ".join(role['scopes']))
        table.add_row("Created At", role['created_at'])
        if role['creator']:
            table.add_row("Creator", f"{role['creator']['name']} ({role['creator']['username']})")

        console.print(table)


def create_role(name: str, scopes: str):
    create_form = {
        "name": name,
        "scopes": scopes.split(","),
    }
    response = httpx.post(
        f"{read_server_url()}/roles/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=create_form,
    )
    if response.status_code != 200:
        console.print("Failed to create role.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Role created successfully.", style="bold green")
    console.print(f"The new role id: {response.json()['id']}")


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
        f"{read_server_url()}/roles/{role_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=update_form,
    )
    if response.status_code != 200:
        console.print("Failed to update role.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Role updated successfully.", style="bold green")


def delete_role(role_id: int):
    response = httpx.delete(
        f"{read_server_url()}/roles/{role_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print("Failed to delete role.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Role deleted successfully.", style="bold green")
