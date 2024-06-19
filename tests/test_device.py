from fastapi.testclient import TestClient

from app.database import schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
device_id = 0
brand_id = 0
device_category_id = 0


def test_start():
    functions.start()

    global admin_access_token
    global brand_id
    global device_category_id

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


def test_create():
    global device_id

    form_data = {
        "hostname": "test_device",
        "asset_number": "PC0001",
        "brand_id": 0,
        "category_id": 1,
    }
    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 404

    form_data = {
        "hostname": "test_device",
        "asset_number": "PC0001",
        "brand_id": 1,
        "category_id": 0,
    }
    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 404

    form_data = {
        "hostname": "test_device",
        "asset_number": "PC0001",
        "brand_id": 0,
        "category_id": 0,
    }
    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 404

    form_data = {
        "hostname": "test_device",
        "asset_number": "PC0001",
        "brand_id": brand_id,
        "category_id": device_category_id,
    }
    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 200
    device_id = response.json()['id']

    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 409

    form_data = {
        "hostname": "test_device",
        "asset_number": "PC0002",
        "ipv4_address": "192.168.1.1",
        "ipv6_address": "2001:db8::1",
        "mac_address": "00:00:00:00:00:00",
        "brand_id": brand_id,
        "category_id": device_category_id,
    }
    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 200
    assert response.json()['ipv4_address'] == "192.168.1.1"


def test_select():
    response = functions.select_devices(admin_access_token)
    assert response.status_code == 200

    response = functions.select_device(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.select_devices(admin_access_token, "PC0001")
    assert response.status_code == 200
    assert response.json()[0]['hostname'] == "test_device"

    response = functions.select_device(admin_access_token, device_id)
    assert response.status_code == 200
    assert response.json()['hostname'] == "test_device"


def test_update():
    form_data = [
        {
            "key": "hostname",
            "value": "test_device2",
        }
    ]

    response = functions.update_device(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.update_device(admin_access_token, device_id, form_data)
    assert response.status_code == 200
    assert response.json()['hostname'] == "test_device2"

    form_data = [
        {
            "key": "asset_number",
            "value": "PC0002",
        }
    ]
    response = functions.update_device(admin_access_token, device_id, form_data)
    assert response.status_code == 423


def test_delete():
    response = functions.delete_device(admin_access_token, 0)
    assert response.status_code == 404

    form_data = {
        "user_id": 1,
        "device_id": device_id,
        "flag": 1,
        "message": "test manager",
        "expired_at": "2022-01-01 00:00:00",
    }
    response = functions.user_has_device_out(admin_access_token, 1, form_data)
    assert response.status_code == 200

    response = functions.delete_device(admin_access_token, device_id)
    assert response.status_code == 409

    form_data = {
        "user_id": 1,
        "device_id": device_id,
    }
    response = functions.user_has_device_in(admin_access_token, 1, form_data)
    print(response.json())
    assert response.status_code == 200

    response = functions.delete_device(admin_access_token, device_id)
    assert response.status_code == 200

    response = functions.delete_device(admin_access_token, device_id)
    assert response.status_code == 404

    response = functions.select_device(admin_access_token, device_id)
    assert response.status_code == 404


def test_end():
    functions.end()
