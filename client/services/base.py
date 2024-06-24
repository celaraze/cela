import httpx
from pick import pick

from client.services import config, auth

from client.util import trans


def connect(server_url: str):
    config.create_if_not_exist()
    print(trans("connecting"))
    response = httpx.get(f"{server_url}/auth/init")
    if response.status_code not in [200, 409]:
        print(trans("connect_failed"))
        return
    config.write({"server_url": server_url})
    print(trans("connect_success"))


def login(username: str, password: str):
    print(trans("logging_in"))
    response = auth.login(config.read_server_url(), username, password)
    if response.status_code != 200:
        print(response.json()["detail"] or None, response.status_code)
        return
    access_token = response.json()["access_token"]
    config.write({"access_token": access_token})
    print(trans("login_success"))


def switch_lang():
    options = ['en_US', 'zh_CN']
    selected = pick(options, trans("switch_languages"))
    config.write({"lang": selected[0]})
    print(trans("switch_lang_success"))


def remove():
    config.remove()
