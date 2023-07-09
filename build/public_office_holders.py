from typing import List
from sqlalchemy.orm import Session
from app.models.models import PublicOfficeHolder
from app.models.processor_models import RawPOH
from app.models.enums import PublicOfficeHolderType
from sqlalchemy import insert

def get_data_row(raw_poh: RawPOH) -> dict:
    return {
        "id": raw_poh.id,
        "name": raw_poh.Name,
        "office": raw_poh.Office,
        "title": raw_poh.Title,
        "type": PublicOfficeHolderType(raw_poh.Type),
        "meeting_id": raw_poh.meeting_id,
    }


def create_public_office_holder_table(session: Session, raw_pohs: List[RawPOH]) -> List[PublicOfficeHolder]:
    data = [get_data_row(raw_poh) for raw_poh in raw_pohs]

    session.execute(insert(PublicOfficeHolder), data)
    session.commit()
    return session.query(PublicOfficeHolder).all()

