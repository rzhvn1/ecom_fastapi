import uuid
from typing import Any, TYPE_CHECKING

from sqlmodel import Session, select, func

from app.models.user import UpdatePassword, User, UserCreate, UserUpdate, UserUpdateMe, UsersPublic
from app.core.security import get_password_hash, verify_password

if TYPE_CHECKING:
    from app.dependencies.user import CurrentUser


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user



def get_users(*, session: Session, skip: int, limit: int) -> UsersPublic:
    count_statement = select(func.count()).select_from(User)
    count = session.exec(statement=count_statement).one()
    
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement=statement)

    return UsersPublic(data=users, count=count)


def get_user_by_id(*, session: Session, id: uuid.UUID) -> User | None:
    statement = select(User).where(User.id == id)
    session_user = session.exec(statement=statement).first()
    return session_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement=statement).first()
    return session_user


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_user = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password=password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


def update_user_me(*, session: Session, current_user: "User", user_in: UserUpdateMe) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    current_user.sqlmodel_update(user_data)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


def update_password_me(*, session:Session, current_user: "User", body: UpdatePassword) -> Any:
    hashed_password = get_password_hash(body.new_password)
    current_user.hashed_password = hashed_password
    session.add(current_user)
    session.commit()
    