from sqlalchemy import Column, Float, Integer

from database import Base


class TeamRatings(Base):
    __tablename__ = "team_ratings"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    home_rating: float = Column(Float, nullable=False)  # type: ignore
    away_rating: float = Column(Float, nullable=False)  # type: ignore

    def __repr__(self) -> str:
        return (
            f"<Team(team_id={self.team_id}, home_rating={self.home_rating}, "
            f"away_rating={self.away_rating})>"
        )
