from pydantic import BaseModel, Field
from typing import Literal, Annotated
from datetime import datetime

class Task(BaseModel):
    title: Annotated[str, Field(..., description="Title of the task")]
    description: Annotated[str, Field(..., description="Description of the task")]
    status: Annotated[Literal["Pending","In-Progress","Completed"], Field(..., description="Status of the task")]
    created_at: Annotated[datetime, Field(..., description="When the task was created")]
    updated_at: Annotated[datetime, Field(..., description="When the task was last updated")]