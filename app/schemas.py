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


