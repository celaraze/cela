import os
import yaml
from rich import print

from client.util import trans

CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), '.cela', 'config.yml')


def remove():
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)
        print("Config file removed.")
    else:
        print("Config file not found.")
        exit(1)


def create_if_not_exist():
    dir_path = os.path.dirname(CONFIG_FILE_PATH)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    if not os.path.exists(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, "w") as f:
            yaml.dump({}, f)


def read(key: str = None):
    if not os.path.exists(CONFIG_FILE_PATH):
        print("Config file not found.")
        exit(1)
    try:
        with open(CONFIG_FILE_PATH, "r") as f:
            content = yaml.safe_load(f)
        if key:
            return content[key]
        return content
    except yaml.YAMLError:
        return {}
    except KeyError:
        raise


def write(key_values: dict):
    create_if_not_exist()
    content = read()
    for key, value in key_values.items():
        content[key] = value
    with open(CONFIG_FILE_PATH, "w") as f:
        yaml.dump(content, f)


def read_server_url():
    try:
        return read("server_url")
    except KeyError:
        print("Server URL not found.")
        exit(1)


def read_access_token():
    try:
        return read("access_token")
    except KeyError:
        print("Access token not found.")
        exit(1)


def read_lang():
    try:
        return read("lang")
    except KeyError:
        return "en_US"
