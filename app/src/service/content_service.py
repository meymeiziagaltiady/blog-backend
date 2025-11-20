from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.src.db.model import Content
from app.src.schema.content_schema import ContentCreate, ContentUpdate


def create_content(db: Session, payload: ContentCreate, user_id: int):
    content = Content(title=payload.title, body=payload.body, user_id=user_id)
    db.add(content)
    db.commit()
    db.refresh(content)

    return content


def get_all_user_content(db: Session, user_id: int):
    contents = db.query(Content).filter(Content.user_id == user_id).all()

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
        )

    return db.query(Content).filter(Content.user_id == user_id).all()


def get_content_by_id(db: Session, content_id: int):
    content = db.query(Content).filter(Content.id == content_id).first()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Content not found"
        )
    
    return content


def update_content(
    db: Session, content_id: int, payload: ContentUpdate, user_id: int, user_role: str
):
    content = get_content_by_id(db, content_id)

    # authorization
    # check whether admin or the creator
    if content.user_id != user_id and user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You do not have permission to update this content",
        )

    if payload.title:
        content.title = payload.title
    if payload.body:
        content.body = payload.body

    db.commit()
    db.refresh(content)

    return content


def delete_content(db: Session, content_id: int, user_id: int, user_role: str):
    content = get_content_by_id(db, content_id)

    # authorization
    # check whether admin or the creator
    if content.user_id != user_id and user_role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You do not have permission to delete this content",
        )

    db.delete(content)
    db.commit()
    
    return content
