from sqlalchemy import Column, Integer, String, Boolean, DATETIME, text
from database.core import Base

class User(Base):
    __tablename__ = "users"

    username = Column(String(100), primary_key=True)
    email = Column(String(100) , unique=True)
    hashed_password = Column(String(60), nullable=False)
    phone_number = Column(String(11), nullable=False , unique=True)
    created_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DATETIME, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
