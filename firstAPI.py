from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message":"Hello World"}

@app.get("/user/{name}")
def user_profile(name: str):
    return {"message":f"Welcome, {name}!"}


@app.get("/items/{item_id}")
def get_itemID(item_id: int, q:str = None):
    return {"item id":f"{item_id}", "q":f"{q}"}