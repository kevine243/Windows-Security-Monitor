from fastapi import APIRouter
from app.database.db import get_db
from sqlalchemy.orm import Session
from app.schemas.schemas import LogEntry,LogResponse
from fastapi import Depends
from app.services.logs_service import get_all_logs,post_failed_login,post_successful_login
logs_router = APIRouter()

@logs_router.post("/failed_login")
def failed_login(data:LogEntry,db: Session = Depends(get_db)):
    return post_failed_login(db,data)    

@logs_router.post("/successful_login")
def successful_login(data:LogEntry,db: Session = Depends(get_db)):
    return post_successful_login(db,data)

@logs_router.get("/logs", response_model=LogResponse)
def get_all(db: Session = Depends(get_db)):
    logs = get_all_logs(db)
    return {"data": logs, "total": len(logs)}


