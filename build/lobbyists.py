from typing import List
from sqlalchemy.orm import Session
from app.models.models import Lobbyist
from app.models.processor_models import RawLobbyist
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

def get_data_row(raw_lobbyist: RawLobbyist) -> dict:
    return {
        "number": raw_lobbyist.Number,
        "first_name": raw_lobbyist.FirstName,
        "middle_initials": raw_lobbyist.MiddleInitials,
        "last_name": raw_lobbyist.LastName,
        "suffix": raw_lobbyist.Suffix,
        "type": LobbyistType(raw_lobbyist.Type),
    }

def create_table(session: Session) -> List[Lobbyist]:
    raw_lobbyists = session.query(RawLobbyist).all()
    grouped_raw_lobbyists = utils.get_grouped_raw_records(raw_lobbyists, LOBBYIST_KEY)

    lobbyists = []
    for raw_lobbyist_list in grouped_raw_lobbyists.values():
        raw_lobbyist = raw_lobbyist_list[
            0
        ]  # Just need to use one of the RawLobbyist objects to get the details

        lobbyist = Lobbyist(**get_data_row(raw_lobbyist))
        lobbyist.data_sources = (
            raw_lobbyist_list  # Assign the list of RawLobbyist objects
        )

        lobbyists.append(lobbyist)

    session.add_all(lobbyists)
    session.commit()

    return Lobbyist.query.all()
