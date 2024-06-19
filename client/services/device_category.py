import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

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
        console.print("Failed to get device categories.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    device_categories = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Name")

    for device_category in device_categories:
        table.add_row(
            str(device_category["id"]),
            device_category["name"],
        )

    console.print("Device Categories", response.status_code, style="bold green")
    console.print(table)


def select_device_category(device_category_id: int):
    response = httpx.get(
        f"{read_server_url()}/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print("Failed to get device_category.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    device_category = response.json()

    console.print("Device Category", response.status_code, style="bold green")

    if device_category:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Fields")
        table.add_column("Values")
        table.add_row("ID", str(device_category['id']))
        table.add_row("Name", device_category['name'])
        table.add_row("Created At", device_category['created_at'])
        if device_category['creator']:
            table.add_row("Creator", f"{device_category['creator']['name']} ({device_category['creator']['username']})")

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
        console.print("Failed to create device category.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Device category created successfully.", style="bold green")
    console.print(f"The new device category id: {response.json()['id']}")


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
        console.print("Failed to update device category.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Device category updated successfully.", style="bold green")


def delete_device_category(device_category_id: int):
    response = httpx.delete(
        f"{read_server_url()}/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print("Failed to delete device category.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Device category deleted successfully.", style="bold green")
