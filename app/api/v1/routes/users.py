from typing import Any

from fastapi import APIRouter, HTTPException, status
from app.dependencies.user import CurrentUser
from app.models.user import UserPublic

router = APIRouter(tags=["users"])

@router.get("/me", response_model=UserPublic)
async def read_user_me(current_user: CurrentUser) -> Any:
    return current_user