from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["Connection Test"])


@router.get("/")
def ping():
    return "ping!"
