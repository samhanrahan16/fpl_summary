from enum import StrEnum


class FPLEndpoints(StrEnum):
    """FPL Endpoints."""

    LOGIN = "https://users.premierleague.com/accounts/login/"
    FIXTURES = "https://fantasy.premierleague.com/api/fixtures"
    STATIC = "https://fantasy.premierleague.com/api/bootstrap-static"
    TEAM = "https://fantasy.premierleague.com/api/my-team/"
