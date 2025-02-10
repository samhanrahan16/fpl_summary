from sqlalchemy import Column, Integer
from database import Base  # type: ignore


class TeamRatings(Base):  # type: ignore
    __tablename__ = "team_ratings"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    home_rating = Column(Integer, nullable=False)
    away_rating = Column(Integer, nullable=False)

    def __repr__(self):
        return (
            f"<Team(team_id={self.team_id}, home_rating={self.home_rating}, "
            f"away_rating={self.away_rating})>"
        )
