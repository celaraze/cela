import argparse

from rich import print
import httpx
from .services import config, auth, role


def connect(server_url: str):
    print("Connecting to the server...")
    response = httpx.get(f"{server_url}/auth/init")
    if response.status_code not in [200, 409]:
        print("Failed to connect to the server.")
        return
    config.write({"server_url": server_url})
    print("Connected to the server successfully.")


def login(username: str, password: str):
    print("Logging in...")
    response = auth.login(config.read_server_url(), username, password)
    if response.status_code != 200:
        print("Failed to login.")
        return
    access_token = response.json()["access_token"]
    config.write({"access_token": access_token})
    print("Logged in successfully.")


def remove():
    config.remove()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    connect_parser = subparsers.add_parser('connect')
    connect_parser.add_argument('server_url', type=str, help='The URL of the CELA server.')

    connect_parser = subparsers.add_parser('remove')

    login_parser = subparsers.add_parser('login')
    login_parser.add_argument('username', type=str, help='Username of the user.')
    login_parser.add_argument('password', type=str, help='Password of the user.')

    role_parser = subparsers.add_parser('role')
    role_action_subparsers = role_parser.add_subparsers(dest='action')
    role_list_subparser = role_action_subparsers.add_parser('list')
    role_info_subparser = role_action_subparsers.add_parser('info')
    role_info_subparser.add_argument('role_id', type=int, help='ID of the role.')
    role_create_subparser = role_action_subparsers.add_parser('create')
    role_create_subparser.add_argument('name', type=str, help='Name of the role.')
    role_create_subparser.add_argument('scopes', type=str, nargs='+', help='Scopes of the role.')
    role_update_subparser = role_action_subparsers.add_parser('update')
    role_update_subparser.add_argument('role_id', type=int, help='ID of the role.')
    role_update_subparser.add_argument('key', type=str, help='Key of the role.')
    role_update_subparser.add_argument('value', type=str, help='Value of the role.')
    role_delete_subparser = role_action_subparsers.add_parser('delete')
    role_delete_subparser.add_argument('role_id', type=int, help='ID of the role.')

    args = parser.parse_args()

    if args.command == 'connect':
        connect(args.server_url)
    elif args.command == 'login':
        login(args.username, args.password)
    elif args.command == 'remove':
        remove()
    elif args.command == 'role':
        role.switch(args)
    else:
        print("Invalid command. Please follow the usage below.")
        print("Usage: cela <command>")


if __name__ == '__main__':
    main()
