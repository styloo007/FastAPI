from sqlalchemy.sql.sqltypes import Integer, String, DateTime
from sqlalchemy import Table, Column, func
from config.db import meta

tasks =  Table(
    'tasks',meta,
    Column('id', Integer, primary_key=True),
    Column('title', String(255)),
    Column('description', String(255)),
    Column('status', String(255), default="Pending"),
    Column('created_at', DateTime, server_default=func.now()),
    Column('last_updated_at', DateTime, server_default=func.now(), onupdate=func.now())
)