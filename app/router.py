from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import json

from app.utils import get_async_db, redis_client, get_ttl_until_1411
from app.models import SpimexTradingResult
from app.schemas import TradingResultSchema


router = APIRouter(tags=['Биржа'])


@router.get("/trading_dates")
async def get_last_trading_dates(db: AsyncSession = Depends(get_async_db)):
    '''
    1 ручка - задание "список дат последних торговых дней (фильтрация по кол-ву последних торговых дней)."
    - сделал список годов и сколько в каждом записей
    '''
    cache_key = "trading_dates"
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    result = []
    scalar_1 = await db.scalars(select(SpimexTradingResult).order_by(SpimexTradingResult.year.asc()).limit(1))
    scalar_2 = await db.scalars(select(SpimexTradingResult).order_by(SpimexTradingResult.year.desc()).limit(1))
    first_year = scalar_1.first()
    last_year = scalar_2.first()

    if not first_year or not last_year:
        raise HTTPException(status_code=404, detail="Данные не найдены")
    for year in range(int(first_year.year), int(last_year.year)):
        print(first_year.year, last_year.year)
        query = await db.scalars(select(SpimexTradingResult).filter(SpimexTradingResult.year == year))
        data_year = query.all()
        result.append({f'year {year}': len(data_year)})

    ttl = get_ttl_until_1411()
    redis_client.setex(cache_key, ttl, json.dumps(result))
    return result    


@router.get("/dynamics", response_model=List[TradingResultSchema])
async def get_dynamics(year_first: Optional[float] = Query(None, description="Начальный год фильтрации"), 
                 year_last: Optional[float] = Query(None, description="Конечный год фильтрации"), 
                 db: AsyncSession = Depends(get_async_db)):
    '''
    2 ручка - задание "список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)."
    - сделал список записей, который можно отфильтровать по заданному диапозону годов (например 2020 и 2024)
    '''
    if year_first > year_last:
        raise HTTPException(status_code=400, detail="Данные введены неверно")
    query = await db.scalars(select(SpimexTradingResult).filter(
        SpimexTradingResult.year >= year_first,
        SpimexTradingResult.year <= year_last
        ))
    result = query.all()
    return result

#### переписать через select
@router.get("/trading_results", response_model=List[TradingResultSchema])
async def get_trading_results(db: AsyncSession = Depends(get_async_db)):
    # список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
    '''
    3 ручка - задание "список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)."
    - сделал список записей за последний год
    '''
    query = await db.scalars(select(SpimexTradingResult).order_by(SpimexTradingResult.year.desc()).limit(1))
    year = query.first()

    try:
        query = await db.scalars(select(SpimexTradingResult).filter(SpimexTradingResult.year==year.year))
        data_year = query.all()
    except:
        raise HTTPException(status_code=404, detail="Данные отсутствуют")
    return data_year



