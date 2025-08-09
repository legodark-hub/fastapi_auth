from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from repositories import user as user_repository
from schemas.user import UserCreate


async def register_new_user(db: AsyncSession, user: UserCreate):
    db_user = await user_repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await user_repository.create_user(db=db, user=user)
