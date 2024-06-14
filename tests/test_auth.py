from fastapi.testclient import TestClient

from app.database import schemas, tables
from app.config.database import engine

from app.main import app

from tests import functions

client = TestClient(app)

access_token = ""


def test_start():
    tables.Base.metadata.drop_all(bind=engine)
    tables.Base.metadata.create_all(bind=engine)

    user_create = schemas.UserCreateForm(
        email="test_admin@test.com",
        name="test_admin",
        password="test_admin",
        username="test_admin",
        creator_id=None,
    )
    print()
    functions.create_admin(user_create)


def test_login():
    global access_token

    response = functions.login("test_admin", "test_admin2")
    assert response.status_code == 401

    response = functions.login("test_admin", "test_admin")
    assert response.status_code == 200

    access_token = response.json()['access_token']
    assert access_token


def test_renew():
    global access_token

    response = functions.renew("test_token")
    assert response.status_code == 401

    response = functions.renew(access_token)
    assert response.status_code == 200

    access_token = response.json()['access_token']
    assert access_token


def test_select():
    global access_token

    response = functions.select_me(access_token)
    assert response.status_code == 200

    assert response.json()['username'] == "test_admin"


def test_update():
    global access_token

    response = functions.update_me(access_token, "name", "test_admin2")
    assert response.status_code == 200

    response = functions.update_me(access_token, "email", "test_admin2@test.com")
    assert response.status_code == 200

    response = functions.update_me(access_token, "username", "test_admin2")
    assert response.status_code == 200

    response = functions.login("test_admin2", "test_admin")
    assert response.status_code == 200

    access_token = response.json()["access_token"]
    assert access_token

    response = functions.update_me_change_password(access_token, "test_admin", "test_admin2")
    assert response.status_code == 200

    response = functions.login("test_admin2", "test_admin2")
    assert response.status_code == 200

    access_token = response.json()["access_token"]
    assert access_token


def test_end():
    tables.Base.metadata.drop_all(bind=engine)
    engine.dispose()
