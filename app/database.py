from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker



SQL_BD_URL = 'postgresql+asyncpg://postgres:password@db:5432/postgres'

async_engine = create_async_engine(SQL_BD_URL, echo=True)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()



# async def create_database():
#     # Подключение без указания базы или к стандартной postgres
#     # engine = create_async_engine("postgresql+asyncpg://postgres:password@db:5432/postgres", echo=True)

#     async with async_engine.connect() as conn:
#         await conn.execute("commit")  # для выполнения к��манды create database
#         await conn.execute(f"CREATE DATABASE my_new_db")
#     await async_engine.dispose()

