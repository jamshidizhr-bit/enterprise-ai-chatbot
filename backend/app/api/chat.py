from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.schemas.chat import ChatRequest
from app.services.ai_service import stream_ai
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.core.auth import get_current_user
from app.models.user import User
from fastapi import HTTPException
from app.schemas.conversation import ConversationResponse
from app.services.conversation_service import get_user_conversations

router = APIRouter(prefix="/api", tags=["Chat"])


@router.post("/chat/stream")
def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # 1. conversation
    if not request.conversation_id:

    conversation = Conversation(
        user_id=current_user.id,
        title="New Chat"
    )

    db.add(conversation)
    db.commit()
    db.refresh(conversation)

    conversation_id = conversation.id

else:

    conversation = db.query(
        Conversation
    ).filter(
        Conversation.id == request.conversation_id,
        Conversation.user_id == current_user.id
    ).first()

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found"
        )

    conversation_id = conversation.id

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
    @router.get(
    "/conversations",
    response_model=list[ConversationResponse]
)
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return get_user_conversations(
        db,
        current_user.id
    )

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