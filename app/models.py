from sqlalchemy import Column, Integer, Float, String
from app.database import Base
from pydantic import BaseModel


class TradingResultSchema(BaseModel):
    id: int
    year: float
    мonth_number: float
    category: str
    count_contracts: float
    count_value_contracts: float

    class Config:
        orm_mode = True


class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Float) # Год
    мonth_number = Column(Float) # Номер месяца
    category = Column(String) # категория
    count_contracts = Column(Float) # 'Суммарное количество заключенных договоров во всех секциях, шт.'
    count_value_contracts = Column(Float) # 'Суммарный объем заключенных договоров во всех секциях, руб.'
