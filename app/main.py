from fastapi import FastAPI
from app.database import engine, Base
from app.routers import game, developer, genre, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Steam Games API", version="1.0.0")

app.include_router(game.router, prefix="/games")
app.include_router(developer.router, prefix="/developers")
app.include_router(genre.router, prefix="/genres")
app.include_router(auth.router, prefix="/auth")


@app.get("/")
def root():
    return {
        "message": "Welcome to the Steam Games API!",
        "links": [
            {"rel": "games", "href": "/games", "method": "GET"},
            {"rel": "developers", "href": "/developers", "method": "GET"},
            {"rel": "genres", "href": "/genres", "method": "GET"},
            {"rel": "register", "href": "/auth/register", "method": "POST"},
            {"rel": "login", "href": "/auth/login", "method": "POST"},
        ],
    }
