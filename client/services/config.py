import os
import yaml
from rich import print

from client.util import trans

CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), '.cela', 'config.yml')


def remove():
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)
        print(trans("remove_config_success"))
    else:
        print(trans("remove_config_not_found"))


def read(key: str = None):
    if not os.path.exists(CONFIG_FILE_PATH):
        print(trans("config_not_found"))
        exit(1)
    with open(CONFIG_FILE_PATH, "r") as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
    if key:
        return content[key]
    return content


def write(key_values: dict):
    dir_path = os.path.dirname(CONFIG_FILE_PATH)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if not os.path.exists(CONFIG_FILE_PATH):
        content = {}
    else:
        content = read()

    # 更新配置
    for key, value in key_values.items():
        content[key] = value

    # 写回配置
    with open(CONFIG_FILE_PATH, "w") as f:
        yaml.dump(content, f)


def read_server_url():
    try:
        return read("server_url")
    except KeyError:
        print(trans("server_url_not_found"))
        exit(1)


def read_access_token():
    try:
        return read("access_token")
    except KeyError:
        print(trans("access_token_not_found"))
        exit(1)


def read_lang():
    try:
        return read("lang")
    except KeyError:
        return "en_US"
