from sqlalchemy import Column, Integer, String, Boolean, DATETIME, text, event
from sqlalchemy.orm import Session

from database.core import Base

class Priority(Base):
    __tablename__ = "priorities"

    id_priority = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    created_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))

# This function will be called after the table is created
def add_default_priorities(db: Session):
    db_priorities = db.query(Priority).all()
    if len(db_priorities) == 0:
        default_priorities = [
            Priority({"title": "Low"}),
            Priority({"title": "Medium"}),
            Priority({"title": "High"}),
            Priority({"title": "Urgent"})
        ]
        db.add_all(default_priorities)
        db.commit()

