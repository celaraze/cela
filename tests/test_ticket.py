from fastapi.testclient import TestClient

from app.database import schemas
from app.main import app

from tests import functions

client = TestClient(app)

admin_access_token = ""
ticket_id = 0


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
    global ticket_id

    form_data = {
        "title": "No LAN connection",
        "description": "The LAN connection is not working.",
    }
    response = functions.create_ticket(admin_access_token, form_data)
    assert response.status_code == 200
    ticket_id = response.json()['id']

    # Test duplicate, should success because of title is not unique.
    response = functions.create_ticket(admin_access_token, form_data)
    assert response.status_code == 200


def test_select():
    response = functions.select_tickets(admin_access_token)
    assert response.status_code == 200

    response = functions.select_ticket(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.select_ticket(admin_access_token, ticket_id)
    assert response.status_code == 200
    assert response.json()['title'] == "No LAN connection"


def test_update():
    form_data = [
        {
            "key": "title",
            "value": "No WLAN connection",
        }
    ]

    response = functions.update_ticket(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.update_ticket(admin_access_token, ticket_id, form_data)
    assert response.status_code == 200
    assert response.json()['title'] == "No WLAN connection"


def test_delete():
    response = functions.delete_ticket(admin_access_token, 0)
    assert response.status_code == 404

    response = functions.delete_ticket(admin_access_token, ticket_id)
    assert response.status_code == 200

    response = functions.delete_ticket(admin_access_token, ticket_id)
    assert response.status_code == 404

    response = functions.select_ticket(admin_access_token, ticket_id)
    assert response.status_code == 404


def test_ticket_comments():
    global ticket_id

    form_data = {
        "title": "No LAN connection",
        "description": "The LAN connection is not working.",
    }
    response = functions.create_ticket(admin_access_token, form_data)
    assert response.status_code == 200
    ticket_id = response.json()['id']

    form_data = {
        "ticket_id": ticket_id,
        "comment": "Test comment.",
    }
    response = functions.create_ticket_comment(admin_access_token, 0, form_data)
    assert response.status_code == 404

    response = functions.create_ticket_comment(admin_access_token, ticket_id, form_data)
    assert response.status_code == 200
    assert response.json()['comment'] == "Test comment."

    response = functions.select_ticket(admin_access_token, ticket_id)
    assert response.status_code == 200
    assert response.json()['comments'][0]['comment'] == "Test comment."


def test_todo_minutes():
    global ticket_id

    form_data = {
        "title": "No LAN connection",
        "description": "The LAN connection is not working.",
    }
    response = functions.create_ticket(admin_access_token, form_data)
    assert response.status_code == 200
    ticket_id = response.json()['id']

    form_data = {
        "ticket_id": 0,
        "message": None
    }

    response = functions.start_work_on_ticket(admin_access_token, 0, form_data)
    assert response.status_code == 404

    form_data = {
        "ticket_id": ticket_id,
        "message": None
    }

    response = functions.start_work_on_ticket(admin_access_token, 0, form_data)
    assert response.status_code == 406

    resource = functions.start_work_on_ticket(admin_access_token, ticket_id, form_data)
    assert resource.status_code == 200
    start_time = resource.json()['created_at']

    response = functions.start_work_on_ticket(admin_access_token, ticket_id, form_data)
    assert response.status_code == 409

    form_data = {
        "ticket_id": 0,
        "message": None
    }

    response = functions.end_work_on_ticket(admin_access_token, 0, form_data)
    assert response.status_code == 404

    form_data = {
        "ticket_id": ticket_id,
        "message": None
    }

    response = functions.end_work_on_ticket(admin_access_token, 0, form_data)
    assert response.status_code == 406

    resource = functions.end_work_on_ticket(admin_access_token, ticket_id, form_data)
    assert resource.status_code == 200
    end_time = resource.json()['created_at']

    assert end_time >= start_time


def test_end():
    functions.end()
