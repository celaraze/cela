import httpx
from .config import read_server_url, read_access_token
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

from ..util import trans, calculate_todo_minutes

console = Console()


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

    todos = response.json()

    table = Table(show_header=True, header_style="bold green")
    table.add_column(trans("todo.columns.id"), style="dim", width=12)
    table.add_column(trans("todo.columns.title"))
    table.add_column(trans("todo.columns.priority"))

    for todo in todos:
        table.add_row(
            str(todo["id"]),
            todo["title"],
            str(todo["priority"]),
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

    console.print(trans("todo.show"), response.status_code, style="bold green")

    todo = response.json()
    minutes = todo['minutes']

    if todo:
        table = Table(show_header=True, header_style="bold")
        table.add_column(trans("table.fields"))
        table.add_column(trans("table.values"))
        table.add_row(trans("todo.columns.id"), str(todo['id']))
        table.add_row(trans("todo.columns.title"), todo['title'])
        table.add_row(trans("todo.columns.priority"), str(todo['priority']))
        table.add_row(trans("todo.columns.created_at"), todo['created_at'])
        if todo['creator']:
            table.add_row(trans("todo.columns.creator"), f"{todo['creator']['name']} ({todo['creator']['username']})")

        console.print(table)

        tree = Tree(f"⏱️ {trans('todo.minutes')}")

        minutes = calculate_todo_minutes(minutes)
        for index, minute in enumerate(minutes):
            render = f"{index + 1} {minute['start']} - {minute['end']}  {trans('todo.keeping')} {minute['diff']}"
            if minute['is_doing']:
                render += f" {trans('todo.doing')}"
            else:
                render += f" {trans('todo.done')}"
            tree.add(render)

        total_minutes = sum([minute['diff'].seconds // 60 for minute in minutes])

        console.print(f"{trans('todo.total_minutes')}: {total_minutes} {trans('todo.units.minutes')}")

        console.print(tree)


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


def start_work(todo_id: int):
    form_data = {
        "todo_id": todo_id,
    }
    response = httpx.post(
        f"{read_server_url()}/todos/{todo_id}/start_work",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=form_data,
    )
    if response.status_code != 200:
        console.print(trans("todo.start_work_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("todo.start_work"), response.status_code, style="bold green")


def end_work(todo_id: int):
    form_data = {
        "todo_id": todo_id,
    }
    response = httpx.post(
        f"{read_server_url()}/todos/{todo_id}/end_work",
        headers={"Authorization": f"Bearer {read_access_token()}"},
        json=form_data,
    )
    if response.status_code != 200:
        console.print(trans("todo.end_work_failed"), style="bold red")
        console.print(response.status_code)
        console.print(response.json()['detail'] or None, style="bold")
        exit(1)

    console.print(trans("todo.end_work"), response.status_code, style="bold green")
