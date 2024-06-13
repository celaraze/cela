# Cela

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