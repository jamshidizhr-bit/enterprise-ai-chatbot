from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest
from app.services.ai_service import stream_ai
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat/stream")
def chat_stream(request: ChatRequest, db: Session = Depends(get_db)):

    # 1. conversation
    if not request.conversation_id:
        conversation = Conversation(user_id=1, title="New Chat")
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        conversation_id = conversation.id
    else:
        conversation_id = request.conversation_id

    # 2. save user message
    user_msg = Message(
        conversation_id=conversation_id,
        role="user",
        content=request.message
    )
    db.add(user_msg)
    db.commit()

    # 3. history
    history = db.query(Message).filter(
        Message.conversation_id == conversation_id
    ).order_by(Message.id).all()

    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    for msg in history:
        messages.append({
            "role": msg.role,
            "content": msg.content
        })

    full_response = []

    def generate():
        for token in stream_ai(messages):
            full_response.append(token)
            yield token

        # 4. save assistant message
        ai_msg = Message(
            conversation_id=conversation_id,
            role="assistant",
            content="".join(full_response)
        )
        db.add(ai_msg)
        db.commit()

    return StreamingResponse(generate(), media_type="text/plain")