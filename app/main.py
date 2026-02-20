from fastapi import FastAPI
from app.database import engine, Base
from app.models import Game, Developer, Genre

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Steam Games API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Welcome to the Steam Games API!"}
