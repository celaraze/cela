from fastapi.testclient import TestClient

from app.database import schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
user_access_token = ""
user_id = 0
role_id = 0
device_id = 0
user_has_role_id = 0
user_has_device_id = 0


def test_start():
    functions.start()

    global admin_access_token
    global role_id
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
        "name": "base",
        "scopes": [
            'auth:me'
        ]
    }
    response = functions.create_role(admin_access_token, form_data)
    assert response.status_code == 200
    role_id = response.json()['id']

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
    global user_id
    form_data = {
        "email": "test_user@test.com",
        "name": "test_user",
        "password": "test_user",
        "username": "test_user",
    }
    response = functions.create_user(admin_access_token, form_data)
    assert response.status_code == 200
    user_id = response.json()['id']

    response = functions.create_user(admin_access_token, form_data)
    assert response.status_code == 409

    form_data = {
        "user_id": user_id,
        "role_id": role_id,
    }

    response = functions.create_user_has_role(admin_access_token, 3, form_data)
    assert response.status_code == 406

    response = functions.create_user_has_role(admin_access_token, user_id, form_data)
    assert response.status_code == 200

    response = functions.create_user_has_role(admin_access_token, user_id, form_data)
    assert response.status_code == 409


def test_login():
    global user_access_token

    response = functions.login("test_user", "test_user2")
    assert response.status_code == 401

    response = functions.login("test_user", "test_user")
    assert response.status_code == 200

    user_access_token = response.json()['access_token']
    assert user_access_token


def test_renew():
    global user_access_token

    response = functions.renew("test_token")
    assert response.status_code == 401

    response = functions.renew(user_access_token)
    assert response.status_code == 200

    user_access_token = response.json()['access_token']
    assert user_access_token


def test_select():
    global user_access_token
    global role_id

    response = functions.select_users(admin_access_token)
    assert response.status_code == 200

    response = functions.select_user(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.select_user(admin_access_token, user_id)
    assert response.status_code == 200
    assert response.json()['username'] == "test_user"

    response = functions.select_users(user_access_token)
    assert response.status_code == 403

    form_data = {
        "name": "test_role",
        "scopes": [
            'user:list'
        ]
    }
    response = functions.create_role(admin_access_token, form_data)
    assert response.status_code == 200
    role_id = response.json()['id']

    form_data = {
        "user_id": user_id,
        "role_id": role_id,
    }

    response = functions.create_user_has_role(admin_access_token, user_id, form_data)
    assert response.status_code == 200

    response = functions.renew(user_access_token)
    assert response.status_code == 200
    user_access_token = response.json()['access_token']

    response = functions.select_users(user_access_token)
    assert response.status_code == 200


def test_update():
    global user_access_token

    update_form = [
        {
            "key": "name",
            "value": "test_user2",
        }
    ]

    response = functions.update_user(admin_access_token, 0, update_form)
    assert response.status_code == 404

    response = functions.update_user(admin_access_token, user_id, update_form)
    assert response.status_code == 200
    assert response.json()['name'] == "test_user2"

    update_form = [
        {
            "key": "email",
            "value": "test_user2@test.com",
        }
    ]

    response = functions.update_user(admin_access_token, user_id, update_form)
    assert response.status_code == 200
    assert response.json()['email'] == "test_user2@test.com"

    update_form = [
        {
            "key": "username",
            "value": "test_user2"
        }
    ]
    response = functions.update_user(admin_access_token, user_id, update_form)
    assert response.status_code == 200
    response = functions.login("test_user2", "test_user")
    assert response.status_code == 200
    user_access_token = response.json()["access_token"]
    assert user_access_token

    update_form = [
        {
            "key": "password",
            "value": "test_user2"
        }
    ]

    response = functions.update_user(admin_access_token, user_id, update_form)
    assert response.status_code == 200
    response = functions.login("test_user2", "test_user2")
    assert response.status_code == 200
    user_access_token = response.json()["access_token"]
    assert user_access_token


def test_delete():
    response = functions.delete_user(admin_access_token, 0)
    assert response.status_code == 404

    form_data = {
        "user_id": user_id,
        "device_id": device_id,
        "flag": 1,
    }
    response = functions.user_has_device_out(admin_access_token, user_id, form_data)
    assert response.status_code == 200

    response = functions.select_devices(admin_access_token)
    assert response.status_code == 200
    assert len(response.json()) == 1

    response = functions.delete_user(admin_access_token, user_id)
    print(response.json())
    assert response.status_code == 200

    response = functions.delete_user(admin_access_token, user_id)
    assert response.status_code == 404

    response = functions.select_user(admin_access_token, user_id)
    assert response.status_code == 404


def test_end():
    functions.end()
