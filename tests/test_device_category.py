from fastapi.testclient import TestClient

from app.database import schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
device_category_id = 0


def test_start():
    functions.start()

    global admin_access_token

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


def test_create():
    global device_category_id

    form_data = {
        "name": "test_device_category",
    }
    response = functions.create_device_category(admin_access_token, form_data)
    assert response.status_code == 200
    device_category_id = response.json()['id']

    # Test duplicate, should success because of name is not unique.
    response = functions.create_device_category(admin_access_token, form_data)
    assert response.status_code == 200


def test_select():
    response = functions.select_device_categories(admin_access_token)
    assert response.status_code == 200

    response = functions.select_device_category(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.select_device_category(admin_access_token, device_category_id)
    assert response.status_code == 200
    assert response.json()['name'] == "test_device_category"


def test_update():
    form_data = [
        {
            "key": "name",
            "value": "test_device_category2",
        }
    ]

    response = functions.update_device_category(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.update_device_category(admin_access_token, device_category_id, form_data)
    assert response.status_code == 200
    assert response.json()['name'] == "test_device_category2"


def test_delete():
    response = functions.delete_device_category(admin_access_token, 0)
    assert response.status_code == 404

    form_data = {
        "name": "test_brand",
    }
    response = functions.create_brand(admin_access_token, form_data)
    assert response.status_code == 200
    brand_id = response.json()['id']

    form_data = {
        "hostname": "test_device",
        "asset_number": "PC0001",
        "brand_id": brand_id,
        "category_id": device_category_id,
    }
    response = functions.create_device(admin_access_token, form_data)
    assert response.status_code == 200
    device_id = response.json()['id']

    response = functions.delete_device_category(admin_access_token, device_category_id)
    assert response.status_code == 409

    response = functions.delete_device(admin_access_token, device_id)
    assert response.status_code == 200

    response = functions.delete_device_category(admin_access_token, device_category_id)
    assert response.status_code == 200

    response = functions.delete_device_category(admin_access_token, device_category_id)
    assert response.status_code == 404

    response = functions.select_device_category(admin_access_token, device_category_id)
    assert response.status_code == 404


def test_end():
    functions.end()
