from fastapi import APIRouter, Depends
from app.api.dependencies import get_current_user

router = APIRouter()

@router.post("/chat")
async def chat():
    return {"message": "Chat endpoint placeholder"}
