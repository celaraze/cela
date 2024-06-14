# Cela

English | [简体中文](README/README.zh_CN.md)

Cela is an asset management system with front-end and back-end separation, and provides a command-line client. Users can
use the command-line client to manage assets, or use their own built front-end program.

Cela has the following features:

- User authentication using `bearer` token.
- Permission control using scopes and RBAC.
- Efficient deployment mode, deployed in a containerized way.
- Convenient secondary development, users only need to focus on the implementation of business logic.
- Complete test cases.
- Inherited from the design pattern of chemex and cat.
- ...

## Quick Start

Start back-end service with the following steps:

`docker run -d -p 8000:8000 --name cela celaraze/cela:latest`

Now you can visit [http://localhost:8000/docs](http://localhost:8000/docs) to view the API documentation.

Tips: The image cannot be used now, because it still needs to be developed.

## Directory Structure

```shell
cela
├── app                                       
│   ├── config                                
│   │   ├── __init__.py                       
│   │   └── database.py                       
│   ├── controllers                           
│   │   ├── __init__.py                       
│   │   ├── auth_controller.py               
│   │   ├── role_controller.py                
│   │   ├── user_controller.py                
│   │   └── user_has_role_controller.py       
│   ├── database                              
│   │   ├── __init__.py                       
│   │   ├── schemas.py                        
│   │   └── tables.py                         
│   ├── models                                
│   │   ├── __init__.py                       
│   │   ├── role.py                           
│   │   ├── user.py                           
│   │   └── user_has_role.py                  
│   ├── services                              
│   │   ├── __init__.py                       
│   │   └── auth.py                           
│   ├── utils                                 
│   │   ├── __init__.py                       
│   │   ├── config.py                         
│   │   ├── crypt.py                          
│   │   └── common.py                         
│   ├── env.yml                               
│   ├── env.yml.example                       
│   ├── admin.py                              
│   ├── main.py                               
│   └── dependencies.py                       
├── tests                                     
│   ├── __init__.py                           
│   ├── functions.py                          
│   └── test_xxx.py                              
├── requirements.txt                          
└── Dockerfile                                
```