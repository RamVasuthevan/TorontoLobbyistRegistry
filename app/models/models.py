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
    get_invalid_postal_code_message,
)
from app.models.enums import (
    LobbyingReportStatus,
    LobbyingReportType,
    BeneficiaryType,
    FirmType,
    FirmBusinessType,
    AddressType,
    CanadianProvincesTerritories,
    MeetingCommittee,
    PublicOfficeHolderType,
    LobbyistType,
)

from app.models.processor_models import RawPOH


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
    report_id = db.Column(db.Integer, db.ForeignKey("lobbying_report.id"))
    report = db.relationship("LobbyingReport", backref="beneficiaries", lazy=True)


class Firm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(FirmType))
    name = db.Column(db.String)
    trade_name = db.Column(db.String)
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


raw_poh_publicofficeholder = db.Table(
    "raw_poh_publicofficeholder",
    db.Model.metadata,
    db.Column(
        "publicofficeholder_id",
        db.Integer,
        db.ForeignKey("public_office_holder.id"),
        primary_key=True,
    ),
    db.Column(
        "raw_poh_id",
        db.Integer,
        db.ForeignKey("raw_poh.id"),
        primary_key=True,
    ),
)


class PublicOfficeHolder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    office = db.Column(db.String)
    title = db.Column(db.String)
    type = db.Column(db.Enum(PublicOfficeHolderType))
    data_sources = db.relationship(
        "RawPOH",
        secondary=raw_poh_publicofficeholder,
    )


meeting_lobbyist = db.Table(
    "meeting_lobbyist",
    db.Model.metadata,
    db.Column("meeting_id", db.Integer, db.ForeignKey("meeting.id")),
    db.Column("lobbyist_id", db.Integer, db.ForeignKey("lobbyist.id")),
)


meeting_publicofficeholder = db.Table(
    "meeting_publicofficeholder",
    db.Model.metadata,
    db.Column("meeting_id", db.Integer, db.ForeignKey("meeting.id")),
    db.Column(
        "publicofficeholder_id", db.Integer, db.ForeignKey("public_office_holder.id")
    ),
)


class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    committee = db.Column(db.Enum(MeetingCommittee))
    date = db.Column(db.Date)
    lobbyists = db.relationship(
        "Lobbyist", secondary=meeting_lobbyist, backref="meetings"
    )
    publicofficeholders = db.relationship(
        "PublicOfficeHolder", secondary=meeting_publicofficeholder, backref="meetings"
    )
    report_id = db.Column(db.Integer, db.ForeignKey("lobbying_report.id"))
    report = db.relationship("LobbyingReport", backref="meetings", lazy=True)


raw_lobbyist_lobbyist = db.Table(
    "raw_lobbyist_lobbyist",
    db.Column(
        "raw_lobbyist_id",
        db.Integer,
        db.ForeignKey("raw_lobbyist.id"),
        primary_key=True,
    ),
    db.Column(
        "lobbyist_id", db.Integer, db.ForeignKey("lobbyist.id"), primary_key=True
    ),
)


raw_communication_lobbyist = db.Table(
    "raw_communication_lobbyist",
    db.Column(
        "raw_communication_id",
        db.Integer,
        db.ForeignKey("raw_communication.id"),
        primary_key=True,
    ),
    db.Column(
        "lobbyist_id", db.Integer, db.ForeignKey("lobbyist.id"), primary_key=True
    ),
)


class Lobbyist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lobbyist_data_sources = db.relationship(
        "RawLobbyist", secondary=raw_lobbyist_lobbyist
    )
    communication_data_sources = db.relationship(
        "RawCommunication", secondary=raw_communication_lobbyist
    )
    number = db.Column(db.String)
    first_name = db.Column(db.String)
    middle_initials = db.Column(db.String)
    last_name = db.Column(db.String)
    suffix = db.Column(db.String)
    type = db.Column(db.Enum(LobbyistType))


raw_address_address = db.Table(
    "raw_address_address",
    db.Column("address_id", db.Integer, db.ForeignKey("address.id"), primary_key=True),
    db.Column(
        "raw_address_id", db.Integer, db.ForeignKey("raw_address.id"), primary_key=True
    ),
)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_sources = db.relationship("RawAddress", secondary=raw_address_address)
    type = db.Column(db.Enum(AddressType))

    __mapper_args__ = {"polymorphic_identity": "address", "polymorphic_on": type}

    def __init__(self, *args, **kwargs):
        if type(self) is Address:
            raise TypeError(
                "Address is an abstract class and cannot be instantiated directly"
            )
        super().__init__(*args, **kwargs)


class CanadianAddress(Address):
    id = db.Column(db.Integer, db.ForeignKey("address.id"), primary_key=True)
    address_line1 = db.Column(db.String)
    address_line2 = db.Column(db.String)
    city = db.Column(db.String)
    province = db.Column(db.String)
    _country = db.Column("country", db.String, default="Canada")
    postal_code = db.Column(db.String)
    phone = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": AddressType.CANADIAN,
    }

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        raise AttributeError(
            f"'{self.__class__.__name__}' object has a fixed 'country' attribute."
        )

    def __str__(self):
        address = self.address_line1
        if self.address_line2:
            address += ", " + self.address_line2
        return f"{address}, {self.city}, {self.province}, {self.country}, {self.postal_code}"


class AmericanAddress(Address):
    id = db.Column(db.Integer, db.ForeignKey("address.id"), primary_key=True)
    address_line1 = db.Column(db.String)
    address_line2 = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    _country = db.Column("country", db.String, default="United States")
    zipcode = db.Column(db.String)
    phone = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": AddressType.AMERICAN,
    }

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, value):
        raise AttributeError(
            f"'{self.__class__.__name__}' object has a fixed 'country' attribute."
        )

    def __str__(self):
        address = self.address_line1
        if self.address_line2:
            address += ", " + self.address_line2
        return f"{address}, {self.city}, {self.state}, {self.country}, {self.zipcode}"


class OtherAddress(Address):
    id = db.Column(db.Integer, db.ForeignKey("address.id"), primary_key=True)
    raw_address_line1 = db.Column(db.String)
    raw_address_line2 = db.Column(db.String)
    raw_city = db.Column(db.String)
    raw_province = db.Column(db.String)
    raw_country = db.Column(db.String)
    raw_postal_code = db.Column(db.String)
    raw_phone = db.Column(db.String)

    __mapper_args__ = {
        "polymorphic_identity": AddressType.OTHER,
    }

    def __str__(self):
        address = self.raw_address_line1
        if self.raw_address_line2:
            address += ", " + self.raw_address_line2
        return f"{address}, {self.raw_city}, {self.raw_province}, {self.raw_country}, {self.raw_postal_code}"
