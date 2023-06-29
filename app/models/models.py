from datetime import date
from app import db
from sqlalchemy.orm import validates
from sqlalchemy import JSON
from enum import Enum
from app.models.errors import (
    get_type_error_message,
    get_enum_error_message,
    get_enum_date_must_be_before_or_equal,
    get_enum_date_must_be_after_or_equal,
    get_invalid_postal_code_message
)
from app.models.enums import (
    LobbyingReportStatus,
    LobbyingReportType,
    BeneficiaryType,
    FirmType,
    FirmBusinessType,
    AddressType,
    CanadianProvincesTerritories
)

report_beneficiary_association = db.Table(
    "report_beneficiary",
    db.Column("report_id", db.Integer, db.ForeignKey("lobbying_report.id")),
    db.Column("beneficiary_id", db.Integer, db.ForeignKey("beneficiary.id")),
)


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
    #beneficiaries = db.relationship(
    #    "Beneficiary",
    #    secondary=report_beneficiary_association,
    #    backref=db.backref("reports", lazy="dynamic"),
    #)
    # registrant_id = db.Column(db.Integer, db.ForeignKey('registrant.id'))
    # registrant = db.relationship('Registrant', back_populates='lobbying_reports')

    @validates("smnumber")
    def validate_smnumber(self, key, smnumber):
        if not isinstance(smnumber, str):
            raise ValueError(get_type_error_message(smnumber, str.__name__, smnumber))

        if (
            len(smnumber) != 7
            or not smnumber.startswith("SM")
            or not smnumber[2:].isdigit()
        ):
            raise ValueError(
                f"smnumber must start with 'SM' and followed by 5 digits, got {smnumber}"
            )

        return smnumber

    @validates("status")
    def validate_status(self, key, status):
        if not isinstance(status, LobbyingReportStatus):
            raise ValueError(
                get_enum_error_message("status", LobbyingReportStatus, status)
            )

        return status

    @validates("type")
    def validate_type(self, key, type):
        if not isinstance(type, LobbyingReportType):
            raise ValueError(get_enum_error_message("type", LobbyingReportType, type))

        return type

    @validates("proposed_start_date")
    def validate_proposed_start_date(self, key, proposed_start_date):
        if proposed_start_date is not None and not isinstance(
            proposed_start_date, date
        ):
            raise ValueError(
                get_type_error_message(
                    "proposed_start_date", date.__name__, proposed_start_date
                )
            )

        if (
            self.proposed_end_date is not None
            and proposed_start_date is not None
            and proposed_start_date > self.proposed_end_date
        ):
            raise ValueError(
                get_enum_date_must_be_before_or_equal(
                    "proposed_start_date",
                    proposed_start_date,
                    "proposed_end_date",
                    self.proposed_end_date,
                )
            )
        return proposed_start_date

    @validates("proposed_end_date")
    def validate_proposed_end_date(self, key, proposed_end_date):
        if proposed_end_date is not None and not isinstance(proposed_end_date, date):
            raise ValueError(
                get_type_error_message(
                    "proposed_end_date", date.__name__, proposed_end_date
                )
            )

        if (
            self.proposed_start_date is not None
            and proposed_end_date is not None
            and proposed_end_date < self.proposed_start_date
        ):
            raise ValueError(
                get_enum_date_must_be_after_or_equal(
                    "proposed_end_date",
                    proposed_end_date,
                    "proposed_start_date",
                    self.proposed_start_date,
                )
            )

        return proposed_end_date

    @validates("initial_approval_date")
    def validate_initial_approval_date(self, key, initial_approval_date):
        if not isinstance(initial_approval_date, date):
            raise ValueError(
                get_type_error_message(
                    "initial_approval_date", date.__name__, initial_approval_date
                )
            )

        if (
            self.effective_date is not None
            and initial_approval_date > self.effective_date
        ):
            raise ValueError(
                get_enum_date_must_be_before_or_equal(
                    "initial_approval_date",
                    initial_approval_date,
                    "effective_date",
                    self.effective_date,
                )
            )

        return initial_approval_date

    @validates("effective_date")
    def validate_effective_date(self, key, effective_date):
        if not isinstance(effective_date, date):
            raise ValueError(
                get_type_error_message("effective_date", date.__name__, effective_date)
            )

        if (
            self.initial_approval_date is not None
            and effective_date < self.initial_approval_date
        ):
            raise ValueError(
                get_enum_date_must_be_after_or_equal(
                    "effective_date",
                    effective_date,
                    "initial_approval_date",
                    self.initial_approval_date,
                )
            )

        return effective_date


