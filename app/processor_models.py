from datetime import date
from app import db
from sqlalchemy.orm import validates
from enum import Enum
from app.models import DataSource

class RawRegistrant(db.Model):
    DataSource = db.Column(db.Enum(DataSource))
    id = db.Column(db.Integer, primary_key=True)
    RegistrationNUmber = db.Column(db.String)
    RegistrationNUmberWithSoNum = db.Column(db.String)
    Status = db.Column(db.String)
    EffectiveDate= db.Column(db.String)
    Type= db.Column(db.String)
    Prefix= db.Column(db.String)
    FirstName= db.Column(db.String)
    MiddleInitials= db.Column(db.String)
    LastName= db.Column(db.String)
    Suffix= db.Column(db.String)
    PositionTitle= db.Column(db.String)
    PreviousPublicOfficeHolder= db.Column(db.String)
    PreviousPublicOfficeHoldPosition= db.Column(db.String)
    PreviousPublicOfficePositionProgramName= db.Column(db.String)
    PreviousPublicOfficeHoldLastDate = db.Column(db.String)