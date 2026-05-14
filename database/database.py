from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

import os

SQL_ALCHEMY_URL = os.getenv("SQL_ALCHEMY_URL")
engine = create_engine(url=SQL_ALCHEMY_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = declarative_base()
