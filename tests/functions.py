from typing import Union

from fastapi.testclient import TestClient
from sqlalchemy import MetaData

from app.database.database import SessionLocal, engine
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


# Auth

def login(username: str, password: str):
    return client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password
        }
    )


def renew(access_token: str):
    return client.post(
        "/auth/renew",
        headers={"Authorization": f"Bearer {access_token}"}
    )


def select_me(access_token: str):
    return client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"}
    )


def update_me(access_token: str, update_form: list[dict]):
    return client.put(
        "/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_form
    )


def update_me_change_password(access_token: str, old_password: str, new_password: str):
    return client.put(
        "/auth/change_password",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"old_password": old_password, "new_password": new_password}
    )


# User

def select_user(access_token: str, user_id: id):
    return client.get(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_users(access_token: str):
    return client.get(
        f"/users",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_user(access_token: str, form_data: dict):
    return client.post(
        f"/users",
        json=form_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_user(access_token: str, user_id: id, update_form: list[dict]):
    return client.put(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=update_form
    )


def delete_user(access_token: str, user_id: id):
    return client.delete(
        f"/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


# Role

def select_role(access_token: str, role_id: id):
    return client.get(
        f"/roles/{role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_roles(access_token: str):
    return client.get(
        f"/roles",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_role(access_token: str, form_data: dict):
    return client.post(
        f"/roles",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def update_role(access_token: str, role_id: id, form_data: list[dict]):
    return client.put(
        f"/roles/{role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_role(access_token: str, role_id: id):
    return client.delete(
        f"/roles/{role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


# UserHasRole

def select_user_roles(access_token: str, user_id: id):
    return client.get(
        f"/users/{user_id}/roles",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_user_historical_roles(access_token: str, user_id: id):
    return client.get(
        f"/users/{user_id}/roles/historical",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_user_has_role(access_token: str, user_id: id, form_data: dict):
    return client.post(
        f"/users/{user_id}/roles",
        json=form_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def delete_user_has_role(access_token: str, user_id: id, role_id: id):
    return client.delete(
        f"/users/{user_id}/roles/{role_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


# Brand

def create_brand(access_token: str, form_data: dict):
    return client.post(
        f"/brands",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def select_brands(access_token: str):
    return client.get(
        f"/brands",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_brand(access_token: str, brand_id: id):
    return client.get(
        f"/brands/{brand_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_brand(access_token: str, brand_id: id, form_data: list[dict]):
    return client.put(
        f"/brands/{brand_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_brand(access_token: str, brand_id: id):
    return client.delete(
        f"/brands/{brand_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_brand_devices(access_token: str, brand_id: id):
    return client.get(
        f"/brands/{brand_id}/devices",
        headers={"Authorization": f"Bearer {access_token}"},
    )


# DeviceCategory

def create_device_category(access_token: str, form_data: dict):
    return client.post(
        f"/device_categories",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def select_device_categories(access_token: str):
    return client.get(
        f"/device_categories",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_device_category(access_token: str, device_category_id: id):
    return client.get(
        f"/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_device_category(access_token: str, device_category_id: id, form_data: list[dict]):
    return client.put(
        f"/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_device_category(access_token: str, device_category_id: id):
    return client.delete(
        f"/device_categories/{device_category_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_device_category_devices(access_token: str, device_category_id: id):
    return client.get(
        f"/device_categories/{device_category_id}/devices",
        headers={"Authorization": f"Bearer {access_token}"},
    )


# Device

def create_device(access_token: str, form_data: dict):
    return client.post(
        f"/devices",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def select_devices(access_token: str, asset_number: Union[str, None] = None):
    query = ""
    if asset_number:
        query = f"asset_number={asset_number}"
    return client.get(
        f"/devices?" + query,
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_device(access_token: str, device_id: id):
    return client.get(
        f"/devices/{device_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def update_device(access_token: str, device_id: id, form_data: list[dict]):
    return client.put(
        f"/devices/{device_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_device(access_token: str, device_id: id):
    return client.delete(
        f"/devices/{device_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


# UserHasDevice

def select_user_devices(access_token: str, user_id: id):
    return client.get(
        f"/users/{user_id}/devices",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_user_historical_devices(access_token: str, user_id: id):
    return client.get(
        f"/users/{user_id}/devices/historical",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def user_has_device_out(access_token: str, user_id: id, form_data: dict):
    return client.post(
        f"/users/{user_id}/devices/out",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def user_has_device_in(access_token: str, user_id: id, form_data: dict):
    return client.post(
        f"/users/{user_id}/devices/in",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data,
    )


def search_asset_numbers(access_token: str, asset_number: str):
    return client.get(
        f"/search/assets/asset_number/{asset_number}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def search_tickets(access_token: str, keyword: str):
    return client.get(
        f"/search/tickets/title/{keyword}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_tickets(access_token: str):
    return client.get(
        f"/tickets",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_ticket(access_token: str, ticket_id: id):
    return client.get(
        f"/tickets/{ticket_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_ticket(access_token: str, form_data: dict):
    return client.post(
        f"/tickets",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def update_ticket(access_token: str, ticket_id: id, form_data: list[dict]):
    return client.put(
        f"/tickets/{ticket_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_ticket(access_token: str, ticket_id: id):
    return client.delete(
        f"/tickets/{ticket_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_ticket_comment(access_token: str, ticket_id: id, form_data: dict):
    return client.post(
        f"/tickets/{ticket_id}/comments",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def start_work_on_ticket(access_token: str, ticket_id: id, form_data: dict):
    return client.post(
        f"/tickets/{ticket_id}/start_work",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data,
    )


def end_work_on_ticket(access_token: str, ticket_id: id, form_data: dict):
    return client.post(
        f"/tickets/{ticket_id}/end_work",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def select_todos(access_token: str):
    return client.get(
        f"/todos",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def select_todo(access_token: str, todo_id: id):
    return client.get(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def create_todo(access_token: str, form_data: dict):
    return client.post(
        f"/todos",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def update_todo(access_token: str, todo_id: id, form_data: list[dict]):
    return client.put(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data
    )


def delete_todo(access_token: str, todo_id: id):
    return client.delete(
        f"/todos/{todo_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )


def start_work_on_todo(access_token: str, todo_id: id, form_data: dict):
    return client.post(
        f"/todos/{todo_id}/start_work",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data,
    )


def end_work_on_todo(access_token: str, todo_id: id, form_data: dict):
    return client.post(
        f"/todos/{todo_id}/end_work",
        headers={"Authorization": f"Bearer {access_token}"},
        json=form_data,
    )
