from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# import psycopg2
# from psycopg2.extras import RealDictCursor
# import time

# while True:
#   try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#                           password='HELLOWORLD101', cursor_factory=RealDictCursor)
#     # Note that the 'cursor_factor=RealDictCursor' just makes it so that the column names are also displayed
#     cursor = conn.cursor()
#     print('Database connection was successful')
#     break
#   except Exception as error:
#     print('Connecting to databse failed')
#     print(error)
#     time.sleep(2)


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()