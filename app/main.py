from fastapi import FastAPI
from app.router import router as main_router

from app.database import async_engine, Base


async def init_models(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield

app = FastAPI(lifespan=init_models)

app.include_router(main_router)

