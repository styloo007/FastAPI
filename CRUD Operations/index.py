from fastapi import FastAPI
from config.db import meta, engine
from routes.user import user

meta.create_all(engine)

app = FastAPI()

app.include_router(user)

