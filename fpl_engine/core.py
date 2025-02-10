from enum import StrEnum

from fpl_client.endpoints import FPLEndpoints


class HomeAway(StrEnum):
    """Home or Away team."""

    HOME = "home"
    AWAY = "away"


class FPlDetailTypes(StrEnum):
    """FPL Detail Values."""

    FIXTURES = "fixtures"
    STATIC = "static"
    PLAYERS = "players"


class StaticDataSections(StrEnum):
    """Static Data JSON Elements."""

    TEAMS = "teams"
    PLAYERS = "elements"


def detail_to_endpoint(detail: FPlDetailTypes) -> FPLEndpoints:
    """Match the detail to the endpoint."""

    match detail:
        case FPlDetailTypes.FIXTURES:
            return FPLEndpoints.FIXTURES
        case FPlDetailTypes.STATIC:
            return FPLEndpoints.STATIC
        case FPlDetailTypes.PLAYERS:
            return FPLEndpoints.TEAM
