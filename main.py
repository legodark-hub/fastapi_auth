from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.routes import auth
from database.connection import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api")
