from sqlalchemy import Column, Integer, String, Boolean, DATETIME, text
from database.core import Base

class List(Base):
    __tablename__ = "lists"

    id_list = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    id_priority = Column(Integer, nullable=False)
    created_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
