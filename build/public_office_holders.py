from typing import List
from sqlalchemy.orm import Session
from app.models.models import PublicOfficeHolder
from app.models.processor_models import RawPOH
from app.models.enums import PublicOfficeHolderType


def get_data_row(raw_poh: RawPOH) -> dict:
    return {
        "id": raw_poh.id,
        "name": raw_poh.Name,
        "office": raw_poh.Office,
        "title": raw_poh.Title,
        "type": PublicOfficeHolderType(raw_poh.Type),
        "data_sources": [raw_poh],
    }


def create_table(session: Session) -> List[PublicOfficeHolder]:
    for raw_poh in RawPOH.query.all():
        data_row = get_data_row(raw_poh)
        session.add(PublicOfficeHolder(**data_row))
    session.commit()
    return PublicOfficeHolder.query.all()
