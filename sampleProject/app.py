from fastapi import FastAPI
from fastapi.responses import PlainTextResponse,HTMLResponse,JSONResponse

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Sample Docker with FastAPI"}

@app.get("/multiplier/{num}", response_class=PlainTextResponse)
def multiplier(num: int):
    returnStr = ""
    for i in range(1,11):
        prod = num*i
        returnStr += f"{num}*{i}={prod}\n"
        
    
    return returnStr
        