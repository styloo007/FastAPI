from typing import Optional,List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from sqlalchemy import engine, MetaData, create_engine
from sqlalchemy.sql.sqltypes import Integer, String, DateTime, Boolean
from sqlalchemy import Table, Column, func

engine = create_engine("mysql+pymysql://root:root@localhost:3306/todo")
meta = MetaData()
connection = engine.connect()

todos = Table(
    'todos',meta,
    Column('id', Integer, primary_key=True),
    Column('title', String(255)),
    Column('description', String(255)),
    Column('priority', String(255)),
    Column('completed', Boolean, default=False),
    Column('created_at', DateTime, server_default= func.now()),
    Column('updated_at', DateTime, server_default= func.now(), onupdate = func.now())
)

class Priority(str, Enum):
    low = "Low"
    medium = "Medium"
    high = "High"

class TodoCreate(BaseModel):
    title:str
    description:Optional[str] = None
    priority: Priority = Priority.medium
    completed: bool = False
    
class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    priority: Priority
    completed: bool
    created_at:datetime
    updated_at:Optional[datetime] = None
    
class updatedTodo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[Priority] = None
    completed: Optional[bool] = None

meta.create_all(engine)

app = FastAPI(
    title="A Simple To-Do Application",
    description="A Simple To-Do Application to learn FastAPI",
    version="1.0.0"
)

@app.get("/")
def home():
    return {"message":"To Do List - FastAPI"}

@app.get("/todo")
def get_tasks():
    return list(connection.execute(todos.select()).mappings().fetchall())

@app.get("/todo/{id}")
def get_task(id: int):
    result = list(connection.execute(todos.select().where(todos.c.id == id)).mappings().fetchall())
    if not result:
        return HTTPException(status_code=404, detail="Task not found")
    return result

@app.post("/todo")
def add_task(todo: TodoCreate):
    connection.execute(todos.insert().values(
        title = todo.title,
        description = todo.description,
        priority = todo.priority,
    ))
    connection.commit()
    return list(connection.execute(todos.select()).mappings().fetchall())

@app.put("/todo/{id}")
def edit_task(id: int, todo: updatedTodo):
    result = connection.execute(todos.update().where(todos.c.id == id).values(
        title = todo.title,
        description = todo.description,
        priority = todo.priority,
        completed = todo.completed
    ))
    
    if not result:
        return HTTPException(status_code=404, detail="Task Not Found")
    connection.commit()
    return list(connection.execute(todos.select().where(todos.c.id == id)).mappings().fetchall())

@app.delete("/todo/{id}")
def delete_task(id: int):
    result = connection.execute(todos.delete().where(todos.c.id == id))
    if not result:
        return HTTPException(status_code=404, detail="Task Not Found")
    return list(connection.execute(todos.select()).mappings().fetchall())