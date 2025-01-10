from sqlalchemy import Table, Column, CheckConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from config.base_class import Base

class Pareja(Base):
    __tablename__ = "pareja"

    idmascota1 = Column(Integer, primary_key=True)
    idmascota2 = Column(Integer, primary_key=True)

    __table_args__ = (
        CheckConstraint('idmascota1 != idmascota2', name='check_idmascota1_not_equal_idmascota2'),
    )

