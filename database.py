from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os 
from dotenv import load_dotenv

#Carregar variaveis do arquivo .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

session = sessionmaker(bind=engine)

#Base para todos os models do 
Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close