import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

from ..util import trans

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
        console.print(trans("role.selects_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("role.list"), response.status_code, style="bold green")

    roles = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(trans("role.columns.id"), style="dim", width=12)
    table.add_column(trans("role.columns.name"))
    table.add_column(trans("role.columns.scopes"))

    for role in roles:
        table.add_row(
            str(role["id"]),
            role["name"],
            ", ".join(role["scopes"]),
        )

    console.print(table)


def select_role(role_id: int):
    response = httpx.get(
        f"{read_server_url()}/roles/{role_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("role.select_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("role.info"), response.status_code, style="bold green")

    role = response.json()

    if role:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(trans("table.fields"))
        table.add_column(trans("table.values"))
        table.add_row(trans("role.columns.id"), str(role['id']))
        table.add_row(trans("role.columns.name"), role['name'])
        table.add_row(trans("role.columns.scopes"), ", ".join(role['scopes']))
        table.add_row(trans("role.columns.created_at"), role['created_at'])
        if role['creator']:
            table.add_row(trans("role.columns.creator"), f"{role['creator']['name']} ({role['creator']['username']})")

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
        console.print(trans("role.create_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("role.create"), response.status_code, style="bold green")

    console.print(f"{trans('role.new_id')}{response.json()['id']}")


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
        console.print(trans("role.update_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("role.update"), response.status_code, style="bold green")


def delete_role(role_id: int):
    response = httpx.delete(
        f"{read_server_url()}/roles/{role_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print(trans("role.delete_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("role.delete"), response.status_code, style="bold green")
