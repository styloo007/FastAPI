from pydantic import BaseModel,Field, EmailStr
from typing import List, Dict, Annotated

class User(BaseModel):
    name: Annotated[str, Field(..., title="Name of the User")]
    email: Annotated[EmailStr, Field(..., title="Email ID of the User")]
    password: Annotated[str, Field(..., title="Password to SignUp/Login")]