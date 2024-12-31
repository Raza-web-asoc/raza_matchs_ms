from sqlalchemy import Table, Column, CheckConstraint
from sqlalchemy.sql.sqltypes import Integer, String
from config.db import engine, meta_data

pareja = Table("pareja", meta_data,
                Column("idmascota1", Integer, primary_key=True),
                Column("idmascota2", Integer, primary_key=True),
                CheckConstraint('idmascota1 != idmascota2', name='check_idmascota1_not_equal_idmascota2')
            )

meta_data.create_all(engine)            