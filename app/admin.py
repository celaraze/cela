import argparse

from app.services import auth
from app.database.database import engine, SessionLocal
from .database import schemas, tables


def create_super_admin():
    db = SessionLocal()
    username = input("Enter username: ")
    email = input("Enter email: ")
    name = input("Enter name: ")
    password = input("Enter password: ")
    auth.create_super_admin(
        db,
        schemas.UserCreateForm(
            username=username,
            email=email,
            name=name,
            password=password,
            creator_id=0
        )
    )
    db.close()


def init_super_admin():
    db = SessionLocal()
    username = "admin"
    email = "admin@localhost"
    name = "Admin"
    password = "admin"
    auth.create_super_admin(
        db,
        schemas.UserCreateForm(
            username=username,
            email=email,
            name=name,
            password=password,
            creator_id=0
        )
    )
    db.close()


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    create_super_admin_parser = subparsers.add_parser('create_super_admin')

    init_super_admin_parser = subparsers.add_parser('init_super_admin')

    args = parser.parse_args()

    if args.command == 'create_super_admin':
        create_super_admin()
    elif args.command == 'init_super_admin':
        init_super_admin()
    else:
        print("Invalid command. Please follow the usage below.")
        print("Usage: python3 admin.py <command>")
        print("Commands:")
        print("  init_super_admin          Create an super-administrator when firstly installed.")
        print("  create_super_admin        Create an super-administrator by yourself.")
        print("Github: https://github.com/celaraze/cela, docs here.")


if __name__ == '__main__':
    tables.Base.metadata.create_all(bind=engine)
    main()
