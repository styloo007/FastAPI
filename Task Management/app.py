from fastapi import FastAPI
from routes.app import task
from config.db import meta, engine

meta.create_all(engine)

app = FastAPI()

app.include_router(task)

