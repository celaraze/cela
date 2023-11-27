from fastapi import APIRouter, Depends
from pydantic import BaseModel
from dependencies import get_token_header
from dependencies import get_query_token
from models import user

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.get("/")
def users():
    return user
