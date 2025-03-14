from fastapi import APIRouter
from app.api.v1.routes import auth, admin, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(admin.router, prefix="/admin")
api_router.include_router(users.router, prefix="/users")