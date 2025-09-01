from fastapi import APIRouter, HTTPException
from config.db import meta, engine, connection
from models.tasks import tasks
from schema.schema import Task

task = APIRouter()

@task.get("/")
async def home():
    return {"message":"Task Management using FastAPI"}

@task.get("/tasks")
async def get_tasks():
    return list(connection.execute(tasks.select()).mappings().fetchall())

@task.get("/tasks/{id}")
async def get_task(id: int):
    result = list(connection.execute(tasks.select().where(tasks.c.id == id)).mappings().fetchall())
    if not result:
        return HTTPException(status_code=404, detail="Task Not Found")
    return result
    
@task.post("/tasks")
async def new_task(task: Task):
    connection.execute(tasks.insert().values(
        title = task.title,
        description = task.description,
    ))
    connection.commit()
    return list(connection.execute(tasks.select()).mappings().fetchall())

@task.put("/tasks/{id}")
def update_task(id: int, task:Task):
    result = connection.execute(tasks.update().where(tasks.c.id == id).values(
        title = task.title,
        description = task.description,
        status = task.status
    ))
    if not result:
        return HTTPException(status_code=404, detail="Task not found")
    connection.commit()
    return list(connection.execute(tasks.select()).mappings().fetchall())

@task.delete("/tasks/{id}")
def delete_task(id: int):
    result = connection.execute(tasks.delete().where(tasks.c.id == id))
    if not result:
        return HTTPException(status_code=404, detail="Task not found")
    connection.commit()
    return list(connection.execute(tasks.select()).mappings().fetchall())