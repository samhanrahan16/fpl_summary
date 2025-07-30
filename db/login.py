from sqlalchemy import TIMESTAMP, Column, Integer, String

from database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), nullable=False)
    password_hash = Column(String(50), nullable=False)
    manager_id = Column(Integer, nullable=False)
    cookie = Column(String(500))
    datadome = Column(String(500))
    created_at = Column(TIMESTAMP, nullable=False)
    last_login = Column(TIMESTAMP, nullable=False)
