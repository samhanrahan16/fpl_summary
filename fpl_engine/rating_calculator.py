import datetime
from dataclasses import dataclass
from typing import cast

import numpy as np
import numpy.typing as npt
import pandas as pd
from sqlalchemy.orm import Session

from db.historical_results import HistoricalResults


def create_results_table(db: Session) -> pd.DataFrame:
    """Create Results Table.

    Create a pandas dataframe of results for the past 3 seasons.
    """
    current_date = datetime.datetime.now()
    if current_date.month < 8:
        season = current_date.year - 1
    else:
        season = current_date.year

    fixtures = (
        db.query(HistoricalResults).filter(HistoricalResults.season >= season - 3).all()
    )

    results_table = pd.DataFrame([row.__dict__ for row in fixtures])
    results_table.drop(columns=["_sa_instance_state"], inplace=True)
    return results_table


def calculate_difficulty_scores(
    historical_fixtures: pd.DataFrame, teams_dict: dict[str, int]
) -> dict[int, tuple[float, float]]:
    """Calculate the difficulty score for each team.

    Calculate the Z score and then difficulty for each team.
    Return a dict as per below:

    {team_id: (difficulty_home, difficulty_away)}
    """
    expected_points_home = {}
    expected_points_away = {}
    for team_id in teams_dict.values():
        rating_calculator_home = RatingCalculator(
            team_id=team_id, result_table=historical_fixtures
        )
        rating_calculator_away = RatingCalculator(
            team_id=team_id, result_table=historical_fixtures, is_home_team=False
        )
        # TODO: When a team has never been in the prem before / no data we need to assign them
        # a rating. For now lets default this to 5 / 3.
        if rating_calculator_home.n_fixtures == 0:
            expected_points_home[team_id] = 1.3
            expected_points_away[team_id] = 0.8

        else:
            expected_points_home[team_id] = rating_calculator_home.expected_points
            expected_points_away[team_id] = rating_calculator_away.expected_points

    all_ep_home: npt.NDArray[np.float64] = np.array(list(expected_points_home.values()))
    all_ep_away: npt.NDArray[np.float64] = np.array(list(expected_points_away.values()))

    def _calculate_difficulty(
        expected_points: npt.NDArray[np.float64],
    ) -> npt.NDArray[np.float64]:
        z_score = (expected_points - expected_points.mean()) / expected_points.std()
        return cast(
            npt.NDArray[np.float64], 5 + 4 * (z_score / np.max(np.abs(z_score)))
        )

    difficulty_scores_home = _calculate_difficulty(all_ep_home)
    difficulty_scores_away = _calculate_difficulty(all_ep_away)
    return {
        team_id: (difficulty_home, difficulty_away)
        for team_id, difficulty_home, difficulty_away in zip(
            teams_dict.values(), difficulty_scores_home, difficulty_scores_away
        )
    }


def update_team_difficulties(
    db: Session, difficulties_dict: dict[int, tuple[float, float]]
) -> None:
    """Update the team ratings table with the updated difficulties calculations."""


@dataclass
class RatingCalculator:
    """Rating Calculator Class.

    For each team calculate the properties required to determine their
    team rating.

    We calculate the team rating as per below:

    Step 1: Expected points
    EP = 3P(W) + 1P(D) + 0P(L)

    Step 2: Z-score
    Z = (EP - u) / s
    u = mean EP
    s = standard deviation of EP

    Step 3: Compute difficulty
    Difficulty = 5 + 5 * Z / max|Z|
    """

    team_id: int
    result_table: pd.DataFrame
    is_home_team: bool = True

    @property
    def fixtures(self) -> pd.DataFrame:
        """Get the fixtures."""
        if self.is_home_team:
            return self.result_table[self.result_table.team_h == self.team_id]
        else:
            return self.result_table[self.result_table.team_a == self.team_id]

    @property
    def n_fixtures(self) -> int:
        return len(self.fixtures)

    @property
    def total_wins(self) -> int:
        """Calculate total number of home wins."""
        if self.is_home_team:
            wins = self.fixtures[
                self.fixtures.team_h_score > self.fixtures.team_a_score
            ]
        else:
            wins = wins = self.fixtures[
                self.fixtures.team_a_score > self.fixtures.team_h_score
            ]
        return len(wins)

    @property
    def total_draws(self) -> int:
        """Calculate the total number of home draws."""
        draws = self.fixtures[self.fixtures.team_h_score == self.fixtures.team_a_score]
        return len(draws)

    @property
    def win_probability(self) -> float:
        """Probability of winning at home."""
        return self.total_wins / self.n_fixtures

    @property
    def draw_probability(self) -> float:
        """Probability of drawing home."""
        return self.total_draws / self.n_fixtures

    @property
    def expected_points(self) -> float:
        """Calculated the expected points at home."""
        return 3 * self.win_probability + self.draw_probability

    # @property
    # def z_score(self) -> float:
    #     """Calculate the Z score of home results."""
    #     return (
    #         self.expected_points - self.mean_expected_points
    #     ) / self.standard_dev_expected_points

    # @property
    # def difficulty_score(self) -> float:
    #     """Calculate the difficulty score."""
    #     return 5 + (self.z_score / self.max_z_score)
