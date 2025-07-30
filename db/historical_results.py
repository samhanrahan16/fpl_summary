from sqlalchemy import Column, Float, Integer

from database import Base


class HistoricalResults(Base):
    __tablename__ = "historical_results"

    id = Column(Integer, primary_key=True, index=True)
    season = Column(Integer, nullable=False)
    team_h = Column(Integer, nullable=False)
    team_a = Column(Integer, nullable=False)
    team_h_score = Column(Integer, nullable=False)
    team_a_score = Column(Integer, nullable=False)
    team_h_xg: float = Column(Float, nullable=False)  # type: ignore
    team_a_xg: float = Column(Float, nullable=False)  # type: ignore
