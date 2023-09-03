from typing import List
from sqlalchemy.orm import Session
from app.models.models import Lobbyist
from app.models.processor_models import RawLobbyist, RawCommunication
from app.models.enums import LobbyistType
import build.utils as utils

LOBBYIST_KEY = (
    "Number",
    "FirstName",
    "MiddleInitials",
    "LastName",
    "Suffix",
    "Business",
    "Type",
)

COMMUNICATIONS_LOBBYIST_KEY = (
    "LobbyistNumber",
    "LobbyistFirstName",
    "LobbyistMiddleInitials",
    "LobbyistLastName",
    "LobbyistSuffix",
    "LobbyistBusiness",
    "LobbyistType",
)


def get_data_row(raw_lobbyist: RawLobbyist) -> dict:
    return {
        "number": raw_lobbyist.Number,
        "first_name": raw_lobbyist.FirstName,
        "middle_initials": raw_lobbyist.MiddleInitials,
        "last_name": raw_lobbyist.LastName,
        "suffix": raw_lobbyist.Suffix,
        "type": LobbyistType(raw_lobbyist.Type),
    }


def get_data_row_from_communication(raw_communication: RawCommunication) -> dict:
    return {
        "number": raw_communication.LobbyistNumber,
        "first_name": raw_communication.LobbyistFirstName,
        "middle_initials": raw_communication.LobbyistMiddleInitials,
        "last_name": raw_communication.LobbyistLastName,
        "suffix": raw_communication.LobbyistSuffix,
        "type": LobbyistType(raw_communication.LobbyistType),
    }


def create_table(session: Session) -> List[Lobbyist]:
    raw_lobbyists = session.query(RawLobbyist).all()
    raw_communications = session.query(RawCommunication).all()

    grouped_raw_lobbyists = utils.get_grouped_raw_records(raw_lobbyists, LOBBYIST_KEY)
    grouped_raw_communications = utils.get_grouped_raw_records(
        raw_communications, COMMUNICATIONS_LOBBYIST_KEY
    )

    keys = set(grouped_raw_lobbyists.keys()).union(
        set(grouped_raw_communications.keys())
    )
    keys.discard(
        (None, None, None, None, None, None, None)
    )  # Some communications don't have a lobbyist
    keys = list(keys)

    lobbyists = []
    for key in keys:
        raw_lobbyist_list = grouped_raw_lobbyists.get(key, [])
        raw_communication_list = grouped_raw_communications.get(key, [])

        if raw_lobbyist_list:
            raw_lobbyist = raw_lobbyist_list[0]
            lobbyist = Lobbyist(**get_data_row(raw_lobbyist))
        else:
            raw_communication = raw_communication_list[0]
            lobbyist = Lobbyist(**get_data_row_from_communication(raw_communication))

        lobbyist.lobbyist_data_sources = raw_lobbyist_list
        lobbyist.communication_data_sources = raw_communication_list

        lobbyists.append(lobbyist)

    session.add_all(lobbyists)
    session.commit()

    return Lobbyist.query.all()
