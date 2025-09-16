import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
DB_URL = os.getenv("DB_URL", "mysql+mysqlconnector://pb:pbpass@127.0.0.1:3307/pool_booking")

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    future=True,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False, future=True)

def get_engine():
    return engine

def get_session():
    return SessionLocal()
