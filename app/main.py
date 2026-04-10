from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import game, developer, genre, auth, stats
from app.core.rate_limit import limiter, rate_limit_handler
from slowapi.errors import RateLimitExceeded

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Steam Games API", version="1.0.0")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow localhost for frontend development
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting state and exception handler
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

app.include_router(stats.router, prefix="/stats")
app.include_router(game.router, prefix="/games")
app.include_router(developer.router, prefix="/developers")
app.include_router(genre.router, prefix="/genres")
app.include_router(auth.router, prefix="/auth")


@app.get("/")
@limiter.limit("10/minute")
def root(request: Request):
    return {
        "message": "Welcome to the Steam Games API!",
        "links": [
            {"rel": "games", "href": "/games", "method": "GET", "description": "Get all games with pagination"},
            {
                "rel": "search-games",
                "href": "/games?search={query}",
                "method": "GET",
                "description": "Search games by name",
            },
            {
                "rel": "filter-by-developer",
                "href": "/games?developer={name}",
                "method": "GET",
                "description": "Filter games by developer name",
            },
            {
                "rel": "filter-by-genre",
                "href": "/games?genre={name}",
                "method": "GET",
                "description": "Filter games by genre name",
            },
            {"rel": "game-details", "href": "/games/{id}", "method": "GET", "description": "Get specific game by ID"},
            {"rel": "developers", "href": "/developers", "method": "GET", "description": "Get all developers"},
            {
                "rel": "developer-details",
                "href": "/developers/{id}",
                "method": "GET",
                "description": "Get specific developer by ID",
            },
            {"rel": "genres", "href": "/genres", "method": "GET", "description": "Get all genres"},
            {
                "rel": "genre-details",
                "href": "/genres/{id}",
                "method": "GET",
                "description": "Get specific genre by ID",
            },
            {
                "rel": "google-login",
                "href": "/auth/google",
                "method": "GET",
                "description": "Initiate Google OAuth login",
            },
            {
                "rel": "register",
                "href": "/auth/register",
                "method": "POST",
                "description": "Register new user (development only)",
            },
            {
                "rel": "login",
                "href": "/auth/login",
                "method": "POST",
                "description": "Login with username/password (development only)",
            },
            {"rel": "docs", "href": "/docs", "method": "GET", "description": "API documentation"},
        ],
    }
