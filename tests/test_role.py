from fastapi.testclient import TestClient

from app.config.database import engine
from app.database import tables, schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
user_access_token = ""
role_id = 0


def test_start():
    tables.Base.metadata.drop_all(bind=engine)
    tables.Base.metadata.create_all(bind=engine)

    global admin_access_token

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


def test_create():
    global role_id

    form_data = {
        "name": "test_role",
        "scopes": ["test:read"],
    }
    response = functions.create_role(admin_access_token, form_data)
    assert response.status_code == 200
    role_id = response.json()['id']

    response = functions.create_role(admin_access_token, form_data)
    assert response.status_code == 409


def test_select():
    response = functions.select_roles(admin_access_token)
    assert response.status_code == 200

    response = functions.select_role(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.select_role(admin_access_token, role_id)
    assert response.status_code == 200
    assert response.json()['name'] == "test_role"


def test_update():
    form_data = {
        "key": "name",
        "value": "test_role2",
    }

    response = functions.update_role(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.update_role(admin_access_token, role_id, form_data)
    assert response.status_code == 200
    assert response.json()['name'] == "test_role2"

    form_data = {
        "key": "scopes",
        "value": ["test:read", "test:write"],
    }
    response = functions.update_role(admin_access_token, role_id, form_data)
    assert response.status_code == 200
    assert response.json()['scopes'] == ["test:read", "test:write"]


def test_delete():
    response = functions.delete_role(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.delete_role(admin_access_token, role_id)
    assert response.status_code == 200
    response = functions.select_role(admin_access_token, role_id)
    assert response.status_code == 404


def test_end():
    tables.Base.metadata.drop_all(bind=engine)
    engine.dispose()
