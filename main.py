from fastapi import FastAPI
from controllers import welcome
from controllers import user

app = FastAPI()

app.include_router(welcome.router)
app.include_router(user.router)
