> [!IMPORTANT]
>
> This project is still working in progress. Please go to [CAT](https://github.com/celaraze/cat)
> or [CHEMEX](https://github.com/celaraze/chemex) for using in production.

# Cela

English | [简体中文](README/README.zh_CN.md)

Cela is an asset management system with front-end and back-end separation, and provides a command-line client. Users can
use the command-line client to manage assets, or use their own built front-end program.

Even if you are a developer or a user, it is highly recommended that you read the [Answering](ANSWERING.md) first, which
will let you know the
development direction and design philosophy of this system.

Cela has the following features:

- User authentication using `bearer` token.
- Permission control using scopes and RBAC.
- Efficient deployment mode, deployed in a containerized way.
- Convenient secondary development, users only need to focus on the implementation of business logic.
- Complete test cases.
- Inherited from the design pattern of chemex and cat.
- ...

## RoadMap

- [x] User authentication
- [x] Role-based access control
- [x] Command-line client
- [x] Todo
- [ ] Device
- [ ] Ticket
- [ ] Software
- [ ] Part
- [ ] Inventory

## Quick Start

Start back-end service with checking `docker-compose.yml` and run the following:

`docker-compose up -d`

And then you need to `GET` [http://localhost:8000/auth/init](http://localhost:8000/auth/init) to initialize the admin.

Now you can visit [http://localhost:8000/docs](http://localhost:8000/docs) to view the API documentation.

Or running `pip install cela` to install the command-line client, and then you can use the command-line client:

```shell
cela connect http://localhost:8000
cela login admin admin
cela device list
```

## Directory Structure

```shell
cela
├── app                                       # The main directory of the project
│   ├── config                                # Configuration file directory
│   │   ├── __init__.py                       
│   │   └── database.py                       # Database configuration file
│   ├── controllers                           # Controller directory
│   │   ├── __init__.py                       
│   │   ├── auth_controller.py                # Authentication controller
│   │   ├── role_controller.py                # Role controller
│   │   └── user_controller.py                # User controller
│   ├── database                              # Database directory
│   │   ├── __init__.py        
│   │   ├── crud.py                           # CRUD operation file       
│   │   ├── schemas.py                        # Pydantic schema file
│   │   └── tables.py                         # SQLAlchemy table file
│   ├── services                              # Service directory
│   │   ├── __init__.py                       
│   │   └── auth.py                           # Authentication service
│   ├── utils                                 # Utility directory
│   │   ├── __init__.py                       
│   │   ├── config.py                         # Configuration file
│   │   ├── crypt.py                          # Cryptography tool
│   │   └── common.py                         # Common tool
│   ├── env.yml                               # Environment configuration file
│   ├── env.yml.example                       # Environment configuration file example
│   ├── admin.py                              # Command-line client
│   ├── main.py                               # Main file
│   └── dependencies.py                       # Dependency functions for controllers
├── tests                                     # Test directory
│   ├── __init__.py                           
│   ├── functions.py                          # Test function file
│   └── test_xxx.py                           # Test file
├── requirements.txt                          # Dependency file
└── Dockerfile                                # Dockerfile
```

## Contributing

If you have any suggestions or find any bugs, please feel free to submit an issue or pull request.

### Code readability

Cela is not a high-performance tool, so we focus on code readability and maintainability. Please write code that is easy
to read and understand.

### Commit message rules

Please follow the commit message rules below when submitting a pull request:

- Use the English language.
- Use the imperative mood.
- Use the present tense.
- Use the lowercase.
- Do not end with a period.

For example:

```text
# we only support the following prefixes.
feat: add a new feature
fix: fix a bug
docs: update the documentation
style: change the code style
refactor: refactor the code
test: add a test case
chore: change the build process
```

## Sponsors

`Afdian.net` is a platform that provides a way for creators to get support from their fans. If you like this project,
you can support me on Afdian.net.

[https://afdian.net/a/celaraze](https://afdian.net/a/celaraze)

## Thanks

JetBrains provides excellent IDEs.

<a href="https://www.jetbrains.com/?from=cela" target="_blank">
    <img src="https://www.jetbrains.com/company/brand/img/jetbrains_logo.png" width="100" alt="JetBrains" />
</a>