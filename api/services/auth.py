from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from repositories import user as user_repository
from schemas.user import UserCreate
from schemas.token import TokenData
from utils.security import verify_password, oauth2_scheme
from config import settings
from database.connection import get_db


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await user_repository.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


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
