import numpy as np
import pandas as pd
from sqlalchemy import delete
from sqlalchemy.orm import Session
from typing import cast

from db.fpl_detail import FPLDetail
from db.fixtures import Fixtures
from db.team_data import TeamData
from db.team_ratings import TeamRatings
from fpl_engine.core import FPlDetailTypes, HomeAway
from fpl_engine.process import ProcessFPLData

FixtureType = dict[str, int | str | bool | None]


def _create_difficulty(
    db: Session, team_id: int, default_difficulty: int, home_away: HomeAway
) -> int:
    difficulty_team = (
        db.query(TeamRatings).filter(TeamRatings.team_id == team_id).one_or_none()
    )
    if difficulty_team is None:
        difficulty = default_difficulty
    elif home_away == HomeAway.HOME:
        difficulty = difficulty_team.home_rating
    else:
        difficulty = difficulty_team.away_rating
    return difficulty


def analyse_team_fixtures(db: Session) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Analyse Team Fixtures.

    Idea here is to return the table of teams with their remaining
    fixtures and analysis of difficulty over next x number of fixtures.
    Should use difficulty rating from fpl unless we have an override set
    then it should use that difficulty.
    """
    teams = {team.id: team.short_name for team in db.query(TeamData).all()}
    fixtures = db.query(Fixtures).all()
    fixtures_table = pd.DataFrame(
        {
            "team_id": [id for id in teams.keys()],
            "Team": [short_name for short_name in teams.values()],
        }
    ).set_index("team_id")
    difficulty_table = fixtures_table.copy()
    for fixture in fixtures:
        gameweek = cast(int | None, fixture.gameweek)
        if gameweek is None:
            gameweek = "Unknown"
        if gameweek not in fixtures_table.columns:
            fixtures_table[gameweek] = None
            difficulty_table[gameweek] = None
        fixtures_table.loc[fixture.team_h, gameweek] = f"{teams[fixture.team_a]} (H)"
        fixtures_table.loc[fixture.team_a, gameweek] = f"{teams[fixture.team_h]} (A)"

        difficulty_table.loc[fixture.team_h, gameweek] = _create_difficulty(
            db, fixture.team_a, fixture.team_h_difficulty, HomeAway.AWAY
        )
        difficulty_table.loc[fixture.team_a, gameweek] = _create_difficulty(
            db, fixture.team_h, fixture.team_a_difficulty, HomeAway.HOME
        )

    return fixtures_table, difficulty_table


def difficulty_summary(
    difficulty_table: pd.DataFrame, x: int | None = None
) -> list[float]:
    """Difficulty Summary

    Tables a table of difficulties for each fixture and returns a summary
    of the average difficulty for each team over the next x fixtures. If x
    is None then we will take the average over all fixtures.
    """
    results: list[float] = []
    difficulty_table.drop("Unknown", axis=1)
    for index in difficulty_table.index:  # type: ignore
        row: pd.Series[int] = difficulty_table.loc[index]  # type: ignore
        numeric_row = pd.to_numeric(row, errors="coerce")  # type: ignore
        final_row: list[float] = list(numeric_row.dropna())
        if x is not None:
            final_row = final_row[:x]
        average = cast(float, np.mean(final_row))
        results.append(average)
    return results


class FPLFixtures(ProcessFPLData):

    def __init__(self, db: Session) -> None:
        super().__init__(db)

    @staticmethod
    def write_fixture(
        db: Session, fixture: FixtureType, team_dict: dict[int, int]
    ) -> Fixtures:
        """Create Fixture ORM."""
        return Fixtures(
            fpl_id=fixture["id"],
            gameweek=fixture["event"],
            team_h=team_dict[cast(int, fixture["team_h"])],
            team_a=team_dict[cast(int, fixture["team_a"])],
            team_h_difficulty=fixture["team_h_difficulty"],
            team_a_difficulty=fixture["team_a_difficulty"],
        )

    def wipe_table(self) -> None:
        """Wipes clean the fixtures table."""
        try:
            self.db.execute(delete(Fixtures))
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Error cleaning fixtures data {e}")

    def process_static_data(self) -> None:
        """Process the full static JSON."""
        static_object = cast(FPLDetail, self.get_static_object(FPlDetailTypes.FIXTURES))
        static_json = cast(list[FixtureType], static_object.fpl_data)
        self.wipe_table()
        teams_dict = {team.fpl_id: team.id for team in self.db.query(TeamData).all()}
        for fixture in static_json:
            if fixture["finished"] is False:
                fixture_orm = self.write_fixture(self.db, fixture, teams_dict)
                self.db.add(fixture_orm)
        self.db.commit()
