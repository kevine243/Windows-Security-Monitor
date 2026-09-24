from sqlalchemy import Column, Integer, String, JSON
from app.database.db import Base

class LogEntry(Base):
    __tablename__ = "log_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_id = Column(Integer, index=True)
    time = Column(String)
    inserts = Column(JSON)
