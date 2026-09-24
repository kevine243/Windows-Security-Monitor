from pydantic import BaseModel,ConfigDict

class LogEntry(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    event_id: int
    time: str
    inserts: list[str]
class LogResponse(BaseModel):
    data: list[LogEntry]
    total: int