class Grassroot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    target = db.Column(db.String)
    report_id = db.Column(db.Integer, db.ForeignKey("lobbying_report.id"))
    report = db.relationship("LobbyingReport", backref="grassroots", lazy=True)

    @validates("start_date")
    def validate_start_date(self, key, start_date):
        if self.end_date and start_date > self.end_date:
            raise ValueError(
                get_enum_date_must_be_before_or_equal(
                    "start_date", start_date, "end_date", self.end_date
                )
            )

        return start_date

    @validates("end_date")
    def validate_end_date(self, key, end_date):
        if self.start_date and end_date < self.start_date:
            raise ValueError(
                get_enum_date_must_be_after_or_equal(
                    "end_date", end_date, "start_date", self.start_date
                )
            )

        return end_date


class Beneficiary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(BeneficiaryType))
    name = db.Column(db.String)
    trade_name = db.Column(db.String)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    address = db.relationship("Address")
    reports = db.relationship(
        "LobbyingReport",
        secondary=report_beneficiary_association,
        backref=db.backref("beneficiaries", lazy="dynamic"),
    )

class Firm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(FirmType))
    name = db.Column(db.String)
    trade_name = db.Column(db.String)
    fiscal_start = db.Column(db.Date)
    fiscal_end = db.Column(db.Date)
    description = db.Column(db.String)
    business_type = db.Column(db.Enum(FirmBusinessType))
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))
    address = db.relationship("Address", backref="firm")
    report_id = db.Column(db.Integer, db.ForeignKey("lobbying_report.id"))
    report = db.relationship("LobbyingReport", backref="firms")


class PrivateFunding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funding = db.Column(db.String)
    contact = db.Column(db.String)
    agent = db.Column(db.String)
    agent_contact = db.Column(db.String)
    report_id = db.Column(db.Integer, db.ForeignKey("lobbying_report.id"))
    report = db.relationship("LobbyingReport", backref="private_fundings", lazy=True)


class GovernmentFunding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    government_name = db.Column(db.String)
    program = db.Column(db.String)
    report_id = db.Column(db.Integer, db.ForeignKey("lobbying_report.id"))
    report = db.relationship("LobbyingReport", backref="government_fundings", lazy=True)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address_type = db.Column(db.Enum(AddressType))
    temp_country = db.Column(db.String)
    raw_fields = db.Column(JSON)

    __mapper_args__ = {
        "polymorphic_on": "address_type",
        "polymorphic_identity": AddressType.OTHER,
    }

class CanadianAddress(Address):
    address_line1 = db.Column(db.String)
    address_line2 = db.Column(db.String)
    city = db.Column(db.String)
    province = db.Column(db.Enum(CanadianProvincesTerritories))
    country = db.Column(db.String)
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": AddressType.CANADIAN,
    }

    @validates('postal_code')
    def validate_postal_code(self, key, postal_code):
        if postal_code is None:
            return None
        
        # define the valid characters for each position
        valid_postal_first_third_chars = set('ABCEGHJKLMNPRSTVXY')
        valid_postal_chars = set('ABCEGHJKLMNPRSTVWXYZ')
        valid_digits = set('0123456789')
        valid_white_space = set(' ')

        valid_chars = [
            valid_postal_first_third_chars,  # A
            valid_digits,                    # 1
            valid_postal_chars,              # A
            valid_white_space,               # <space>
            valid_digits,                    # 1
            valid_postal_chars,              # A
            valid_digits,                    # 1
        ]

        # check if the length of postal code is correct
        if len(postal_code) != len(valid_chars):
            raise ValueError(get_invalid_postal_code_message(postal_code))

        # check if each character in the postal code is valid
        for char, valid_set in zip(postal_code, valid_chars):
            if char not in valid_set:
                raise ValueError(get_invalid_postal_code_message(postal_code))

        # if all checks pass, return the formatted postal code
        return postal_code
