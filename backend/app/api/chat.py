from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.services.ai_service import stream_ai

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat-stream")
def chat_stream(request: dict):
    return StreamingResponse(
        stream_ai(request["message"]),
        media_type="text/plain"
    )