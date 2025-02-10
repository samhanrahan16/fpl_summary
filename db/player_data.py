from sqlalchemy import Column, Integer, String, Float
from database import Base  # type: ignore


class PlayerData(Base):  # type: ignore
    __tablename__ = "player_data"

    id = Column(Integer, primary_key=True, index=True)
    fpl_id = Column(Integer, nullable=False)
    fpl_code = Column(Integer, nullable=False)
    team_id = Column(Integer, nullable=False)
    first_name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    position = Column(String(10), nullable=False)
    chance_of_playing = Column(Float, nullable=False)
    form = Column(Float, nullable=False)
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
    expected_goals = Column(Float, nullable=False)
    expected_assists = Column(Float, nullable=False)
    expected_goals_conceeded = Column(Float, nullable=False)
    expected_goal_involvments = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Team(first_name={self.first_name}, surname={self.second_name} "
