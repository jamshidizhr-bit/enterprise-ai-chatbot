from fastapi import APIRouter
from app.schemas.chat import ChatRequest
from app.services.ai_service import ask_ai

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat")
def chat(request: ChatRequest):
    return {
        "answer": ask_ai(request.message)
    }