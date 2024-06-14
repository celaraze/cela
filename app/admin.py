import argparse

from app.services import auth
from app.config.database import engine
from .database import schemas, tables


def create_super_admin():
    username = input("Enter username: ")
    email = input("Enter email: ")
    name = input("Enter name: ")
    password = input("Enter password: ")
    auth.create_super_admin(
        schemas.UserCreateForm(
            username=username,
            email=email,
            name=name,
            password=password,
            creator_id=None
        )
    )


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    admin_parser = subparsers.add_parser('create_super_admin')

    args = parser.parse_args()

    if args.command == 'create_super_admin':
        create_super_admin()
    else:
        print("Invalid command. Please follow the usage below.")
        print("Usage: python3 admin.py <command>")
        print("Commands:")
        print("  admin        Create an super-administrator.")
        print("Github: https://github.com/celaraze/fastservice, docs here.")


if __name__ == '__main__':
    tables.Base.metadata.create_all(bind=engine)
    main()
