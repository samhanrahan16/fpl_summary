import aiohttp
from fpl import FPL
from fpl.models import User
import pandas as pd
from sqlalchemy.orm import Session
from typing import cast

from db.player_data import PlayerData
from db.login import Users
from fpl_client.client import AsyncRunner

MyTeamType = dict[str, int | bool]


class MissingPlayerException(Exception):
    """Missing Player Exception."""


class MyTeam:
    """Runs the methods needed from the FPL python package
    which must be run via async. This will mainly be used to
    get my own team."""

    def __init__(self, db: Session, email: str, fpl_password: str) -> None:

        self.async_runner = AsyncRunner()
        user = db.query(Users).filter(Users.email == email).one()
        self.cookie = f"datadome={user.datadome};pl_profile={user.cookie}"
        self.email = email
        self.password = fpl_password
        self.manager_id = user.manager_id
        self.session = self.async_runner.run(self._create_session())
        self.user = self.login(
            self.async_runner,
            self.session,
            email,
            self.password,
            self.manager_id,
            self.cookie,
        )

    def __del__(self):
        """Ensure the session is closed when the object is deleted."""
        self.async_runner.run(self.session.close())

    @staticmethod
    async def _create_session() -> aiohttp.ClientSession:
        return aiohttp.ClientSession()

    @staticmethod
    def login(
        async_runner: AsyncRunner,
        session: aiohttp.ClientSession,
        email: str,
        password: str,
        manager_id: int,
        cookie: str,
    ) -> User:
        """Login to the FPL account."""

        async def _login() -> User:
            fpl = FPL(session)
            await fpl.login(email=email, password=password, cookie=cookie)
            return await fpl.get_user(manager_id)

        return async_runner.run(_login())

    @property
    def my_team(self) -> list[dict[str, int | bool]]:
        """Get back my team JSON."""

        async def _my_team() -> dict[str, int | bool]:
            return await self.user.get_team()

        return self.async_runner.run(_my_team())


# Need to add into the player table the position which is element type.
# Then need to combine with the team fixture table to produce the full table
# of their fixtures and difficulties.
def create_team_table(db: Session, my_team: list[MyTeamType]) -> pd.DataFrame:
    """Takes in my team and generates a table of player names and fixtures."""
    element_type_key = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}
    player_ids: list[int] = []
    player_positions: dict[int, int] = {}
    subs: dict[int, str] = {}
    for player in my_team:
        element = cast(int, player["element"])
        element_type = cast(int, player["element_type"])
        player_ids.append(cast(int, player["element"]))
        player_positions[element] = element_type
        if player["multiplier"] == 0:
            subs[element] = "SUB"
        elif player["multiplier"] > 1:
            subs[element] = "CAP"
        else:
            subs[element] = "START"
    team = db.query(PlayerData).filter(PlayerData.fpl_id.in_(player_ids)).all()

    # Ensure that we get back correct number of players from db
    if len(team) != len(player_ids):
        raise MissingPlayerException(
            "A player has not been found please re-download the player data."
        )

    team_table = pd.DataFrame.from_records(
        [
            {
                "id": player.fpl_id,
                "name": f"{player.first_name} {player.second_name}",
                "position": element_type_key[player_positions[player.fpl_id]],
                "starting": subs[player.fpl_id],
                "team_id": player.team_id,
                "xG": player.expected_goals,
                "xA": player.expected_assists,
                "form": player.form,
                "total_points": player.total_points,
            }
            for player in team
        ]
    )
    custom_order = ["GKP", "DEF", "MID", "FWD"]
    team_table["position"] = pd.Categorical(
        team_table["position"], categories=custom_order, ordered=True
    )
    return team_table.sort_values(by="position")
