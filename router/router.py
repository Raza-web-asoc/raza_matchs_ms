from fastapi import APIRouter, Response, Depends
from schema.match_schema import MatchSchema
from config.db import db_dependency
from model.matchs import Pareja
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from starlette.status import HTTP_204_NO_CONTENT
from sqlalchemy import or_ , and_


match = APIRouter()

@match.get("/")
def root():
    return {"message": "Hi from raza with router"}

@match.get("/api/match", response_model=List[MatchSchema])
def get_matchs(db: db_dependency):
    matchs = db.query(Pareja).all()
    return [MatchSchema(idmascota1=match.idmascota1, idmascota2=match.idmascota2) for match in matchs]

@match.get("/api/match/{pet_id}", response_model=List[MatchSchema])
def get_pet_matchs(db: db_dependency, pet_id: int):
    matchs = db.query(Pareja).filter(
        or_(Pareja.idmascota1 == pet_id, Pareja.idmascota2 == pet_id)
    ).all()
    return [MatchSchema(idmascota1=match.idmascota1, idmascota2=match.idmascota2) for match in matchs]

@match.post("/api/match")
def create_match(db: db_dependency, data_match: MatchSchema):
    new_match = Pareja(idmascota1=data_match.idmascota1, idmascota2=data_match.idmascota2)
    try:
        db.add(new_match)
        db.commit()
        return {"message": "Insert successful"}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"Error inserting data: {str(e)}"}

@match.delete("/api/match/{pet_id}-{pet_id2}", status_code=HTTP_204_NO_CONTENT)
def delete_match(db: db_dependency, pet_id: int, pet_id2: int):
    db.query(Pareja).filter(
        and_(Pareja.idmascota1 == pet_id, Pareja.idmascota2 == pet_id2)
    ).delete()
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)
