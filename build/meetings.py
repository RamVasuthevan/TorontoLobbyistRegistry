from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Meeting
from app.models.processor_models import RawMeeting
from app.models.enums import MeetingCommittee
from sqlalchemy import insert
from app.models.errors import get_enum_error_message

def get_meeting_committee(raw_meeting: RawMeeting) -> MeetingCommittee:
    committee = raw_meeting.Committee

    if "Government Relations Committee" in committee:
        return MeetingCommittee.GOVERNMENT_RELATIONS
    elif "Smart Cities" == committee:
        return MeetingCommittee.SMART_CITIES
    elif "Board of Directors" in committee:
        return MeetingCommittee.BOARD_OF_DIRECTORS
    elif "Scarborough Community Multicultural Festival" == committee:
        return MeetingCommittee.SCARBOROUGH_MULTICULTURAL_FESTIVAL
    elif "Executive Committee" == committee:
        return MeetingCommittee.EXECUTIVE
    raise ValueError(get_enum_error_message("committee", MeetingCommittee, committee))


def get_meeting_data_row(raw_meeting: RawMeeting) -> dict:
    return {
        "data_source": raw_meeting.DataSource,
        "id": raw_meeting.id,
        "committee": get_meeting_committee(raw_meeting),
        "description": raw_meeting.Desc,
        "date": datetime.strptime(raw_meeting.Date, "%Y-%m-%d").date(),
        "report_id": raw_meeting.report_id,
    }


def create_meeting_table(session: Session, raw_meetings: List[RawMeeting]) -> List[Meeting]:
    data = [get_meeting_data_row(raw_meeting) for raw_meeting in raw_meetings]

    session.execute(insert(Meeting), data)
    session.commit()
    return session.query(Meeting).all()
