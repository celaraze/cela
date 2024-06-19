import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

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
        console.print("Failed to get brands.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    brands = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Name")

    for brand in brands:
        table.add_row(
            str(brand["id"]),
            brand["name"],
        )

    console.print("Brands", response.status_code, style="bold green")
    console.print(table)


def select_brand(brand_id: int):
    response = httpx.get(
        f"{read_server_url()}/brands/{brand_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print("Failed to get brand.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    brand = response.json()

    console.print("Role", response.status_code, style="bold green")

    if brand:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Fields")
        table.add_column("Values")
        table.add_row("ID", str(brand['id']))
        table.add_row("Name", brand['name'])
        table.add_row("Created At", brand['created_at'])
        if brand['creator']:
            table.add_row("Creator", f"{brand['creator']['name']} ({brand['creator']['username']})")

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
        console.print("Failed to create brand.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Brand created successfully.", style="bold green")
    console.print(f"The new brand id: {response.json()['id']}")


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
        console.print("Failed to update brand.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Brand updated successfully.", style="bold green")


def delete_brand(brand_id: int):
    response = httpx.delete(
        f"{read_server_url()}/brand/{brand_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print("Failed to delete brand.", style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'], style="bold")
        return

    console.print("Brand deleted successfully.", style="bold green")
