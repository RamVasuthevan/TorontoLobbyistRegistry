from datetime import date
from app import db
from sqlalchemy.orm import validates
from enum import Enum


def get_type_error_message(variable_name: str, expected_type: str, variable_value) -> str:
    return f"{variable_name} must be {expected_type}, got {variable_value} of type {type(variable_value).__name__}"


def get_enum_error_message(variable_name: str, enum_name: str, variable_value) -> str:
    return f"{variable_name} must be one of {', '.join([e.value for e in enum_name])}, got {variable_value}"


class LobbyingReportStatus(Enum):
    ACTIVE = 'Active'
    CLOSED = 'Closed'
    CLOSED_BY_LRO = 'Closed by LRO'


class LobbyingReportType(Enum):
    CONSULTANT = 'Consultant'
    IN_HOUSE = 'In-house'
    VOLUNTARY = 'Voluntary'


class LobbyingReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smnumber = db.Column(db.String, unique=True)
    status = db.Column(db.Enum(LobbyingReportStatus))
    type = db.Column(db.Enum(LobbyingReportType))
    subject_matter = db.Column(db.String)
    particulars = db.Column(db.String)
    proposed_start_date = db.Column(db.Date, nullable=True)
    proposed_end_date = db.Column(db.Date, nullable=True)
    initial_approval_date = db.Column(db.Date)
    effective_date = db.Column(db.Date)

    @validates('smnumber')
    def validate_smnumber(self, key, smnumber):
        if not isinstance(smnumber, str):
            raise ValueError(get_type_error_message(smnumber, str.__name__, smnumber))

        if len(smnumber) != 7 or not smnumber.startswith('SM') or not smnumber[2:].isdigit():
            raise ValueError(f"smnumber must start with 'SM' and followed by 5 digits, got {smnumber}")

        return smnumber

    @validates('status')
    def validate_status(self, key, status):
        if not isinstance(status, LobbyingReportStatus):
            raise ValueError(get_enum_error_message("status", LobbyingReportStatus, status))

        return status

    @validates('type')
    def validate_type(self, key, type):
        if not isinstance(type, LobbyingReportType):
            raise ValueError(get_enum_error_message("type", LobbyingReportType, type))

        return type

    @validates('proposed_start_date')
    def validate_proposed_start_date(self, key, proposed_start_date):
        if proposed_start_date is not None and not isinstance(proposed_start_date, date):
            raise ValueError(get_type_error_message('proposed_start_date', date.__name__, proposed_start_date))

        if self.proposed_end_date is not None and proposed_start_date is not None and proposed_start_date > self.proposed_end_date:
            raise ValueError(f"proposed_start_date {proposed_start_date} must be on or before proposed_end_date {self.proposed_end_date}")

        return proposed_start_date

    @validates('proposed_end_date')
    def validate_proposed_end_date(self, key, proposed_end_date):
        if proposed_end_date is not None and not isinstance(proposed_end_date, date):
            raise ValueError(get_type_error_message('proposed_end_date', date.__name__, proposed_end_date))

        if self.proposed_start_date is not None and proposed_end_date is not None and proposed_end_date < self.proposed_start_date:
            raise ValueError(f"proposed_end_date {proposed_end_date} must be on or after proposed_start_date {self.proposed_start_date}")

        return proposed_end_date

    @validates('initial_approval_date')
    def validate_initial_approval_date(self, key, initial_approval_date):
        if not isinstance(initial_approval_date, date):
            raise ValueError(get_type_error_message('initial_approval_date', date.__name__, initial_approval_date))

        if self.effective_date is not None and initial_approval_date > self.effective_date:
            raise ValueError(f"initial_approval_date {initial_approval_date} must be before or the same as effective_date {self.effective_date}")

        return initial_approval_date

    @validates('effective_date')
    def validate_effective_date(self, key, effective_date):
        if not isinstance(effective_date, date):
            raise ValueError(get_type_error_message('effective_date', date.__name__, effective_date))

        if self.initial_approval_date is not None and effective_date < self.initial_approval_date:
            raise ValueError(f"effective_date {effective_date} must be on or after initial_approval_date {self.initial_approval_date}")

        return effective_date
