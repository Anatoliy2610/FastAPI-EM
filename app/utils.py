import redis
from fastapi import Depends
from datetime import datetime, timedelta

from app.database import async_session_maker


async def get_async_db():
    async with async_session_maker() as session:
        yield session


redis_client = redis.Redis(host='redis', port=6379, db=0)


def get_ttl_until_1411():
    now = datetime.now()
    target = now.replace(hour=14, minute=11, second=0, microsecond=0)
    if now > target:
        target += timedelta(days=1)  # если уже после 14:11, считаем до следующего дня
    return int((target - now).total_seconds())

