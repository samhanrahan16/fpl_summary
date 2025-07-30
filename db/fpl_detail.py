from sqlalchemy import JSON, TIMESTAMP, Boolean, Column, Integer, String, func

from database import Base


class FPLDetail(Base):
    __tablename__ = "fpl_detail"

    id = Column(Integer, primary_key=True, autoincrement=True)
    detail_type = Column(String(100), nullable=False)
    fpl_data = Column(JSON, nullable=False)  # Storing JSON data
    created_at = Column(
        TIMESTAMP, default=func.now()
    )  # Automatically set to current timestamp
    record_version = Column(Integer, nullable=False)
    is_current_record = Column(Boolean, nullable=False)

    def __repr__(self) -> str:
        return f"<FPLDetail(id={self.id}, detail_type='{self.detail_type}', created_at='{self.created_at}')>"
