import pandas as pd
from sqlalchemy.orm import Session

from db.login import Users
from fpl_engine.fixtures import analyse_team_fixtures, difficulty_summary


def get_existing_user(db: Session, email: str) -> Users | None:
    """Get current User."""
    return db.query(Users).filter(Users.email == email).one_or_none()


def create_difficulty_table(
    db: Session, difficulty_summary_list: list[int]
) -> pd.DataFrame:
    fixtures, difficulties = analyse_team_fixtures(db)
    for n in difficulty_summary_list:
        fixtures[f"Difficulty Next {n} Fixtures"] = difficulty_summary(difficulties, n)
    fixtures["Difficulty All Remaining Fixtures"] = difficulty_summary(difficulties)
    return fixtures.round(3)
