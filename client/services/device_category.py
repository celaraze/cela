import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

from ..util import trans

console = Console()


def switch(args):
    if args.action == "list":
        select_device_categories()
    if args.action == "info":
        select_device_category(args.device_category_id)
    if args.action == "create":
        create_device_category(args.name)
    if args.action == "update":
        update_device_category(args.device_category_id, args.key, args.value)
    if args.action == "delete":
        delete_device_category(args.device_category_id)


def select_device_categories():
    response = httpx.get(
        f"{read_server_url()}/device_categories/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("device_category.create_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device_category.list"), response.status_code, style="bold green")

    device_categories = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(trans("device_category.columns.id"), style="dim", width=12)
    table.add_column(trans("device_category.columns.name"))

    for device_category in device_categories:
        table.add_row(
            str(device_category["id"]),
            device_category["name"],
        )

    console.print(table)


def select_device_category(device_category_id: int):
    response = httpx.get(
        f"{read_server_url()}/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("device_category.select_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device_category.info"), response.status_code, style="bold green")

    device_category = response.json()

    if device_category:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(trans("table.fields"))
        table.add_column(trans("table.values"))
        table.add_row(trans("device_category.columns.id"), str(device_category['id']))
        table.add_row(trans("device_category.columns.name"), device_category['name'])
        table.add_row(trans("device_category.columns.created_at"), device_category['created_at'])
        if device_category['creator']:
            table.add_row(trans("device_category.columns.creator"),
                          f"{device_category['creator']['name']} ({device_category['creator']['username']})")

        console.print(table)


def create_device_category(name: str):
    create_form = {
        "name": name,
    }
    response = httpx.post(
        f"{read_server_url()}/device_categories/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=create_form,
    )
    if response.status_code != 200:
        console.print(trans("device_category.create_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device_category.create"), response.status_code, style="bold green")

    console.print(f"{trans('device_category.new_id')}{response.json()['id']}")


def update_device_category(device_category_id: int, key: str, value: str):
    if value == "null":
        value = None
    update_form = [
        {
            "key": key,
            "value": value,
        }
    ]
    response = httpx.put(
        f"{read_server_url()}/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=update_form,
    )
    if response.status_code != 200:
        console.print(trans("device_category.update_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device_category.update"), response.status_code, style="bold green")


def delete_device_category(device_category_id: int):
    response = httpx.delete(
        f"{read_server_url()}/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print(trans("device_category.delete_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device_category.delete"), response.status_code, style="bold green")
