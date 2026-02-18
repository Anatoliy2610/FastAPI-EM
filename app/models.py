from sqlalchemy import Column, Integer, Float, String
from app.database import Base


class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Float) # Год
    мonth_number = Column(Float) # Номер месяца
    category = Column(String) # категория
    count_contracts = Column(Float) # 'Суммарное количество заключенных договоров во всех секциях, шт.'
    count_value_contracts = Column(Float) # 'Суммарный объем заключенных договоров во всех секциях, руб.'
