from app.models.models import LogEntry as LogEntryModel
from app.schemas.schemas import LogEntry as LogEntrySchema


def get_all_logs(db):
    return db.query(LogEntryModel).all()
    
def post_failed_login(db,data: LogEntrySchema):
    log = LogEntryModel(event_id=data.event_id, time=data.time, inserts=data.inserts)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
def post_successful_login(db,data: LogEntrySchema):
    log = LogEntryModel(event_id=data.event_id, time=data.time, inserts=data.inserts)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log    