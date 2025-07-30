from pydantic import BaseModel

TeamRatingType = list[dict[str, str | float]]


class Team(BaseModel):
    """Basic team and rating object."""

    team_name: str
    team_id: int | None = None
    home_rating: float | str
    away_rating: float | str


class Teams(BaseModel):
    """Object of all teams"""

    teams: list[Team]


class Season(BaseModel):
    """Yeah of the season."""

    year: int


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
