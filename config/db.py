from fastapi import  Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Annotated
from dotenv import load_dotenv
from config.base_class import Base
import os

load_dotenv()

DB_PORT = os.getenv("DB_PORT")  # Puerto predeterminado para PostgreSQL
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_HOST = os.getenv("DB_HOST")

# URL de conexión para PostgreSQL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)



def init_db():
    try:
        engine.connect()
        print("Conectadooooooo")
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")
        
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
