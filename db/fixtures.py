from sqlalchemy import TIMESTAMP, Column, Integer

from database import Base


class Fixtures(Base):
    __tablename__ = "fixtures"

    id = Column(Integer, primary_key=True, index=True)
    fpl_id = Column(Integer, nullable=False)
    gameweek = Column(Integer, nullable=True)
    kickoff_time = Column(TIMESTAMP)
    team_h = Column(Integer, nullable=False)
    team_a = Column(Integer, nullable=False)
    team_h_difficulty = Column(Integer, nullable=False)
    team_a_difficulty = Column(Integer, nullable=False)
