import os
import yaml
from rich import print

CONFIG_FILE_PATH = os.path.join(os.path.expanduser('~'), '.cela', 'config.yml')


def remove():
    if os.path.exists(CONFIG_FILE_PATH):
        os.remove(CONFIG_FILE_PATH)
        print("Config file removed.")
    else:
        print("Config file not found.")


def read(key: str = None):
    if not os.path.exists(CONFIG_FILE_PATH):
        print("Failed to open config file. Please run `cela connect` first.")
        return
    with open(CONFIG_FILE_PATH, "r") as f:
        content = yaml.load(f, Loader=yaml.FullLoader)
    if key:
        return content[key]
    return content


def write(key_values: dict):
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
    return read("server_url")


def read_access_token():
    return read("access_token")
