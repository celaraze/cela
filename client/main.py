import fire
from .services import base, todo


class ConfigCommands:
    @staticmethod
    def connect(server_url: str):
        base.connect(server_url)

    @staticmethod
    def language():
        base.switch_lang()

    @staticmethod
    def remove():
        base.remove()


class AuthCommands:
    @staticmethod
    def login(username: str, password: str):
        base.login(username, password)


class TodoCommands:
    @staticmethod
    def list():
        todo.select_todos()

    @staticmethod
    def show(todo_id: int):
        todo.select_todo(todo_id)

    @staticmethod
    def create(title: str, priority: int = 0):
        todo.create_todo(title, priority)

    @staticmethod
    def update(todo_id: int, key: str, value: str):
        todo.update_todo(todo_id, key, value)

    @staticmethod
    def delete(todo_id: int):
        todo.delete_todo(todo_id)

    @staticmethod
    def start(todo_id: int):
        todo.start_work(todo_id)

    @staticmethod
    def end(todo_id: int):
        todo.end_work(todo_id)


if __name__ == '__main__':
    fire.Fire({
        'config': ConfigCommands,
        'auth': AuthCommands,
        'todo': TodoCommands,
    })
