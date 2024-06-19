import httpx


def login(server_url: str, username: str, password: str):
    return httpx.post(
        f"{server_url}/auth/login",
        data={
            "username": username,
            "password": password,
        }
    )
