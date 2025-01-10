from fastapi import  Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from typing import Annotated
from dotenv import load_dotenv
from config.base_class import Base
import os

load_dotenv()

DB_PORT = os.getenv("RAZA_MATCH_DB_PORT_DOCKER")  # Puerto predeterminado para PostgreSQL
DB_PASSWORD = os.getenv("RAZA_MATCH_DB_PASSWORD")
DB_NAME = os.getenv("RAZA_MATCH_DB_NAME")
DB_USER = os.getenv("RAZA_MATCH_DB_USER")
DB_HOST = os.getenv("DB_HOST", "localhost")

# URL de conexión para PostgreSQL
URL_DATABASE = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,bind=engine)

def init_db():
    try:
        engine.connect()
        print("Conectado a la Base de Datos")
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")

    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]