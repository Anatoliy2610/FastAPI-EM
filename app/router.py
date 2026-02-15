from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.utils import get_db, redis_client, get_ttl_until_1411
from app.models import SpimexTradingResult


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import json

router = APIRouter(tags=['Биржа'])


@router.get("/trading_dates")
async def get_last_trading_dates(db: AsyncSession = Depends(get_db)):
    '''
    1 ручка - задание "список дат последних торговых дней (фильтрация по кол-ву последних торговых дней)."
    - сделал список годов и сколько в каждом записей
    '''
    cache_key = "trading_dates"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    year = 2026
    result = []
    while True:
        query = select(SpimexTradingResult).filter(SpimexTradingResult.year == year)
        count_result = await db.execute(query)
        count = count_result.scalars().unique().count()
        if count == 0:
            break
        result.append({f'year {year}': count})
        year -= 1

    if not result:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    ttl = get_ttl_until_1411()
    await redis_client.setex(cache_key, ttl, json.dumps(result))
    return result    


@router.get("/dynamics")
async def get_dynamics(year_first: Optional[float] = Query(None, description="Год для фильтрации"), 
                 year_last: Optional[float] = Query(None, description="Год для фильтрации"), 
                 db: Session = Depends(get_db)):
    '''
    2 ручка - задание "список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)."
    - сделал список записей, который можно отфильтровать по заданному диапозону годов (например 2020 и 2024)
    '''
    if year_first > year_last:
        raise HTTPException(status_code=404, detail="Данные введены неверно")
    query = db.query(SpimexTradingResult).filter(
        SpimexTradingResult.year >= year_first,
        SpimexTradingResult.year <= year_last).all()
    return query


@router.get("/trading_results")
async def get_trading_results(db: Session = Depends(get_db)):
    # список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
    '''
    3 ручка - задание "список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)."
    - сделал список записей за последний год
    '''
    try:
        query = db.query(SpimexTradingResult).order_by(SpimexTradingResult.year.desc()).first()
        year = query.year
    except:
        raise HTTPException(status_code=404, detail="Данные отсутствуют")
    result = db.query(SpimexTradingResult).filter(SpimexTradingResult.year == year).all()
    return result



