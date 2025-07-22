from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price : float
    tax : float = None
    
@app.get("/")
def helloworld():
    return {"message":"Hello world!"}

@app.post("/items")
def create_item(item: Item):
    return {"message":"Item Created", "item":item}


@app.get("/user/{name}")
def user_profile(name:str):
    return {"message":f"Welcome {name}!"}

@app.get("/items/{item_id}")
def read_item(item_id : int, q:str = None):
    return {"Item ID":item_id, "q":q}

@app.put("/items/{item_id}")
def update_item(item_id : int, item : Item ):
    return {"item_id":item_id, "Updated Item":item}

@app.put("/items/{item_id}/advanced")
def update_item_advanced(item_id:int, item:Item, q:str = None):
    result = {"item_id":item_id, **item.dict()}
    if q:
        result["query"] = q
    return result

@app.get("/items")
def listItems(item : Item):
    return {"Items":item}
