import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

SERVER_URL = read_server_url()
ACCESS_TOKEN = read_access_token()

console = Console()


def switch(args):
    if args.action == "list":
        select_devices()
    if args.action == "info":
        select_device(args.device_id)
    if args.action == "create":
        create_device(args.name)
    if args.action == "update":
        update_device(args.device_id, args.key, args.value)
    if args.action == "delete":
        delete_device(args.device_id)


def select_devices():
    response = httpx.get(
        f"{SERVER_URL}/devices/",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    if response.status_code != 200:
        console.print("Failed to get devices.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    devices = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Name")

    for device in devices:
        table.add_row(
            str(device["id"]),
            device["name"],
        )

    console.print("Devices", response.status_code, style="bold green")
    console.print(table)


def select_device(device_id: int):
    response = httpx.get(
        f"{SERVER_URL}/devices/{device_id}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    if response.status_code != 200:
        console.print("Failed to get device.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    device = response.json()

    console.print("Role", response.status_code, style="bold green")

    if device:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Fields")
        table.add_column("Values")
        table.add_row("ID", str(device['id']))
        table.add_row("Name", device['name'])
        table.add_row("Created At", device['created_at'])
        if device['creator']:
            table.add_row("Creator", f"{device['creator']['name']} ({device['creator']['username']})")

        console.print(table)


def create_device(name: str):
    create_form = {
        "name": name,
    }
    response = httpx.post(
        f"{SERVER_URL}/devices/",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=create_form,
    )
    if response.status_code != 200:
        console.print("Failed to create device.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Device created successfully.", style="bold green")
    console.print(f"The new device id: {response.json()['id']}")


def update_device(role_id: int, key: str, value: str):
    if value == "null":
        value = None
    update_form = [
        {
            "key": key,
            "value": value,
        }
    ]
    response = httpx.put(
        f"{SERVER_URL}/devices/{role_id}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        json=update_form,
    )
    if response.status_code != 200:
        console.print("Failed to update device.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Device updated successfully.", style="bold green")


def delete_device(role_id: int):
    response = httpx.delete(
        f"{SERVER_URL}/devices/{role_id}",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )

    if response.status_code != 200:
        console.print("Failed to delete device.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Device deleted successfully.", style="bold green")
