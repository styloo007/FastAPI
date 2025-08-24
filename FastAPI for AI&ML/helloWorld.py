from fastapi import FastAPI
app = FastAPI()

@app.get("/")
def helloWorld():
    return {'message':'Hello World'}

@app.get("/shashank-agasimani")
def about():
    return {'message':'Shashank Agasimani works as as AI Developer at Antlabs'}
