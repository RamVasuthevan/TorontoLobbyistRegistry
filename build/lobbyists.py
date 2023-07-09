from typing import List,Dict
from sqlalchemy.orm import Session
from app.models.models import Lobbyist
from app.models.processor_models import RawLobbyist
from app.models.enums import LobbyistType
from sqlalchemy import insert
from collections import defaultdict

def get_grouped_raw_lobbyists(raw_lobbyists: List[RawLobbyist]) -> Dict[tuple, List[RawLobbyist]]:
    D = defaultdict(list)
    for raw_lobbyist in raw_lobbyists:
        key = (
            raw_lobbyist.Number,
            raw_lobbyist.FirstName,
            raw_lobbyist.MiddleInitials,
            raw_lobbyist.LastName,
            raw_lobbyist.Suffix,
            raw_lobbyist.Business,
            raw_lobbyist.Type,
        )
        D[key].append(raw_lobbyist)
    return D

def get_data_row(raw_lobbyist: RawLobbyist) -> dict:
    return {
        "number": raw_lobbyist.Number,
        "first_name": raw_lobbyist.FirstName,
        "middle_initials": raw_lobbyist.MiddleInitials,
        "last_name": raw_lobbyist.LastName,
        "suffix": raw_lobbyist.Suffix,
        "type": LobbyistType(raw_lobbyist.Type),
    }


def create_lobbyist_table(session: Session, raw_lobbyists: List[RawLobbyist]) -> List[Lobbyist]:
    grouped_raw_lobbyists = get_grouped_raw_lobbyists(raw_lobbyists)

    lobbyists = []
    for raw_lobbyist_list in grouped_raw_lobbyists.values():
        raw_lobbyist = raw_lobbyist_list[0]  # Just need to use one of the RawLobbyist objects to get the details
        
        lobbyist = Lobbyist(**get_data_row(raw_lobbyist))
        lobbyist.data_sources = raw_lobbyist_list  # Assign the list of RawLobbyist objects

        lobbyists.append(lobbyist)

    session.add_all(lobbyists)
    session.commit()

    return Lobbyist.query.all()
