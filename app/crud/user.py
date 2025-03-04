import uuid
from typing import Any

from sqlmodel import Session, select

from models.user import User, UserCreate
from core.security import get_password_hash, verify_password


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user