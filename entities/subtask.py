from sqlalchemy import Column, Integer, String, Boolean, DATETIME, text
from database.core import Base

class Subtask(Base):
    __tablename__ = "subtasks"

    id_subtask = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    is_completed = Column(Boolean, server_default='0', nullable=False)
    id_task = Column(Integer, nullable=False)
    created_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
