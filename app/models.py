from datetime import datetime
from app import db
from sqlalchemy.orm import validates
from enum import Enum

class LobbyingReportStatus(Enum):
    ACTIVE = 'Active'
    CLOSED = 'Closed'
    CLOSED_BY_LRO = 'Closed by LRO'

class LobbyingReportType(Enum):
    IN_HOUSE = 'In-house'
    CONSULTANT = 'Consultant'
    VOLUNTARY = 'Voluntary'

class LobbyingReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smnumber = db.Column(db.String)
    status = db.Column(db.Enum(LobbyingReportStatus))
    type = db.Column(db.Enum(LobbyingReportType))
    subject_matter = db.Column(db.String)

    @validates('smnumber')
    def validate_smnumber(self, key, smnumber):
        if not isinstance(smnumber, str):
            raise ValueError("smnumber must be a string")

        if len(smnumber) != 7 or not smnumber.startswith('SM') or not smnumber[2:].isdigit():
            raise ValueError("smnumber must start with 'SM' and followed by 5 digits")
        
        return smnumber

    @validates('status')
    def validate_status(self, key, status):
        if not isinstance(status, LobbyingReportStatus):
            raise ValueError("status must be a LobbyingReportStatus enum value")
        
        return status

    @validates('type')
    def validate_type(self, key, type):
        if not isinstance(type, LobbyingReportType):
            print(f"Invalid type '{type}', should be one of {[t.value for t in LobbyingReportType]}")
            raise ValueError("type must be a LobbyingReportType enum value")
        
        return type
