from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey, UniqueConstraint, event
from sqlalchemy.sql import func
from config.base_class import Base

class Interaccion(Base):
    __tablename__ = 'interacciones'

    id_interaccion = Column(Integer, primary_key=True, autoincrement=True)
    id_mascota1 = Column(Integer, nullable=False, comment='Mascota que da el swipe')
    id_mascota2 = Column(Integer, nullable=False, comment='Mascota que recibe el swipe')
    tipo_interaccion = Column(Enum('like', 'dislike', name='tipo_interaccion_enum'), nullable=False, comment='Tipo de interacción')
    fecha_interaccion = Column(DateTime, server_default=func.now(), comment='Fecha de la interacción')


