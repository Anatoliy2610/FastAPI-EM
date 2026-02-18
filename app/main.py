from fastapi import FastAPI
from app.router import router as main_router

import asyncio

import tracemalloc
import warnings 


from app.database import async_engine, Base

async def init_models(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield



app = FastAPI(lifespan=init_models)



app.include_router(main_router)



# from fastapi import FastAPI
# from app.router import router as main_router
# import asyncio


# from app.database import Base, async_engine

# # target_metadata = Base.metadata
# async def init_models():
#     async with async_engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)

# asyncio.run(init_models())

# app = FastAPI()

# app.include_router(main_router)



