from fastapi.testclient import TestClient

from app.database import schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
user_access_token = ""
role_id = 0


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
    global role_id

    form_data = {
        "name": "test_role",
        "scopes": ["test:read"],
    }
    response = functions.create_role(admin_access_token, form_data)
    assert response.status_code == 200
    role_id = response.json()['id']

    # Test duplicate, should success because of name is not unique.
    response = functions.create_role(admin_access_token, form_data)
    assert response.status_code == 200


def test_select():
    response = functions.select_roles(admin_access_token)
    assert response.status_code == 200

    response = functions.select_role(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.select_role(admin_access_token, role_id)
    assert response.status_code == 200
    assert response.json()['name'] == "test_role"


def test_update():
    form_data = [
        {
            "key": "name",
            "value": "test_role2",
        },
        {
            "key": "scopes",
            "value": ["test:read", "test:write"],
        }
    ]

    response = functions.update_role(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.update_role(admin_access_token, role_id, form_data)
    assert response.status_code == 200
    assert response.json()['name'] == "test_role2"
    assert response.status_code == 200
    assert response.json()['scopes'] == ["test:read", "test:write"]


def test_delete():
    response = functions.delete_role(admin_access_token, 0)
    assert response.status_code == 404

    form_data = {
        "name": "test_user",
        "email": "test_user@test.com",
        "username": "test_user",
        "password": "test_user",
    }
    response = functions.create_user(admin_access_token, form_data)
    assert response.status_code == 200
    user_id = response.json()['id']

    form_data = {
        "user_id": user_id,
        "role_id": role_id,
    }
    response = functions.create_user_has_role(admin_access_token, 0, form_data)
    assert response.status_code == 406

    response = functions.create_user_has_role(admin_access_token, user_id, form_data)
    assert response.status_code == 200

    response = functions.delete_role(admin_access_token, role_id)
    assert response.status_code == 409

    response = functions.delete_user_has_role(admin_access_token, user_id, role_id)
    assert response.status_code == 200

    response = functions.delete_role(admin_access_token, role_id)
    assert response.status_code == 200

    response = functions.delete_role(admin_access_token, role_id)
    assert response.status_code == 404

    response = functions.select_role(admin_access_token, role_id)
    assert response.status_code == 404


def test_end():
    functions.end()
