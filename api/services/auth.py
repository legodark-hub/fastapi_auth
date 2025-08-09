from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import user as user_repository
from schemas.user import UserCreate
from utils.security import verify_password


async def register_new_user(db: AsyncSession, user: UserCreate):
    db_user = await user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_repository.create_user(db=db, user=user)


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user = await user_repository.get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user