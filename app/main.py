from fastapi import FastAPI
from .database import tables
from .config.database import engine
from .controllers import (
    auth_controller,
    role_controller,
    user_controller,
    brand_controller,
    device_category_controller,
    device_controller,
)

tables.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations with authentication.",
    },
]

description = """
`Cela` API helps you do awesome stuff. 🚀
"""

app = FastAPI(
    title="Cela",
    description=description,
    summary="Cela APIs",
    version="0.0.1",
    contact={
        "name": "celaraze",
        "url": "https://github.com/celarze",
        "email": "celaraze@qq.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=tags_metadata,
)

app.include_router(auth_controller.router)
app.include_router(role_controller.router)
app.include_router(user_controller.router)
app.include_router(brand_controller.router)
app.include_router(device_category_controller.router)
app.include_router(device_controller.router)
