from fastapi import FastAPI
from app.database import engine, Base
from app.routers import game, developer

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Steam Games API", version="1.0.0")

app.include_router(game.router, prefix="/games")
app.include_router(developer.router, prefix="/developers")


@app.get("/")
def root():
    return {"message": "Welcome to the Steam Games API!"}
