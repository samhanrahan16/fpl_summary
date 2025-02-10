import datetime
from fastapi import FastAPI, Depends
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from typing import cast, Any

from API.models import (
    Teams,
    TeamNames,
    TeamRatingType,
    AccountDetails,
    CookieDetails,
    FPLAccount,
)
from API.team_rating import check_team_data, write_team_data
from API.utils import get_existing_user, create_difficulty_table
from database import get_db
from db.login import Users
from fpl_client.client import FPLClient
from fpl_engine.core import FPlDetailTypes
from fpl_engine.fixtures import FPLFixtures
from fpl_engine.my_team import MyTeam, create_team_table
from fpl_engine.static import FPLStatic

app = FastAPI()

FixturesType = list[dict[str | int, str | int]]

TeamDifficultyType = Any  # Replace with actual type when known


@app.post("/create_account")
def create_account(
    account_details: AccountDetails, db: Session = Depends(get_db)
) -> str:
    password_hash = bcrypt.hash(account_details.password)
    existing_user = get_existing_user(db, account_details.email)
    if existing_user:
        return f"Account already exists for user {account_details.email}"

    try:
        new_user = Users(
            email=account_details.email,
            password_hash=password_hash,
            manager_id=account_details.manager_id,
            cookie=account_details.fpl_cookie,
            datadome=account_details.datadome_cookie,
            created_at=datetime.datetime.now(),
        )
        db.add(new_user)
        db.commit()
        return "Account succesfully created"
    except Exception:
        return "Failed to create account"


@app.put("/change_cookie")
def change_cookie(cookie_details: CookieDetails, db: Session = Depends(get_db)) -> str:
    existing_user = get_existing_user(db, cookie_details.email)
    if not existing_user:
        return f"No account exists for {cookie_details.email} please create account."

    existing_user.cookie = cookie_details.fpl_cookie  # type: ignore
    existing_user.datadome = cookie_details.datadome_cookie  # type: ignore

    db.add(existing_user)
    db.commit()
    return "Succesfully changed cookie data."


@app.get("/teams/rating")
def get_ratings(
    db: Session = Depends(get_db), team_names: TeamNames | None = None
) -> TeamRatingType:
    return check_team_data(db, team_names)


@app.put("/teams/rating")
def update_ratings(teams: Teams, db: Session = Depends(get_db)) -> TeamRatingType:
    write_team_data(db, teams)
    team_names = TeamNames(names=[team.name for team in teams.teams])
    return check_team_data(db, team_names)


@app.post("/teams/rating")
def create_ratings(teams: Teams, db: Session = Depends(get_db)) -> TeamRatingType:
    write_team_data(db, teams, update_existing=False)
    team_names = TeamNames(names=[team.name for team in teams.teams])
    return check_team_data(db, team_names)


@app.post("/fpl/update/fixtures")
def update_fpl_fixtures(db: Session = Depends(get_db)) -> str:
    fpl_client = FPLClient()
    static_processer = FPLFixtures(db)
    try:
        static_processer.refresh_detail(db, fpl_client, FPlDetailTypes.FIXTURES)
        static_processer.process_static_data()
        return "Succesfully processed fixtures"
    except Exception as e:
        return f"Exception ocurred updating fixtures: {e}"


# add api for getting back the fixtures
# this should return a pandas dataframe in JSON format
# This should be teams as rows with fixtures as columns and then
# difficulty of next fixture next 3 / 6 / 10.
# A similar table will be presented for your team so this should use
# a generic function that produces the pandas dataframe.


@app.get("/fixtures/table")
def get_fixtures_table(
    difficulty_summary_list: list[int] = [1, 3, 6, 10],
    db: Session = Depends(get_db),
) -> FixturesType:
    fixtures = create_difficulty_table(db, difficulty_summary_list)
    return cast(FixturesType, fixtures.to_dict(orient="records"))


@app.post("/update/static")
def update_static_data(db: Session = Depends(get_db)) -> str:
    static_processer = FPLStatic(db)
    fpl_client = FPLClient()
    try:
        static_processer.refresh_detail(db, fpl_client, FPlDetailTypes.STATIC)
        static_processer.process_static_data()
        return "Succesfully processed static data"
    except Exception as e:
        return f"Exception ocurred updating static data: {e}"


@app.get("/my_team/get_team")
def get_my_team(
    fpl_account: FPLAccount, db: Session = Depends(get_db)
) -> TeamDifficultyType:
    my_team = MyTeam(db, fpl_account.fpl_email, fpl_account.fpl_password)
    team_json = my_team.my_team
    team_table = create_team_table(db, team_json)
    return team_table.to_dict(orient="records")


@app.get("/my_team/fixture_difficulty")
def get_my_team_difficulty(
    fpl_account: FPLAccount,
    difficulty_summary_list: list[int] = [1, 3, 6, 10],
    summary_table: bool = True,
    db: Session = Depends(get_db),
) -> TeamDifficultyType:
    my_team = MyTeam(db, fpl_account.fpl_email, fpl_account.fpl_password)
    team_json = my_team.my_team
    team_table = create_team_table(db, team_json)
    fixtures = create_difficulty_table(db, difficulty_summary_list)
    combined_table = team_table.merge(
        fixtures, left_on="team_id", right_on="team_id", how="left"
    )
    if summary_table:
        combined_table = combined_table.drop(
            columns=[
                col
                for col in combined_table.columns
                if isinstance(col, int) or col == "Unknown"
            ]
        )
    return combined_table.to_dict(orient="records")
