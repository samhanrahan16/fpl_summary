from sqlalchemy import Column, Integer, TIMESTAMP, String
from database import Base  # type: ignore


class Users(Base):  # type: ignore
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(50), nullable=False)
    password_hash = Column(String(50), nullable=False)
    manager_id = Column(Integer)
    cookie = Column(String(500))
    datadome = Column(String(500))
    created_at = Column(TIMESTAMP, nullable=False)
    last_login = Column(TIMESTAMP, nullable=False)
