from sqlalchemy import Table, Column, CheckConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data

pareja = Table("pareja", meta_data,
                Column("idMascota1", Integer, primary_key=True),
                Column("idMascota2", Integer, primary_key=True),
                CheckConstraint('idMascota1 != idMascota2', name='check_idmascota1_not_equal_idmascota2')
            )

meta_data.create_all(engine)            