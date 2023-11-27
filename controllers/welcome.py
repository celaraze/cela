from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def users():
    return {"message": "Welcome to Cela!"}
