from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQL_BD_URL = "sqlite:///./DB.db" 
SQL_BD_URL = "sqlite:///./DB.db"


engine = create_engine(SQL_BD_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
