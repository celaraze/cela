import argparse

from rich import print
import httpx
from .services import config, auth, role, brand, device_category, device


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

    # cela <command>
    subparsers = parser.add_subparsers(dest='command')

    # cela connect <server_url>
    connect_parser = subparsers.add_parser('connect')
    connect_parser.add_argument('server_url', type=str, help='The URL of the CELA server.')

    # cela remove
    connect_parser = subparsers.add_parser('remove')

    # cela login <username> <password>
    login_parser = subparsers.add_parser('login')
    login_parser.add_argument('username', type=str, help='Username of the user.')
    login_parser.add_argument('password', type=str, help='Password of the user.')

    # cela role <action>
    role_parser = subparsers.add_parser('role')
    role_action_subparsers = role_parser.add_subparsers(dest='action', required=True)

    # cela role list
    role_list_subparser = role_action_subparsers.add_parser('list')

    # cela role info <role_id>
    role_info_subparser = role_action_subparsers.add_parser('info')
    role_info_subparser.add_argument('role_id', type=int, help='ID of the role.')

    # cela role create <name> <scopes>
    role_create_subparser = role_action_subparsers.add_parser('create')
    role_create_subparser.add_argument('--name', type=str, help='Name of the role.')
    role_create_subparser.add_argument('--scopes', type=str, help='Scopes of the role.')

    # cela role update <role_id> <key> <value>
    role_update_subparser = role_action_subparsers.add_parser('update')
    role_update_subparser.add_argument('role_id', type=int, help='ID of the role.')
    role_update_subparser.add_argument('key', type=str, help='Key of the role.')
    role_update_subparser.add_argument('value', type=str, help='Value of the role.')

    # cela role delete <role_id>
    role_delete_subparser = role_action_subparsers.add_parser('delete')
    role_delete_subparser.add_argument('role_id', type=int, help='ID of the role.')

    # cela brand <action>
    brand_parser = subparsers.add_parser('brand')
    brand_action_subparsers = brand_parser.add_subparsers(dest='action', required=True)

    # cela brand list
    brand_list_subparser = brand_action_subparsers.add_parser('list')

    # cela brand info
    brand_info_subparser = brand_action_subparsers.add_parser('info')
    # cela brand info <brand_id>
    brand_info_subparser.add_argument('brand_id', type=int, help='ID of the brand.')

    # cela brand create <name>
    brand_create_subparser = brand_action_subparsers.add_parser('create')
    brand_create_subparser.add_argument('--name', type=str, help='Name of the brand.')

    # cela brand update <brand_id> <key> <value>
    brand_update_subparser = brand_action_subparsers.add_parser('update')
    brand_update_subparser.add_argument('brand_id', type=int, help='ID of the brand.')
    brand_update_subparser.add_argument('key', type=str, help='Key of the brand.')
    brand_update_subparser.add_argument('value', type=str, help='Value of the brand.')

    # cela brand delete <brand_id>
    brand_delete_subparser = brand_action_subparsers.add_parser('delete')
    brand_delete_subparser.add_argument('brand_id', type=int, help='ID of the brand.')

    # cela device_category <action>
    device_category_parser = subparsers.add_parser('device_category')
    device_category_action_subparsers = device_category_parser.add_subparsers(dest='action', required=True)

    # cela device_category list
    device_category_list_subparser = device_category_action_subparsers.add_parser('list')

    # cela device_category info <device_category_id>
    device_category_info_subparser = device_category_action_subparsers.add_parser('info')
    device_category_info_subparser.add_argument('device_category_id', type=int, help='ID of the device category.')

    # cela device_category create <name> <scopes>
    device_category_create_subparser = device_category_action_subparsers.add_parser('create')
    device_category_create_subparser.add_argument('--name', type=str, help='Name of the device category.')

    # cela device_category update <device_category_id> <key> <value>
    device_category_update_subparser = device_category_action_subparsers.add_parser('update')
    device_category_update_subparser.add_argument('device_category_id', type=int, help='ID of the device category.')
    device_category_update_subparser.add_argument('key', type=str, help='Key of the device category.')
    device_category_update_subparser.add_argument('value', type=str, help='Value of the device category.')

    # cela device_category delete <device_category_id>
    device_category_delete_subparser = device_category_action_subparsers.add_parser('delete')
    device_category_delete_subparser.add_argument('device_category_id', type=int, help='ID of the device category.')

    # cela device <action>
    device_parser = subparsers.add_parser('device')
    device_action_subparsers = device_parser.add_subparsers(dest='action', required=True)

    # cela device list
    device_list_subparser = device_action_subparsers.add_parser('list')

    # cela device info
    device_info_subparser = device_action_subparsers.add_parser('info')
    # cela device info <device_id>
    device_info_subparser.add_argument('device_id', type=int, help='ID of the device.')

    # cela device create <name>
    device_create_subparser = device_action_subparsers.add_parser('create')
    device_create_subparser.add_argument('--hostname', type=str, help='Name of the device.')
    device_create_subparser.add_argument('--asset-number', type=str, help='Name of the device.')
    device_create_subparser.add_argument('--ipv4-address', type=str, help='Name of the device.')
    device_create_subparser.add_argument('--ipv6-address', type=str, help='Name of the device.')
    device_create_subparser.add_argument('--mac-address', type=str, help='Name of the device.')
    device_create_subparser.add_argument('--description', type=str, help='Name of the device.')
    device_create_subparser.add_argument('--brand-id', type=str, help='Name of the device.')
    device_create_subparser.add_argument('--category-id', type=str, help='Name of the device.')

    # cela device update <device_id> <key> <value>
    device_update_subparser = device_action_subparsers.add_parser('update')
    device_update_subparser.add_argument('device_id', type=int, help='ID of the device.')
    device_update_subparser.add_argument('key', type=str, help='Key of the device.')
    device_update_subparser.add_argument('value', type=str, help='Value of the device.')

    # cela device delete <device_id>
    brand_delete_subparser = device_action_subparsers.add_parser('delete')
    brand_delete_subparser.add_argument('device_id', type=int, help='ID of the device.')

    args = parser.parse_args()

    if args.command == 'connect':
        connect(args.server_url)
    elif args.command == 'login':
        login(args.username, args.password)
    elif args.command == 'remove':
        remove()
    elif args.command == 'role':
        role.switch(args)
    elif args.command == 'brand':
        brand.switch(args)
    elif args.command == 'device_category':
        device_category.switch(args)
    elif args.command == 'device':
        device.switch(args)
    else:
        print("Invalid command. Please follow the usage below.")
        print("Usage: cela <command>")


if __name__ == '__main__':
    main()
