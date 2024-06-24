import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

from ..util import trans

console = Console()


def switch(args):
    if args.action == "list":
        select_devices()
    if args.action == "info":
        select_device(args.device_id)
    if args.action == "create":
        create_device(args)
    if args.action == "update":
        update_device(args.device_id, args.key, args.value)
    if args.action == "delete":
        delete_device(args.device_id)


def select_devices():
    response = httpx.get(
        f"{read_server_url()}/devices/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("device.select_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device.list"), response.status_code, style="bold green")

    devices = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(trans("device.columns.id"), style="dim", width=12, justify="center")
    table.add_column(trans("device.columns.hostname"), justify="center")
    table.add_column(trans("device.columns.asset_number"), justify="center")
    table.add_column(trans("device.columns.ipv4_address"), justify="center")
    table.add_column(trans("device.columns.mac_address"), justify="center")

    for device in devices:
        table.add_row(
            str(device["id"]),
            device["hostname"],
            device["asset_number"],
            device["ipv4_address"],
            device["mac_address"],
        )

    console.print(table)


def select_device(device_id: int):
    response = httpx.get(
        f"{read_server_url()}/devices/{device_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("device.select_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device.info"), response.status_code, style="bold green")

    device = response.json()

    if device:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(trans("table.fields"))
        table.add_column(trans("table.values"), justify="right")
        table.add_row(trans("device.columns.id"), str(device['id']))
        table.add_row(trans("device.columns.hostname"), device['hostname'])
        table.add_row(trans("device.columns.ipv4_address"), device['ipv4_address'])
        table.add_row(trans("device.columns.ipv6_address"), device['ipv6_address'])
        table.add_row(trans("device.columns.mac_address"), device['mac_address'])
        table.add_row(trans("device.columns.description"), device['description'])
        table.add_row(trans("device.columns.created_at"), device['created_at'])
        if device['creator']:
            table.add_row(trans("device.columns.creator"),
                          f"{device['creator']['name']} ({device['creator']['username']})")
        console.print(table)


def create_device(args):
    create_form = {
        "hostname": args.hostname,
        "asset_number": args.asset_number,
        "ipv4_address": args.ipv4_address,
        "ipv6_address": args.ipv6_address,
        "mac_address": args.mac_address,
        "description": args.description,
        "brand_id": args.brand_id,
        "category_id": args.category_id,
    }
    response = httpx.post(
        f"{read_server_url()}/devices/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=create_form,
    )
    if response.status_code != 200:
        console.print(trans("device.create_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device.create"), response.status_code, style="bold green")

    console.print(f"{trans('device.new_id')}{response.json()['id']}")


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
        f"{read_server_url()}/devices/{role_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=update_form,
    )
    if response.status_code != 200:
        console.print(trans("device.update_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device.update"), response.status_code, style="bold green")


def delete_device(role_id: int):
    response = httpx.delete(
        f"{read_server_url()}/devices/{role_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print(trans("device.delete_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("device.delete"), response.status_code, style="bold green")
