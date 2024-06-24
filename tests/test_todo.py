from fastapi.testclient import TestClient

from app.database import schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
todo_id = 0


def test_start():
    functions.start()

    global admin_access_token

    form_data = schemas.UserCreateForm(
        email="test_admin@test.com",
        name="test_admin",
        password="test_admin",
        username="test_admin",
    )
    functions.create_admin(form_data)
    response = functions.login("test_admin", "test_admin")
    assert response.status_code == 200
    admin_access_token = response.json()['access_token']
    assert admin_access_token


def test_create():
    global todo_id

    form_data = {
        "title": "todo 1",
        "priority": 1,
    }
    response = functions.create_todo(admin_access_token, form_data)
    assert response.status_code == 200
    todo_id = response.json()['id']

    # Test duplicate, should success because of title is not unique.
    response = functions.create_todo(admin_access_token, form_data)
    assert response.status_code == 200


def test_select():
    response = functions.select_todos(admin_access_token)
    assert response.status_code == 200

    response = functions.select_todo(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.select_todo(admin_access_token, todo_id)
    assert response.status_code == 200
    assert response.json()['title'] == "todo 1"


def test_update():
    form_data = [
        {
            "key": "title",
            "value": "todo 2",
        }
    ]

    response = functions.update_todo(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.update_todo(admin_access_token, todo_id, form_data)
    assert response.status_code == 200
    assert response.json()['title'] == "todo 2"


def test_delete():
    response = functions.delete_todo(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.delete_todo(admin_access_token, todo_id)
    assert response.status_code == 200

    response = functions.delete_todo(admin_access_token, todo_id)
    assert response.status_code == 404

    response = functions.delete_todo(admin_access_token, todo_id)
    assert response.status_code == 404


def test_todo_minute():
    global todo_id

    form_data = {
        "title": "todo 1",
    }
    response = functions.create_todo(admin_access_token, form_data)
    assert response.status_code == 200
    todo_id = response.json()['id']

    form_data = {
        "todo_id": 0,
    }

    response = functions.start_work_on_todo(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.start_work_on_todo(admin_access_token, todo_id, form_data)
    assert response.status_code == 406

    form_data = {
        "todo_id": todo_id,
    }

    response = functions.start_work_on_todo(admin_access_token, todo_id, form_data)
    assert response.status_code == 200
    start_time = response.json()['created_at']

    response = functions.start_work_on_todo(admin_access_token, todo_id, form_data)
    assert response.status_code == 409

    form_data = {
        "todo_id": 0
    }

    response = functions.end_work_on_todo(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.end_work_on_todo(admin_access_token, todo_id, form_data)
    assert response.status_code == 406

    form_data = {
        "todo_id": todo_id,
    }

    response = functions.end_work_on_todo(admin_access_token, todo_id, form_data)
    assert response.status_code == 200
    end_time = response.json()['created_at']

    response = functions.end_work_on_todo(admin_access_token, todo_id, form_data)
    assert response.status_code == 404

    assert end_time >= start_time


def test_end():
    functions.end()
