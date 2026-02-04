from fastapi import FastAPI
from router import router as main_router



from database import Base, engine, SessionLocal


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(main_router)



