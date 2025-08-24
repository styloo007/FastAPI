from typing import Optional,List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from enum import Enum

app = FastAPI(
    title="A Simple To-Do Application",
    description="A Simple To-Do Application to learn FastAPI",
    version="1.0.0"
)

class Priority(str, Enum):
    low = "Low"
    medium = "medium"
    high = "high"

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

