from fastapi import APIRouter
from config.db import connection
from models.index import users
from schema.user import User

user = APIRouter()

@user.get("/")
async def home():
    return {"message":"User Management - FastAPI"}

@user.get("/users")
async def read_data():
    return list(connection.execute(users.select()).mappings().fetchall())

@user.get("/users/{id}")
async def read_data(id: int):
    return list(connection.execute(users.select().where(users.c.id == id)).mapping().fetchall())

@user.post("/users")
async def write_data(user: User):
    connection.execute(users.insert().values(
        name = user.name,
        email = user.email,
        password = user.password
    ))
    connection.commit() 
    return list(connection.execute(users.select()).mappings().fetchall())

@user.put("/users/{id}")
async def update_data(id: int, user: User):
    connection.execute(users.update().where(users.c.id == id).values(
        name=user.name,
        email=user.email,
        password=user.password
    ))
    connection.commit() 
    return list(connection.execute(users.select()).mappings().fetchall())

@user.delete("/users/{id}")
async def delete_data(id: int):
    connection.execute(users.delete().where(users.c.id == id))
    connection.commit() 
    return list(connection.execute(users.select()).mappings().fetchall())

