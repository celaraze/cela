from fastapi.testclient import TestClient

from app.config.database import engine
from app.database import tables, schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
user_access_token = ""
user_id = 0
role_id = 0
user_has_role_id = 0


def test_start():
    tables.Base.metadata.drop_all(bind=engine)
    tables.Base.metadata.create_all(bind=engine)

    global admin_access_token
    global user_access_token
    global user_id
    global role_id

    form_data = schemas.UserForm(
        email="test_admin@test.com",
        name="test_admin",
        password="test_admin",
        username="test_admin",
        creator_id=None,
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
        "name": "test_role",
        "scopes": [
            "auth:me"
        ],
    }
    response = functions.create_role(admin_access_token, form_data)
    assert response.status_code == 200
    role_id = response.json()['id']

    form_data = {
        "user_id": user_id,
        "role_id": role_id,
    }
    response = functions.create_user_has_role(admin_access_token, form_data)
    assert response.status_code == 200

    response = functions.login("test_user", "test_user")
    assert response.status_code == 200
    user_access_token = response.json()['access_token']
    assert user_access_token


def test_create():
    global user_has_role_id
    global user_access_token

    form_data = {
        "user_id": user_id,
        "role_id": role_id,
    }
    response = functions.create_user_has_role(user_access_token, form_data)
    assert response.status_code == 403

    form_data = {
        "key": "scopes",
        "value": [
            "auth:me",
            "user_has_role:create"
        ]
    }
    response = functions.update_role(admin_access_token, role_id, form_data)
    assert response.status_code == 200

    response = functions.renew(user_access_token)
    assert response.status_code == 200
    user_access_token = response.json()['access_token']

    form_data = {
        "user_id": 0,
        "role_id": role_id,
    }
    response = functions.create_user_has_role(user_access_token, form_data)
    assert response.status_code == 404

    form_data = {
        "user_id": user_id,
        "role_id": 0,
    }
    response = functions.create_user_has_role(user_access_token, form_data)
    assert response.status_code == 404

    form_data = {
        "user_id": 0,
        "role_id": 0,
    }
    response = functions.create_user_has_role(user_access_token, form_data)
    assert response.status_code == 404

    form_data = {
        "user_id": user_id,
        "role_id": role_id,
    }
    response = functions.create_user_has_role(user_access_token, form_data)
    assert response.status_code == 200
    user_has_role_id = response.json()['id']


def test_select():
    global user_access_token

    response = functions.select_user_has_roles(user_access_token)
    assert response.status_code == 403

    form_data = {
        "key": "scopes",
        "value": [
            "auth:me",
            "user_has_role:create",
            "user_has_role:list",
        ]
    }
    response = functions.update_role(admin_access_token, role_id, form_data)
    assert response.status_code == 200

    response = functions.renew(user_access_token)
    assert response.status_code == 200
    user_access_token = response.json()['access_token']

    response = functions.select_user_has_roles(user_access_token)
    assert response.status_code == 200

    response = functions.select_user_has_role(user_access_token, user_has_role_id)
    assert response.status_code == 403

    form_data = {
        "key": "scopes",
        "value": [
            "auth:me",
            "user_has_role:create",
            "user_has_role:list",
            "user_has_role:info",
        ]
    }
    response = functions.update_role(admin_access_token, role_id, form_data)
    assert response.status_code == 200

    response = functions.renew(user_access_token)
    assert response.status_code == 200
    user_access_token = response.json()['access_token']

    response = functions.select_user_has_role(user_access_token, 0)
    assert response.status_code == 404

    response = functions.select_user_has_role(user_access_token, user_has_role_id)
    assert response.status_code == 200


def test_delete():
    global user_access_token

    response = functions.delete_user_has_role(user_access_token, user_has_role_id)
    assert response.status_code == 403

    response = functions.delete_user_has_role(admin_access_token, 0)
    assert response.status_code == 404

    form_data = {
        "key": "scopes",
        "value": [
            "auth:me",
            "user_has_role:create",
            "user_has_role:list",
            "user_has_role:info",
            "user_has_role:delete",
        ]
    }
    response = functions.update_role(admin_access_token, role_id, form_data)
    assert response.status_code == 200

    response = functions.delete_user_has_role(admin_access_token, user_has_role_id)
    assert response.status_code == 200

    form_data = {
        "user_id": user_id,
        "role_id": role_id,
    }
    response = functions.create_user_has_role(user_access_token, form_data)
    assert response.status_code == 200

    response = functions.renew(user_access_token)
    assert response.status_code == 200
    user_access_token = response.json()['access_token']

    response = functions.delete_user_has_role_by_user_id_and_role_id(user_access_token, 0, role_id)
    assert response.status_code == 404

    response = functions.delete_user_has_role_by_user_id_and_role_id(user_access_token, user_id, 0)
    assert response.status_code == 404

    response = functions.delete_user_has_role_by_user_id_and_role_id(user_access_token, 0, 0)
    assert response.status_code == 404

    response = functions.delete_user_has_role_by_user_id_and_role_id(user_access_token, user_id, role_id)
    assert response.status_code == 200


def test_end():
    tables.Base.metadata.drop_all(bind=engine)
    engine.dispose()
