from sqlalchemy import Column, Integer, String
from database import Base  # type: ignore


class TeamData(Base):  # type: ignore
    __tablename__ = "team_data"

    id = Column(Integer, primary_key=True, index=True)
    fpl_id = Column(Integer, nullable=False)
    fpl_code = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)
    short_name = Column(String(50), nullable=False)

    def __repr__(self):
        return (
            f"<Team(name={self.name}, short_name={self.short_name}, "
            f"fpl_id={self.fpl_id})>"
        )
