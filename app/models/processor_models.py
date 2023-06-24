from datetime import date
from app import db
from sqlalchemy.orm import validates
from enum import Enum
from app.models.models import DataSource


class TempRawRegistrant(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    RegistrationNUmber = db.Column(db.String)
    RegistrationNUmberWithSoNum = db.Column(db.String)
    Status = db.Column(db.String)
    EffectiveDate = db.Column(db.String)
    Type = db.Column(db.String)
    Prefix = db.Column(db.String)
    FirstName = db.Column(db.String)
    MiddleInitials = db.Column(db.String)
    LastName = db.Column(db.String)
    Suffix = db.Column(db.String)
    PositionTitle = db.Column(db.String)
    PreviousPublicOfficeHolder = db.Column(db.String)
    PreviousPublicOfficeHoldPosition = db.Column(db.String)
    PreviousPublicOfficePositionProgramName = db.Column(db.String)
    PreviousPublicOfficeHoldLastDate = db.Column(db.String)


class RawLobbyingReport(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    SMNumber = db.Column(db.String)
    Status = db.Column(db.String)
    Type = db.Column(db.String)
    SubjectMatter = db.Column(db.String)
    Particulars = db.Column(db.String)
    InitialApprovalDate = db.Column(db.String)
    EffectiveDate = db.Column(db.String)
    ProposedStartDate = db.Column(db.String)
    ProposedEndDate = db.Column(db.String)
    registrant_id = db.Column(db.Integer, db.ForeignKey("raw_registrant.id"))
    communications = db.relationship("RawCommunication", backref="report", lazy=True)
    grassroots = db.relationship("RawGrassroot", backref="report", lazy=True)
    beneficiaries = db.relationship("RawBeneficiary", backref="report", lazy=True)
    firms = db.relationship("RawFirm", backref="report", lazy=True)
    privatefundings = db.relationship("RawPrivateFunding", backref="report", lazy=True)
    gmtfundings = db.relationship("RawGmtFunding", backref="report", lazy=True)


class RawRegistrant(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    RegistrationNUmber = db.Column(db.String)
    RegistrationNUmberWithSoNum = db.Column(db.String)
    Status = db.Column(db.String)
    EffectiveDate = db.Column(db.String)
    Type = db.Column(db.String)
    Prefix = db.Column(db.String)
    FirstName = db.Column(db.String)
    MiddleInitials = db.Column(db.String)
    LastName = db.Column(db.String)
    Suffix = db.Column(db.String)
    PositionTitle = db.Column(db.String)
    PreviousPublicOfficeHolder = db.Column(db.String)
    PreviousPublicOfficeHoldPosition = db.Column(db.String)
    PreviousPublicOfficePositionProgramName = db.Column(db.String)
    PreviousPublicOfficeHoldLastDate = db.Column(db.String)
    reports = db.relationship("RawLobbyingReport", backref="registrant", lazy=True)
    address_id = db.Column(db.Integer, db.ForeignKey("raw_address.id"))
    address = db.relationship("RawAddress", backref="raw_registrant")


class RawCommunication(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    POH_Office = db.Column(db.String)
    POH_Type = db.Column(db.String)
    POH_Position = db.Column(db.String)
    POH_Name = db.Column(db.String)
    CommunicationsMethod = db.Column(db.String)
    CommunicationDate = db.Column(db.String)
    CommunicationGroupId = db.Column(db.String)
    LobbyistNumber = db.Column(db.String)
    LobbyistType = db.Column(db.String)
    LobbyistPrefix = db.Column(db.String)
    LobbyistFirstName = db.Column(db.String)
    LobbyistMiddleInitials = db.Column(db.String)
    LobbyistLastName = db.Column(db.String)
    LobbyistSuffix = db.Column(db.String)
    LobbyistBusiness = db.Column(db.String)
    LobbyistPositionTitle = db.Column(db.String)
    PreviousPublicOfficeHolder = db.Column(db.String)
    PreviousPublicOfficeHoldPosition = db.Column(db.String)
    PreviousPublicOfficePositionProgramName = db.Column(db.String)
    PreviousPublicOfficeHoldLastDate = db.Column(db.String)
    address_id = db.Column(db.Integer, db.ForeignKey("raw_address.id"))
    address = db.relationship("RawAddress", backref="raw_communication")
    report_id = db.Column(db.Integer, db.ForeignKey("raw_lobbying_report.id"))


class RawGrassroot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Community = db.Column(db.String)
    StartDate = db.Column(db.String)
    EndDate = db.Column(db.String)
    Target = db.Column(db.String)
    report_id = db.Column(db.Integer, db.ForeignKey("raw_lobbying_report.id"))


class RawBeneficiary(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String)
    Name = db.Column(db.String)
    TradeName = db.Column(db.String)
    FiscalStart = db.Column(db.String)
    FiscalEnd = db.Column(db.String)
    address_id = db.Column(db.Integer, db.ForeignKey("raw_address.id"))
    address = db.relationship("RawAddress", backref="raw_beneficiary")
    report_id = db.Column(db.Integer, db.ForeignKey("raw_lobbying_report.id"))


class RawFirm(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    Type = db.Column(db.String)
    Name = db.Column(db.String)
    TradeName = db.Column(db.String)
    FiscalStart = db.Column(db.String)
    FiscalEnd = db.Column(db.String)
    Description = db.Column(db.String)
    BusinessType = db.Column(db.String)
    address_id = db.Column(db.Integer, db.ForeignKey("raw_address.id"))
    address = db.relationship("RawAddress", backref="raw_firm")
    report_id = db.Column(db.Integer, db.ForeignKey("raw_lobbying_report.id"))


class RawPrivateFunding(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    Funding = db.Column(db.String)
    Contact = db.Column(db.String)
    Agent = db.Column(db.String)
    AgentContact = db.Column(db.String)
    report_id = db.Column(db.Integer, db.ForeignKey("raw_lobbying_report.id"))


class RawGmtFunding(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    GMTName = db.Column(db.String)
    Program = db.Column(db.String)
    report_id = db.Column(db.Integer, db.ForeignKey("raw_lobbying_report.id"))


class RawMeeting(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    Committee = db.Column(db.String)
    Desc = db.Column(db.String)
    Date = db.Column(db.String)
    report_id = db.Column(
        db.Integer, db.ForeignKey("raw_lobbying_report.id"), nullable=False
    )


class RawPOH(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String)
    Office = db.Column(db.String)
    Title = db.Column(
        db.String,
    )
    Type = db.Column(db.String)
    meeting_id = db.Column(db.Integer, db.ForeignKey("raw_meeting.id"), nullable=False)


class RawLobbyist(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    Number = db.Column(db.Text, nullable=True)
    Prefix = db.Column(db.Text, nullable=True)
    FirstName = db.Column(db.Text, nullable=True)
    MiddleInitials = db.Column(db.Text, nullable=True)
    LastName = db.Column(db.Text, nullable=True)
    Suffix = db.Column(db.Text, nullable=True)
    Business = db.Column(db.Text, nullable=True)
    Type = db.Column(db.Text, nullable=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey("raw_meeting.id"), nullable=False)


class RawAddress(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    address_line_1 = db.Column(db.String)
    address_line_2 = db.Column(db.String)
    city = db.Column(db.String)
    country = db.Column(db.String)
    postal_code = db.Column(db.String)
    province = db.Column(db.String)
    phone = db.Column(db.String)
