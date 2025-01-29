from pydantic import BaseModel

class MatchSchema(BaseModel):
    idmascota1: int
    idmascota2: int
    estado: str

class InteraccionSchema(BaseModel):
    id_mascota1: int
    id_mascota2: int
    tipo_interaccion: str

