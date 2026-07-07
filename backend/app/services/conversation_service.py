from sqlalchemy.orm import Session

from app.models.conversation import Conversation


def get_user_conversations(
    db: Session,
    user_id: int
):
    return (
        db.query(Conversation)
        .filter(
            Conversation.user_id == user_id
        )
        .order_by(
            Conversation.id.desc()
        )
        .all()
    )