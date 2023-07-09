from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import insert
from app.models.models import Meeting, Lobbyist, raw_lobbyist_lobbyist
from app.models.processor_models import RawMeeting, RawLobbyist
from app.models.enums import MeetingCommittee
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


def get_data_row(raw_meeting: RawMeeting, lobbyists: List[Lobbyist]) -> dict:
    return {
        "committee": get_meeting_committee(raw_meeting),
        "date": datetime.strptime(raw_meeting.Date, "%Y-%m-%d").date(),
        "lobbyists": lobbyists,
        "report_id": raw_meeting.report_id,
    }


def create_meeting_table(
    session: Session, raw_meetings: List[RawMeeting]
) -> List[Meeting]:
    meetings = []

    for raw_meeting in raw_meetings:
        # Query for Lobbyists who attended the meeting
        lobbyists = [
            session.query(Lobbyist)
            .join(
                raw_lobbyist_lobbyist,
                (raw_lobbyist_lobbyist.c.lobbyist_id == Lobbyist.id),
            )
            .filter(raw_lobbyist_lobbyist.c.raw_lobbyist_id == raw_lobbyist.id)
            .one()
            for raw_lobbyist in session.query(RawLobbyist)
            .filter_by(meeting_id=raw_meeting.id)
            .all()
        ]

        session.query(RawLobbyist).filter_by(meeting_id=raw_meeting.id).all()
        # print(f"Meeting {raw_meeting.id} {raw_meeting.report_id} {raw_meeting.Committee} {raw_meeting.Date} has lobbyists: {lobbyists}")
        meetings.append(Meeting(**get_data_row(raw_meeting, lobbyists)))

    session.add_all(meetings)
    session.commit()

    return session.query(Meeting).all()
