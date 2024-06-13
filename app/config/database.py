from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from ..utils.config import get_database_config

SQLALCHEMY_DATABASE_URL = get_database_config()["url"]
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
