from fastapi.testclient import TestClient

from app.database import schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
user_id = 0
brand_id = 0
device_category_id = 0
device_id = 0
user_has_device_id = 0


def test_start():
    functions.start()

    global admin_access_token
    global user_id
    global brand_id
    global device_category_id
    global device_id

    form_data = schemas.UserCreateForm(
        email="test_admin@test.com",
        name="test_admin",
        password="test_admin",
        username="test_admin",
        creator_id=0,
    )
    functions.create_admin(form_data)
    response = functions.login("test_admin", "test_admin")
    assert response.status_code == 200
    admin_access_token = response.json()['access_token']
    assert admin_access_token

    form_data = {
        "email": "test_user@test.com",
        "name": "test_user",
        "password": "test_user",
        "username": "test_user",
    }
    response = functions.create_user(admin_access_token, form_data)
    assert response.status_code == 200
    user_id = response.json()['id']

    form_data = {
        "name": "test_brand",
    }
    response = functions.create_brand(admin_access_token, form_data)
    assert response.status_code == 200
    brand_id = response.json()['id']

    form_data = {
        "name": "test_device_category",
    }
    response = functions.create_device_category(admin_access_token, form_data)
    assert response.status_code == 200
    device_category_id = response.json()['id']

    form_data = {
        "hostname": "test_device",
        "asset_number": "PC0001",
        "brand_id": brand_id,
        "category_id": device_category_id,
    }
    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 200
    device_id = response.json()['id']


def test_create():
    global user_has_device_id

    form_data = {
        "user_id": 0,
        "device_id": device_id,
        "flag": 1,
        "message": "user manages device",
    }
    response = functions.create_user_has_device(admin_access_token, form_data)
    assert response.status_code == 404

    form_data = {
        "user_id": user_id,
        "device_id": 0,
        "flag": 1,
        "message": "user manages device",
    }
    response = functions.create_user_has_device(admin_access_token, form_data)
    assert response.status_code == 404

    form_data = {
        "user_id": user_id,
        "device_id": device_id,
        "flag": 1,
        "message": "user manages device",
    }
    response = functions.create_user_has_device(admin_access_token, form_data)
    assert response.status_code == 200
    user_has_device_id = response.json()['id']

    form_data = {
        "user_id": user_id,
        "device_id": device_id,
        "flag": 1,
        "message": "user manages device",
    }
    response = functions.create_user_has_device(admin_access_token, form_data)
    assert response.status_code == 409

    form_data = {
        "hostname": "test_device2",
        "asset_number": "PC0002",
        "brand_id": brand_id,
        "category_id": device_category_id,
    }
    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 200
    temp_device_id = response.json()['id']

    form_data = {
        "user_id": user_id,
        "device_id": temp_device_id,
        "flag": 2,
        "message": "user lends device",
        "expired_at": "2022-01-01 00:00:00",
    }
    response = functions.create_user_has_device(admin_access_token, form_data)
    assert response.status_code == 200


def test_select():
    response = functions.select_user_has_devices(admin_access_token)
    assert response.status_code == 200

    response = functions.select_user_has_device(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.select_user_has_device(admin_access_token, user_has_device_id)
    assert response.status_code == 200


def test_delete():
    response = functions.delete_user_has_device(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.delete_user_has_device(admin_access_token, user_has_device_id)
    assert response.status_code == 200

    response = functions.delete_user_has_device(admin_access_token, user_has_device_id)
    assert response.status_code == 404


def test_end():
    functions.end()
