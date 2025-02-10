from sqlalchemy.orm import Session
from typing import Any, cast

from db.fpl_detail import FPLDetail
from db.team_data import TeamData
from db.player_data import PlayerData
from fpl_engine.core import FPlDetailTypes, StaticDataSections
from fpl_engine.process import ProcessFPLData


class FPLStatic(ProcessFPLData):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    @staticmethod
    def process_team_data(db: Session, team_data: list[dict[str, Any]]) -> None:
        """Process team section of static data."""
        current_team_ids = db.query(TeamData.fpl_id).all()
        current_team_ids = [id[0] for id in current_team_ids]
        for team in team_data:
            required_team_data = {
                "id": team.get("id"),
                "code": team.get("code"),
                "name": team.get("name"),
                "short_name": team.get("short_name"),
            }
            if None in list(required_team_data.values()):
                continue
            if required_team_data["id"] not in current_team_ids:
                team_data = TeamData(
                    fpl_id=required_team_data["id"],
                    fpl_code=required_team_data["code"],
                    name=required_team_data["name"],
                    short_name=required_team_data["short_name"],
                )
                db.add(team_data)
        db.commit()

    @staticmethod
    def process_player_data(
        db: Session, player_data: list[dict[str, str | int | float]]
    ) -> None:
        """Process player section of static data"""
        current_players = {
            player.fpl_id: player for player in db.query(PlayerData).all()
        }
        for player in player_data:
            player_id = cast(int, player["id"])
            if player_id not in current_players.keys():
                team_id = (
                    db.query(TeamData.id)
                    .filter(TeamData.fpl_id == player["team"])
                    .one()[0]
                )
                player_data = PlayerData(
                    fpl_id=player_id,
                    fpl_code=player["code"],
                    team_id=team_id,
                    first_name=player["first_name"],
                    second_name=player["second_name"],
                    chance_of_playing=player["chance_of_playing_next_round"],
                    form=float(player["form"]),
                    total_points=player["total_points"],
                    goals=player["goals_scored"],
                    assists=player["assists"],
                    clean_sheets=player["clean_sheets"],
                    goals_conceeded=player["goals_conceded"],
                    penalties_saved=player["penalties_saved"],
                    penalties_missed=player["penalties_missed"],
                    yellow_cards=player["yellow_cards"],
                    red_cards=player["red_cards"],
                    saves=player["saves"],
                    bonus_points=player["bonus"],
                    starts=player["starts"],
                    expected_goals=player["expected_goals_per_90"],
                    expected_assists=player["expected_assists_per_90"],
                    expected_goals_conceeded=player["expected_goals_conceded_per_90"],
                    expected_goal_involvments=player[
                        "expected_goal_involvements_per_90"
                    ],
                )
                db.add(player_data)
            else:
                player_data = current_players[player_id]
                player_data.chance_of_playing = (  # type: ignore
                    player["chance_of_playing_next_round"],
                )
                player_data.form = float(player["form"])  # type: ignore
                player_data.total_points = player["total_points"]  # type: ignore
                player_data.goals = player["goals_scored"]  # type: ignore
                player_data.assists = player["assists"]  # type: ignore
                player_data.clean_sheets = player["clean_sheets"]  # type: ignore
                player_data.goals_conceeded = player["goals_conceeded"]  # type: ignore
                player_data.penalties_saved = player["penalties_saved"]  # type: ignore
                player_data.penalties_missed = player["penalties_missed"]  # type: ignore
                player_data.yellow_cards = player["yellow_cards"]  # type: ignore
                player_data.red_cards = player["red_cards"]  # type: ignore
                player_data.saves = player["saves"]  # type: ignore
                player_data.bonus_points = player["bonus"]  # type: ignore
                player_data.starts = player["starts"]  # type: ignore
                player_data.expected_goals = player["expected_goals_per_90"]  # type: ignore
                player_data.expected_assists = player["expected_assists_per_90"]  # type: ignore
                player_data.expected_goals_conceeded = (  # type: ignore
                    player["expected_goals_conceeded_per_90"]
                )
                player_data.expected_goal_involvments = (  # type: ignore
                    player["expected_goal_involvements_per_90"]
                )
                db.add(player_data)

        db.commit()

    def process_static_data(self) -> None:
        """Process the full static JSON."""
        static_object = cast(FPLDetail, self.get_static_object(FPlDetailTypes.STATIC))
        static_json = static_object.fpl_data
        # process the team data
        self.process_team_data(self.db, static_json[StaticDataSections.TEAMS])
        # process the player data
        self.process_player_data(self.db, static_json[StaticDataSections.PLAYERS])
