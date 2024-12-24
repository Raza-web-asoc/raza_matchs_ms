from fastapi import APIRouter,Response
from schema.match_schema import MatchSchema
from config.db import engine
from model.matchs import pareja
from sqlalchemy import and_,or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import DeclarativeMeta
import json
from typing import List
from starlette.status import HTTP_204_NO_CONTENT



match=APIRouter()

@match.get("/")
def root():
    return {"message": "Hi from raza with router"}

@match.get("/api/match", response_model=List[MatchSchema])
def get_matchs():
    with engine.connect() as conn:
        matchs = conn.execute(pareja.select()).fetchall()
        result=[]
        for u in matchs:
            result.append(u._mapping)
            print(u._mapping)
        print(result)
        return result



@match.get("/api/match/{pet_id}")
def get_pet_matchs(pet_id:int, response_model=List[MatchSchema]):
    with engine.connect() as conn:
        matchs = conn.execute(pareja.select().where(or_(pareja.c.idMascota1==pet_id,pareja.c.idMascota2==pet_id ))).fetchall()
        result=[]
        for u in matchs:
            result.append(u._mapping)
            print(u._mapping)
        print(result)
        return result

@match.post("/api/match")
def create_match(data_match:MatchSchema):
    with engine.connect() as conn:
        new_match=data_match.dict()
        print(data_match)
        print(new_match)
        result = ""
        try:
            result = conn.execute(pareja.insert().values(new_match))
            conn.commit()
            print(f"Insert successful, rows affected: {result.rowcount}")
            result=f"Insert successful, rows affected: {result.rowcount}"
        except SQLAlchemyError as e:
            print(f"Error inserting data: {str(e)}")
            result=f"Error inserting data: {str(e)}"
        return result

@match.delete("/api/match/{pet_id}-{pet_id2}",status_code=HTTP_204_NO_CONTENT)
def delete_match(pet_id:int,pet_id2:int):
    with engine.connect() as conn:
        # result=
        conn.execute(pareja.delete().where(and_(pareja.c.idMascota1==pet_id,pareja.c.idMascota2==pet_id2)))
        conn.commit()
        # print(result)
    return Response(status_code=HTTP_204_NO_CONTENT)
    
