import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

from ..util import trans

console = Console()


def switch(args):
    if args.action == "list":
        select_brands()
    if args.action == "info":
        select_brand(args.brand_id)
    if args.action == "create":
        create_brand(args.name)
    if args.action == "update":
        update_brand(args.brand_id, args.key, args.value)
    if args.action == "delete":
        delete_brand(args.brand_id)


def select_brands():
    response = httpx.get(
        f"{read_server_url()}/brands/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("brand.selects_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("brand.list"), response.status_code, style="bold green")

    brands = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(trans("brand.columns.id"), style="dim", width=12)
    table.add_column(trans("brand.columns.name"))

    for brand in brands:
        table.add_row(
            str(brand["id"]),
            brand["name"],
        )

    console.print(table)


def select_brand(brand_id: int):
    response = httpx.get(
        f"{read_server_url()}/brands/{brand_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("brand.select_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("brand.info"), response.status_code, style="bold green")

    brand = response.json()

    if brand:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(trans("table.fields"))
        table.add_column(trans("table.values"))
        table.add_row(trans("brand.columns.id"), str(brand['id']))
        table.add_row(trans("brand.columns.name"), brand['name'])
        table.add_row(trans("brand.columns.created_at"), brand['created_at'])
        if brand['creator']:
            table.add_row(trans("brand.columns.creator"),
                          f"{brand['creator']['name']} ({brand['creator']['username']})")

        console.print(table)


def create_brand(name: str):
    create_form = {
        "name": name,
    }
    response = httpx.post(
        f"{read_server_url()}/brands/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=create_form,
    )
    if response.status_code != 200:
        console.print(trans("brand.create_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("brand.create"), response.status_code, style="bold green")

    console.print(f"{trans('brand.new_id')}{response.json()['id']}")


def update_brand(brand_id: int, key: str, value: str):
    if value == "null":
        value = None
    update_form = [
        {
            "key": key,
            "value": value,
        }
    ]
    response = httpx.put(
        f"{read_server_url()}/brands/{brand_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=update_form,
    )
    if response.status_code != 200:
        console.print(trans("brand.update_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("brand.update"), response.status_code, style="bold green")


def delete_brand(brand_id: int):
    response = httpx.delete(
        f"{read_server_url()}/brand/{brand_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print(trans("brand.delete_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("brand.delete"), response.status_code, style="bold green")
