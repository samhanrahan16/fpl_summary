from abc import ABC, abstractmethod
import datetime
from sqlalchemy.orm import Session
from typing import Any

from db.fpl_detail import FPLDetail
from fpl_client.client import FPLClient
from fpl_client.endpoints import FPLEndpoints
from fpl_engine.core import detail_to_endpoint, FPlDetailTypes


class MissingDataException(Exception):
    """Exception for missing data."""


class ProcessFPLData(ABC):
    """Process FPL Data."""

    def __init__(self, db: Session) -> None:

        self.db = db

    @staticmethod
    def get_fpl_data(fpl_client: FPLClient, endpooint: FPLEndpoints) -> dict[Any, Any]:
        """Get data from FPL."""
        return fpl_client.get_data(endpooint)

    @staticmethod
    def query_detail_table(
        db: Session, detail_type: FPlDetailTypes
    ) -> FPLDetail | None:
        """Query the FPL Detail table for current version."""
        return (
            db.query(FPLDetail)
            .filter(
                FPLDetail.detail_type == detail_type, FPLDetail.is_current_record == 1
            )
            .one_or_none()
        )

    @classmethod
    def refresh_detail(
        cls, db: Session, fpl_client: FPLClient, detail_type: FPlDetailTypes
    ) -> None:
        """Save FPL result to detail table."""

        collect_data = True
        endpoint = detail_to_endpoint(detail_type)
        today = datetime.datetime.today().date()

        # Check that entry doesn't already exist for today
        entries = cls.query_detail_table(db, detail_type)
        if entries:
            version = entries.record_version
            current_entry_date = entries.created_at.date()
            if current_entry_date == today:
                collect_data = False
            else:
                entries.is_current_record = 0  # type: ignore
                db.add(entries)
        else:
            version = 0
        # Get the data from FPL
        if collect_data:
            fpl_data = cls.get_fpl_data(fpl_client, endpoint)
            # Save down into the db making sure versioning is correct
            # version = entries.record_version + 1
            version = version + 1
            new_detail = FPLDetail(
                detail_type=detail_type,
                fpl_data=fpl_data,
                record_version=version,
                is_current_record=True,
            )
            db.add(new_detail)
            db.commit()

    def get_static_object(self, static_type: FPlDetailTypes) -> FPLDetail | None:
        """Get Static Object.

        Check that the static object exists and return it.
        """
        static_object = self.query_detail_table(self.db, static_type)
        if not static_object:
            raise MissingDataException(
                f"Missing data for FPL data of type {static_type}"
            )
        return static_object

    @abstractmethod
    def process_static_data(self) -> None:
        """Process static FPL data into useful tables."""
        pass
