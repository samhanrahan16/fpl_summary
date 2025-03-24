from pydantic import BaseModel

TeamRatingType = list[dict[str, str | int]]


class Team(BaseModel):
    """Basic team and rating object."""

    team_name: str
    home_rating: int | str
    away_rating: int | str


class Teams(BaseModel):
    """Object of all teams"""

    teams: list[Team]


class TeamNames(BaseModel):
    """Team Names."""

    names: list[str]


class AccountDetails(BaseModel):
    """Username / Password."""

    email: str
    password: str
    manager_id: int
    fpl_cookie: str
    datadome_cookie: str


class CookieDetails(BaseModel):
    """Cookie Details"""

    email: str
    fpl_cookie: str
    datadome_cookie: str


class FPLAccount(BaseModel):
    """FPL Account Details."""

    fpl_email: str
    fpl_password: str


class ManagerId(BaseModel):
    """Manager ID."""

    manager_id: int
