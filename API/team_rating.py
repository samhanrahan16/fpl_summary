import json
import re
from typing import cast

from bs4 import BeautifulSoup
from sqlalchemy.orm import Session

from API.models import TeamNames, Teams
from db.historical_results import HistoricalResults
from db.team_data import TeamData
from db.team_ratings import TeamRatings
from fpl_client.client import FPLClient

SeasonResultsType = list[dict[str, bool | str | dict[str, str]]]


class MissingTeamException(Exception):
    """Missing Team Exception."""


def _query_team_ratings(
    db: Session, team_names: TeamNames
) -> list[tuple[TeamRatings, str]]:
    return cast(
        list[tuple[TeamRatings, str]],
        (
            db.query(TeamRatings, TeamData.name)
            .join(TeamRatings, TeamRatings.team_id == TeamData.id)
            .filter(TeamData.name.in_(team_names.names))
            .all()
        ),
    )


def check_team_data(
    db: Session, team_names: TeamNames | None = None
) -> list[dict[str, str | float]]:
    """Check existing team data."""

    if not team_names:
        teams = cast(
            list[tuple[TeamRatings, str]],
            (
                db.query(TeamRatings, TeamData.name)
                .join(TeamRatings, TeamRatings.team_id == TeamData.id)
                .all()
            ),
        )
    else:
        teams = _query_team_ratings(db, team_names)

    return [
        {
            "team_name": team[1],
            "home_rating": team[0].home_rating,
            "away_rating": team[0].away_rating,
        }
        for team in teams
    ]


def write_team_data(
    db: Session, team_ratings: Teams, update_existing: bool = True
) -> None:
    """Write team data to DB."""

    def _validate_team_names(team_names: list[str]) -> None:
        all_teams: set[str] = set(
            [team_name[0] for team_name in db.query(TeamData.name).all()]
        )
        mismatch_names = [team for team in team_names if team not in all_teams]
        if mismatch_names:
            raise MissingTeamException(
                f"The following teams don't exist {mismatch_names}. "
                f"Only teams from the following list can be added / updated "
                f"{list(all_teams)}"
            )

    team_names = TeamNames(names=[team.team_name for team in team_ratings.teams])
    _validate_team_names(team_names.names)
    existing_teams = _query_team_ratings(db, team_names)
    existing_teams_dict = {team[1]: team[0] for team in existing_teams}
    for team in team_ratings.teams:
        new_team: TeamRatings | None = None
        if team.team_name in existing_teams_dict.keys():
            if update_existing:
                new_team = existing_teams_dict[team.team_name]
                new_team.home_rating = int(team.home_rating)
                new_team.away_rating = int(team.away_rating)
        else:
            team_id = (
                db.query(TeamData.id).filter(TeamData.name == team.team_name).one()[0]
            )
            new_team = TeamRatings(
                team_id=team_id,
                home_rating=int(team.home_rating),
                away_rating=int(team.away_rating),
            )
        if new_team:
            db.add(new_team)
    db.commit()


def write_team_ratings(
    db: Session, diffculty_scores: dict[int, tuple[float, float]]
) -> None:
    """Write Team Ratings.

    Take a set of calculated team scores related to their ID and write them into the
    TeamRatings table.
    """
    existing_rating = (
        db.query(TeamRatings)
        .filter(TeamRatings.team_id.in_(list(diffculty_scores.keys())))
        .all()
    )
    existing_rating_ids = []
    for team in existing_rating:
        team.home_rating = diffculty_scores[team.team_id][0]  # type: ignore
        team.away_rating = diffculty_scores[team.team_id][1]  # type: ignore
        existing_rating_ids.append(team.team_id)
        db.add(team)

    for team_id, score in diffculty_scores.items():
        if team_id not in existing_rating_ids:
            team_rating = TeamRatings(
                team_id=team_id, home_rating=score[0], away_rating=score[1]
            )
            db.add(team_rating)

    db.commit()


def get_teams_dict(db: Session) -> dict[str, int]:
    """Dictionary of teams.

    Return a dictionary mapping the teams short name
    to the id of the team.
    """
    teams = db.query(TeamData).all()
    return {cast(str, team.short_name): cast(int, team.id) for team in teams}


def get_seasons_results(year: int, fpl_client: FPLClient) -> SeasonResultsType:
    """Get Historical Season Results.

    Scrapes data from the understat website to get back historical result data for
    a specified season.
    """

    endpoint = f"https://understat.com/league/EPL/{year}"

    response = cast(str, fpl_client.get_data(endpoint))
    soup = BeautifulSoup(response, "html.parser")
    script_text = ""
    for script in soup.find_all("script"):
        if "datesData" in script.text:
            script_text = script.text
            break

    match = re.search(r"datesData\s*=\s*JSON\.parse\('(.+?)'\)", script_text)
    if match:
        json_text = match.group(1)
        json_text = json_text.encode().decode("unicode_escape")

        return cast(SeasonResultsType, json.loads(json_text))
    else:
        raise Exception(
            f"Understat did not contain the desired section for season {year}"
        )


def save_results(
    db: Session,
    understat_results: list[dict[str, bool | str | dict[str, str]]],
    year: int,
    teams_dict: dict[str, int],
    understat_map: dict[str, str],
) -> None:
    """Save the understat results to the database.

    Take dicts from the understat library convert them into an ORM and save
    it into the database.
    """
    for result in understat_results:
        home_team = cast(dict[str, str], result["h"])
        away_team = cast(dict[str, str], result["a"])
        home_team_short_title = understat_map.get(
            home_team["short_title"], home_team["short_title"]
        )
        away_team_short_title = understat_map.get(
            away_team["short_title"], away_team["short_title"]
        )
        goals = cast(dict[str, str], result["goals"])
        xg = cast(dict[str, str], result["xG"])
        new_result = HistoricalResults(
            season=year,
            team_h=teams_dict.get(home_team_short_title, 0),
            team_a=teams_dict.get(away_team_short_title, 0),
            team_h_score=int(goals["h"]),
            team_a_score=int(goals["a"]),
            team_h_xg=float(xg["h"]),
            team_a_xg=float(xg["a"]),
        )
        db.add(new_result)
    db.commit()
