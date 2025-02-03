from fastapi import APIRouter, Response, Depends, HTTPException
from schema.match_schema import MatchSchema, InteraccionSchema
from config.db import db_dependency
from model.matchs import Pareja
from model.interaccion import Interaccion
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from datetime import datetime, timedelta

match = APIRouter()

def update_match_as_like_if_both_pets_gave_like(db: db_dependency, id_pet1: int, id_pet2: int):
    try:
        interaccion_pet2 = db.query(Interaccion).filter(
            Interaccion.id_mascota1 == id_pet2,
            Interaccion.id_mascota2 == id_pet1,
            Interaccion.tipo_interaccion == 'like'
        ).first()

        if interaccion_pet2:
            match_pet1 = db.query(Pareja).filter(
                Pareja.id_mascota1 == id_pet1,
                Pareja.id_mascota2 == id_pet2
            ).first()

            match_pet2 = db.query(Pareja).filter(
                Pareja.id_mascota1 == id_pet2,
                Pareja.id_mascota2 == id_pet1
            ).first()

            if match_pet1 and match_pet2:
                match_pet1.estado = 'aceptado'
                match_pet2.estado = 'aceptado'
                db.commit()
                return True
        return False
    except Exception as e:
        db.rollback()
        raise e

def update_match_as_rejected_if_dislike(db: db_dependency, id_pet1: int, id_pet2: int):
    try:
        match_pet1 = db.query(Pareja).filter(
            Pareja.id_mascota1 == id_pet1,
            Pareja.id_mascota2 == id_pet2
        ).first()

        match_pet2 = db.query(Pareja).filter(
            Pareja.id_mascota1 == id_pet2,
            Pareja.id_mascota2 == id_pet1
        ).first()

        if match_pet1 and match_pet2:
            match_pet1.estado = 'rechazado'
            match_pet2.estado = 'rechazado'
            db.commit()
        return False
    except Exception as e:
        db.rollback()
        raise e

def create_match_as_pending(db: db_dependency, id_pet1: int, id_pet2: int):
    match_pet1 = db.query(Pareja).filter(
        Pareja.id_mascota1 == id_pet1,
        Pareja.id_mascota2 == id_pet2
    ).first()

    match_pet2 = db.query(Pareja).filter(
        Pareja.id_mascota1 == id_pet2,
        Pareja.id_mascota2 == id_pet1
    ).first()

    if not match_pet1 and not match_pet2:
        new_match = Pareja(
            id_mascota1=id_pet1,
            id_mascota2=id_pet2,
            estado='pendiente'
        )
        new_match_pet2_to_pet1 = Pareja(
            id_mascota1=id_pet2,
            id_mascota2=id_pet1,
            estado='pendiente'
        )

        try:
            db.add(new_match)
            db.add(new_match_pet2_to_pet1)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

def delete_match(db: db_dependency, id_pet1: int, id_pet2: int):

    try:
        match_pet1 = db.query(Pareja).filter(
            Pareja.id_mascota1 == id_pet1,
            Pareja.id_mascota2 == id_pet2
        ).first()

        match_pet2 = db.query(Pareja).filter(
            Pareja.id_mascota1 == id_pet2,
            Pareja.id_mascota2 == id_pet1
        ).first()

        if match_pet1 and match_pet2:
            db.delete(match_pet1)
            db.delete(match_pet2)
            db.commit()

    except Exception as e:
        db.rollback()
        raise e

def create_interaccion(db: db_dependency, data_interaccion: InteraccionSchema):
    try:
        new_interaccion = Interaccion(
            id_mascota1=data_interaccion.id_mascota1,
            id_mascota2=data_interaccion.id_mascota2,
            tipo_interaccion=data_interaccion.tipo_interaccion
        )
        db.add(new_interaccion)
        db.commit()

    except Exception as e:
        db.rollback()
        raise e

def handle_repeated_interaction_between_2_pets(db: db_dependency, data_interaccion: InteraccionSchema):
    try:
        interaccion = db.query(Interaccion).filter(
            Interaccion.id_mascota1 == data_interaccion.id_mascota1,
            Interaccion.id_mascota2 == data_interaccion.id_mascota2
        ).first()

        interaccion2 = db.query(Interaccion).filter(
            Interaccion.id_mascota1 == data_interaccion.id_mascota2,
            Interaccion.id_mascota2 == data_interaccion.id_mascota1
        ).first()

        if interaccion:
            if (datetime.now() - interaccion.fecha_interaccion) < timedelta(days=10):
                return {"error": "Interaction already exists"}
            else:
                delete_match(db, data_interaccion.id_mascota1, data_interaccion.id_mascota2)
                db.delete(interaccion)
                if(interaccion2):
                    db.delete(interaccion2)
                db.commit()

        return {"message": "Interaction inserted"}

    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"Error inserting data: {str(e)}"}


@match.post("/api/swipe")
def handle_swipe(db: db_dependency, data_interaccion: InteraccionSchema):
    if data_interaccion.id_mascota1 == data_interaccion.id_mascota2:
        return {"error": "id_mascota1 and id_mascota2 must be different"}

    try:
        repeated_interaction = handle_repeated_interaction_between_2_pets(db, data_interaccion)
        if repeated_interaction.get("error"):
            return repeated_interaction
        create_interaccion(db, data_interaccion)
        create_match_as_pending(db, data_interaccion.id_mascota1, data_interaccion.id_mascota2)

        match = False
        if data_interaccion.tipo_interaccion == 'like':
            match = update_match_as_like_if_both_pets_gave_like(db, data_interaccion.id_mascota1, data_interaccion.id_mascota2)
        else:
            match = update_match_as_rejected_if_dislike(db, data_interaccion.id_mascota1, data_interaccion.id_mascota2)

        return {"message": "Interaction inserted", "match": match}
    except SQLAlchemyError as e:
        db.rollback()
        return {"error": f"Error inserting data: {str(e)}"}

@match.get("/api/match", response_model=List[MatchSchema])
def get_matchs(db: db_dependency):
    matchs = db.query(Pareja).all()
    return [MatchSchema(idmascota1=match.id_mascota1, idmascota2=match.id_mascota2, estado=match.estado) for match in matchs]

#Get endpoint to get all matchs by specific id
@match.get("/api/match/{id_pet}", response_model=List[MatchSchema])
def get_matchs_by_id(db: db_dependency, id_pet: int):
    matchs = db.query(Pareja).filter(Pareja.id_mascota1 == id_pet).all()
    return [MatchSchema(idmascota1=match.id_mascota1, idmascota2=match.id_mascota2, estado=match.estado) for match in matchs]

@match.get("/api/interaction/{id_pet}", response_model=List[InteraccionSchema])
def get_interactions_by_id(db: db_dependency, id_pet: int):
    interactions = db.query(Interaccion).filter(Interaccion.id_mascota1 == id_pet).all()
    return [InteraccionSchema(id_mascota1=interaction.id_mascota1, id_mascota2=interaction.id_mascota2, tipo_interaccion=interaction.tipo_interaccion) for interaction in interactions]