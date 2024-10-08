from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import psycopg2
#from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# # Array to test simulate API behaviour without an actual database
# my_posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'id': 1},{'title': 'favourite foods', 'content': 'i like pizza', 'id': 2}]

# #connect to postgres using psycopg2 
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#                                 password='lemonade-finance1', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Database connected successfully!")
#         break
#     except Exception as error:
#         print("Database not connected successfully!")
#         print ("Error: ", error)
#         time.sleep(2)

# #Array functions instead of postgress
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p
            
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p["id"] == id:
#             return i