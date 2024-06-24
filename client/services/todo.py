import httpx
import fire
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table

from ..util import trans

console = Console()


def switch(args):
    print(args)
    if len(args) < 3:
        select_todos()
        return
    if args[2] == "create":
        create_todo(args[3], args[4])
    elif args[2] == "update":
        update_todo(args[3], args[4], args[5])
    elif args[2] == "delete":
        delete_todo(args[3])
    else:
        select_todo(args[2])


def select_todos():
    response = httpx.get(
        f"{read_server_url()}/todos/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("todo.selects_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("todo.list"), response.status_code, style="bold green")

    roles = response.json()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column(trans("todo.columns.id"), style="dim", width=12)
    table.add_column(trans("todo.columns.title"))
    table.add_column(trans("role.columns.priority"))

    for role in roles:
        table.add_row(
            str(role["id"]),
            role["title"],
            str(role["priority"]),
        )

    console.print(table)


def select_todo(todo_id: int):
    response = httpx.get(
        f"{read_server_url()}/todos/{todo_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )
    if response.status_code != 200:
        console.print(trans("todo.select_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("todo.info"), response.status_code, style="bold green")

    todo = response.json()

    if todo:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(trans("table.fields"))
        table.add_column(trans("table.values"))
        table.add_row(trans("todo.columns.id"), str(todo['id']))
        table.add_row(trans("todo.columns.title"), todo['title'])
        table.add_row(trans("todo.columns.priority"), str(todo['priority']))
        table.add_row(trans("todo.columns.created_at"), todo['created_at'])
        if todo['creator']:
            table.add_row(trans("role.columns.creator"), f"{todo['creator']['name']} ({todo['creator']['username']})")

        console.print(table)


def create_todo(title: str, priority: int = 0):
    create_form = {
        "title": title,
        "priority": priority,
    }
    response = httpx.post(
        f"{read_server_url()}/todos/",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=create_form,
    )
    if response.status_code != 200:
        console.print(trans("todo.create_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("todo.create"), response.status_code, style="bold green")

    console.print(f"{trans('todo.new_id')}{response.json()['id']}")


def update_todo(todo_id: int, key: str, value: str):
    if value == "null":
        value = None
    update_form = [
        {
            "key": key,
            "value": value,
        }
    ]
    response = httpx.put(
        f"{read_server_url()}/todos/{todo_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=update_form,
    )
    if response.status_code != 200:
        console.print(trans("todo.update_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("todo.update"), response.status_code, style="bold green")


def delete_todo(todo_id: int):
    response = httpx.delete(
        f"{read_server_url()}/todos/{todo_id}",
        headers={"Authorization": f"Bearer {read_access_token()}"},
    )

    if response.status_code != 200:
        console.print(trans("todo.delete_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("todo.delete"), response.status_code, style="bold green")
