## CELA 是什么？

`CELA` 是一个轻量、快速、友好的 Web API 开发脚手架。设计思路来源于 Laravel 全栈框架，致力于打造 Python
生态圈的轻量级类 Laravel 开发框架，让 Laravel 开发者可友好切换开发体验。上游依赖基于 `FastAPI`、`SQLAlchemy`
等。与 Laravel 不同的是，`CELA` 移除了 MVC 中的视图层。

由于 Python 生态和 PHP 生态的差异性，暂时无法完全照搬 Laravel 的设计模式，后续会通过迭代方式尽可能的接近 Laravel 的开发体验。

## 使用方法

### 数据库

#### ORM

> ORM 使用 SQLAlchemy 实现，详细文档可参考：https://docs.sqlalchemy.org/en/20/

#### 数据库迁移

> 数据库迁移脚本使用 `/alembic` 实现，详细文档可参考：https://alembic.sqlalchemy.org/en/latest/tutorial.html

数据库迁移和应用本身连接数据库的配置是独立的，迁移时使用的数据库配置文件在 `database/migrations/alembic.ini` 中。

##### 创建迁移文件

首先执行命令 `cd database/migrations` 进入数据库迁移目录。

修改 `alembic.ini` 配置文件：

```ini
...

# 修改数据库连接信息，例如：mariadb_pymysql://root:password@127.0.0.1:3306/cela
sqlalchemy.url = mariadb+pymysql://username:password@host:port/database_name

...
```

`alembic revision -m "create articles table"`

会在 `database/migrations/versions` 中创建一条数据库迁移脚本。

迁移文件脚本使用和 Laravel
类似，都分别定义了一个升级和一个降级对应的方法，所进行的数据库操作脚本也同样被定义在方法中，写法可参考预设的 `2f6b7edbcb33_create_users_table.py` 。

##### 迁移升级

执行 `alembic upgrade head` 为升级到最新版本状态。

##### 迁移降级

执行 `alembic downgrade base` 为降级到最初始状态。