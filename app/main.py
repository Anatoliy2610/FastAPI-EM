from fastapi import FastAPI
from app.router import router as main_router



from app.database import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(main_router)



