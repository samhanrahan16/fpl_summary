from sqlalchemy.orm import Session
from typing import cast

from API.models import TeamNames, Teams
from db.team_ratings import TeamRatings
from db.team_data import TeamData


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
) -> list[dict[str, str | int]]:
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

    team_names = TeamNames(names=[team.name for team in team_ratings.teams])
    _validate_team_names(team_names.names)
    existing_teams = _query_team_ratings(db, team_names)
    existing_teams_dict = {team[1]: team[0] for team in existing_teams}
    for team in team_ratings.teams:
        new_team: TeamRatings | None = None
        if team.name in existing_teams_dict.keys():
            if update_existing:
                new_team = existing_teams_dict[team.name]
                new_team.home_rating = team.home_rating  # type: ignore
                new_team.away_rating = team.away_rating  # type: ignore
        else:
            team_id = db.query(TeamData.id).filter(TeamData.name == team.name).one()[0]
            new_team = TeamRatings(
                team_id=team_id,
                home_rating=team.home_rating,
                away_rating=team.away_rating,
            )
        if new_team:
            db.add(new_team)
    db.commit()
