> [!IMPORTANT]
>
> 这个项目仍在开发中。如有生产环境使用需求请前往 [CAT](https://github.com/celaraze/cat)
> 或 [CHEMEX](https://github.com/celaraze/chemex) 。

# Cela

[English](../README.md) | 简体中文

Cela 是一个前后端分离的资产管理系统，提供了命令行客户端。用户可以使用命令行客户端管理资产，或者使用自己构建的前端程序。

Cela 具有以下特点：

- 使用 `bearer` token 进行用户认证。
- 使用 scopes 和 RBAC 进行权限控制。
- 高效的部署模式，以容器化方式部署。
- 方便的二次开发，用户只需关注业务逻辑的实现。
- 完整的测试用例。
- 继承自 chemex 和 cat 的设计模式。
- ...

## 快速开始

使用以下步骤启动后端服务：

`docker run -d -p 8000:8000 --name cela celaraze/cela:latest`

现在您可以访问 [http://localhost:8000/docs](http://localhost:8000/docs) 查看 API 文档。

提示：现在无法使用该镜像，因为它仍在开发中。

## 目录结构

```shell
cela
├── app                                       # 项目主目录
│   ├── config                                # 配置文件目录
│   │   ├── __init__.py                       
│   │   └── database.py                       # 数据库配置文件
│   ├── controllers                           # 控制器目录
│   │   ├── __init__.py                       
│   │   ├── auth_controller.py                # 认证控制器
│   │   ├── role_controller.py                # 角色控制器
│   │   └── user_controller.py                # 用户控制器
│   ├── database                              # 数据库目录
│   │   ├── __init__.py                       
│   │   ├── crud.py                           # CRUD 操作文件
│   │   ├── schemas.py                        # Pydantic schema 文件
│   │   └── tables.py                         # 数据库表文件
│   ├── services                              # 服务目录
│   │   ├── __init__.py                       
│   │   └── auth.py                           # 认证服务
│   ├── utils                                 # 工具目录
│   │   ├── __init__.py                       
│   │   ├── config.py                         # 配置工具
│   │   ├── crypt.py                          # 加密工具
│   │   └── common.py                         # 通用工具
│   ├── env.yml                               # 环境配置文件
│   ├── env.yml.example                       # 环境配置文件示例
│   ├── admin.py                              # 命令行工具文件
│   ├── main.py                               # 主文件
│   └── dependencies.py                       # 控制器依赖函数
├── tests                                     # 测试目录
│   ├── __init__.py                           
│   ├── functions.py                          # 测试函数文件
│   └── test_xxx.py                           # 测试文件
├── requirements.txt                          # 依赖文件
└── Dockerfile                                # Dockerfile
```

## 贡献

如果您有任何建议或发现任何错误，请随时提交 ISSUES 或 PR。

### 代码规范

Cela 不是一个高性能工具，因此我们注重代码的可读性和可维护性。请编写易于阅读和理解的代码。

### 提交消息规则

请在提交 PR 时遵循以下提交消息规则：

- 使用英语。
- 使用祈使句。
- 使用现在时。
- 使用小写。
- 不要以句号结尾。

例如：

```text
# 我们只支持以下前缀。
feat: 添加一个新功能
fix: 修复一个 bug
docs: 更新文档
style: 更改代码风格
refactor: 重构代码
test: 添加一个测试用例
chore: 更改构建过程
```

## 赞助

`Afdian.net` 是一个为创作者提供支持的平台。如果您喜欢这个项目，可以在 `Afdian.net` 上支持我。

[https://afdian.net/a/celaraze](https://afdian.net/a/celaraze)

## 感谢

JetBrains 提供了优秀的 IDE。

<a href="https://www.jetbrains.com/?from=cela" target="_blank">
    <img src="https://www.jetbrains.com/company/brand/img/jetbrains_logo.png" width="100" alt="JetBrains" />
</a>