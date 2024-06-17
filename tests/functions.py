from fastapi.testclient import TestClient
from httpx import Response

from app.config.database import SessionLocal, engine
from app.database import schemas, tables
from app.services import auth

from app.main import app

client = TestClient(app)


def start():
    db = SessionLocal()
    tables.Base.metadata.drop_all(bind=engine)
    tables.Base.metadata.create_all(bind=engine)
    db.close()


def end():
    db = SessionLocal()
    tables.Base.metadata.drop_all(bind=engine)
    db.close()


def create_admin(user: schemas.UserCreateForm):
    db = SessionLocal()
    user_create = schemas.UserCreateForm(
        email=user.email,
        name=user.name,
        password=user.password,
        username=user.username,
        creator_id=user.creator_id,
    )
    auth.create_super_admin(db, user_create)
    db.close()


def login(username: str, password: str) -> Response:
    return client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )


def renew(access_token: str) -> Response:
    return client.post(
        "/auth/renew",
        headers={"Authorization": f"Bearer {access_token}"}
    )


def select_me(access_token: str) -> Response:
    return client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )


def update_me(access_token: str, key: str, value: str) -> Response:
    return client.put(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"key": key, "value": value}
    )


def update_me_change_password(access_token: str, old_password: str, new_password: str) -> Response:
    return client.put(
        "/auth/change_password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"old_password": old_password, "new_password": new_password}
    )


def select_user(access_token: str, user_id: id) -> Response:
    return client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_users(access_token: str) -> Response:
    return client.get(
        f"/users",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_user(access_token: str, form_data: dict) -> Response:
    return client.post(
        f"/users",
        json=form_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_user(access_token: str, user_id: id, key: str, value: str) -> Response:
    return client.put(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"key": key, "value": value}
    )


def delete_user(access_token: str, user_id: id) -> Response:
    return client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_role(access_token: str, role_id: id) -> Response:
    return client.get(
        f"/roles/{role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_roles(access_token: str) -> Response:
    return client.get(
        f"/roles",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_role(access_token: str, form_data: dict) -> Response:
    return client.post(
        f"/roles",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def update_role(access_token: str, role_id: id, form_data: dict) -> Response:
    return client.put(
        f"/roles/{role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_role(access_token: str, role_id: id) -> Response:
    return client.delete(
        f"/roles/{role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_user_has_roles(access_token: str) -> Response:
    return client.get(
        f"/user_has_roles",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_user_has_role(access_token: str, user_has_role_id: id) -> Response:
    return client.get(
        f"/user_has_roles/{user_has_role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_user_has_role(access_token: str, form_data: dict) -> Response:
    return client.post(
        f"/user_has_roles",
        json=form_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def delete_user_has_role(access_token: str, user_has_role_id: id) -> Response:
    return client.delete(
        f"/user_has_roles/{user_has_role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def delete_user_has_role_by_user_id_and_role_id(access_token: str, user_id: id, role_id: id) -> Response:
    return client.delete(
        f"/user_has_roles/{user_id}/{role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_brand(access_token: str, form_data: dict) -> Response:
    return client.post(
        f"/brands",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def select_brands(access_token: str) -> Response:
    return client.get(
        f"/brands",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_brand(access_token: str, brand_id: id) -> Response:
    return client.get(
        f"/brands/{brand_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_brand(access_token: str, brand_id: id, form_data: dict) -> Response:
    return client.put(
        f"/brands/{brand_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_brand(access_token: str, brand_id: id) -> Response:
    return client.delete(
        f"/brands/{brand_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_device_category(access_token: str, form_data: dict) -> Response:
    return client.post(
        f"/device_categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def select_device_categories(access_token: str) -> Response:
    return client.get(
        f"/device_categories",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_device_category(access_token: str, device_category_id: id) -> Response:
    return client.get(
        f"/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_device_category(access_token: str, device_category_id: id, form_data: dict) -> Response:
    return client.put(
        f"/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_device_category(access_token: str, device_category_id: id) -> Response:
    return client.delete(
        f"/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_device(access_token: str, form_data: dict) -> Response:
    return client.post(
        f"/devices",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def select_devices(access_token: str, params: dict = None) -> Response:
    query = ""
    if params:
        query = "&".join([f"{key}={value}" for key, value in params.items()])
    return client.get(
        f"/devices?" + query,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_device(access_token: str, device_id: id) -> Response:
    return client.get(
        f"/devices/{device_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_device(access_token: str, device_id: id, form_data: dict) -> Response:
    return client.put(
        f"/devices/{device_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_device(access_token: str, device_id: id) -> Response:
    return client.delete(
        f"/devices/{device_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
