from fastapi import FastAPI

app = FastAPI(title="Steam Games API", version="1.0.0")


@app.get("/")
def root():
    return {"message": "Welcome to the Steam Games API!"}
