from uvicorn import run
from fastapi import FastAPI, APIRouter
from app.routers.logs_router import logs_router
from app.database.db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def index():
    return {"message": "Hello World"}


app.include_router(logs_router, prefix="/api/v1/logs", tags=["logs"])

if __name__ == "__main__":
    run("main:app", host="0.0.0.0", port=8000, reload=True)
