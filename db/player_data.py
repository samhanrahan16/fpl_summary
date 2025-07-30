from sqlalchemy import Column, Float, Integer, String

from database import Base


class PlayerData(Base):
    __tablename__ = "player_data"

    id = Column(Integer, primary_key=True, index=True)
    fpl_id = Column(Integer, nullable=False)
    fpl_code = Column(Integer, nullable=False)
    team_id = Column(Integer, nullable=False)
    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    position = Column(String(10), nullable=False)
    chance_of_playing: float = Column(Float, nullable=False)  # type: ignore
    form: float = Column(Float, nullable=False)  # type: ignore
    total_points = Column(Integer, nullable=False)
    goals = Column(Integer, nullable=False)
    assists = Column(Integer, nullable=False)
    clean_sheets = Column(Integer, nullable=False)
    goals_conceeded = Column(Integer, nullable=False)
    penalties_saved = Column(Integer, nullable=False)
    penalties_missed = Column(Integer, nullable=False)
    yellow_cards = Column(Integer, nullable=False)
    red_cards = Column(Integer, nullable=False)
    saves = Column(Integer, nullable=False)
    bonus_points = Column(Integer, nullable=False)
    starts = Column(Integer, nullable=False)
    expected_goals: float = Column(Float, nullable=False)  # type: ignore
    expected_assists: float = Column(Float, nullable=False)  # type: ignore
    expected_goals_conceeded: float = Column(Float, nullable=False)  # type: ignore
    expected_goal_involvments: float = Column(Float, nullable=False)  # type: ignore

    def __repr__(self) -> str:
        return f"<Team(first_name={self.first_name}, surname={self.second_name} "
