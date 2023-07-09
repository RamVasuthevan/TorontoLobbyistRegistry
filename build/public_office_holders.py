from typing import List
from sqlalchemy.orm import Session
from app.models.models import PublicOfficeHolder
from app.models.processor_models import RawPOH
from app.models.enums import PublicOfficeHolderType
import build.utils as utils


def get_data_row(raw_poh: RawPOH) -> dict:
    return {
        "id": raw_poh.id,
        "name": raw_poh.Name,
        "office": raw_poh.Office,
        "title": raw_poh.Title,
        "type": PublicOfficeHolderType(raw_poh.Type),
        "meeting_id": raw_poh.meeting_id,
    }


def create_table(session: Session):
    return utils.create_table(session, RawPOH, PublicOfficeHolder, get_data_row)
