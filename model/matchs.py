from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.sql import func
from config.base_class import Base

class Pareja(Base):
    __tablename__ = 'matches'

    id_match = Column(Integer, primary_key=True, autoincrement=True)
    id_mascota1 = Column(Integer, primary_key=True, nullable=False, comment='ID de la primera mascota en el match')
    id_mascota2 = Column(Integer, primary_key=True, nullable=False, comment='ID de la segunda mascota en el match')
    fecha_inicio = Column(DateTime, server_default=func.now(), comment='Fecha en que se inició el match')
    estado = Column(Enum('pendiente', 'aceptado', 'rechazado', name='estado_match_enum'), server_default='pendiente', comment='Estado del match')

    __table_args__ = (
        CheckConstraint('id_mascota1 != id_mascota2', name='check_id_mascota1_not_equal_id_mascota2'),
    )