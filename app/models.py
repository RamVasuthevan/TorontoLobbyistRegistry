from datetime import datetime
from app import db
from sqlalchemy.orm import validates

class LobbyingReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    smnumber = db.Column(db.String)
    status = db.Column(db.String)
    type = db.Column(db.String)

    @validates('smnumber')
    def validate_smnumber(self, key, smnumber):
        if not isinstance(smnumber, str):
            raise ValueError("smnumber must be a string")

        if len(smnumber) != 7 or not smnumber.startswith('SM') or not smnumber[2:].isdigit():
            raise ValueError("smnumber must start with 'SM' and followed by 5 digits")
        
        return smnumber

    @validates('status')
    def validate_status(self, key, status):
        valid_statuses = ['Active', 'Closed', 'Closed by LRO']
        if not isinstance(status, str):
            raise ValueError("status must be a string")
        
        if status not in valid_statuses:
            raise ValueError(f"Invalid status '{status}', should be one of {valid_statuses}")
        return status
