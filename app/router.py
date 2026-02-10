from fastapi import APIRouter, Depends, Query
from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import json

from app.utils import get_db
from app.models import SpimexTradingResult
from app.cache_redis import redis_client, get_ttl_until_1411

router = APIRouter(tags=['Биржа'])


@router.get("/trading_dates")
def get_last_trading_dates(db: Session = Depends(get_db)):
    '''
    1 ручка - задание "список дат последних торговых дней (фильтрация по кол-ву последних торговых дней)."
    - сделал список годов и сколько в каждом записей
    '''
    cache_key = "trading_dates"
    cached = redis_client.get(cache_key)
    if cached:
        print('работает редис')
        return json.loads(cached)
    
    query = db.query(SpimexTradingResult).order_by(SpimexTradingResult.year.desc())
    result = []
    year = 2026
    while True:
        data = query.filter(SpimexTradingResult.year == year).count()
        if not data:
            break
        result.append({f'year {year}': data})
        year -= 1
    if not result:
        raise HTTPException(status_code=404, detail="Данные не найдены")

    ttl = get_ttl_until_1411()
    redis_client.setex(cache_key, ttl, json.dumps(result))

    return result

@router.get("/dynamics")
def get_dynamics(year_first: Optional[float] = Query(None, description="Год для фильтрации"), 
                 year_last: Optional[float] = Query(None, description="Год для фильтрации"), 
                 db: Session = Depends(get_db)):
    '''
    2 ручка - задание "список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)."
    - сделал список записей, который можно отфильтровать по заданному диапозону годов (например 2020 и 2024)
    '''
    query = db.query(SpimexTradingResult).filter(
        SpimexTradingResult.year >= year_first,
        SpimexTradingResult.year <= year_last).all()
    return query

@router.get("/trading_results")
def get_trading_results(db: Session = Depends(get_db)):
    # список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
    '''
    3 ручка - задание "список торгов за заданный период (фильтрация по oil_id, delivery_type_id, delivery_basis_id, start_date, end_date)."
    - сделал список записей за последний год
    '''
    query = db.query(SpimexTradingResult).order_by(SpimexTradingResult.year.desc()).first()
    year = query.year
    result = db.query(SpimexTradingResult).filter(SpimexTradingResult.year == year).all()
    return result



