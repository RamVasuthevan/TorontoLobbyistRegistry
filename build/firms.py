from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Firm, raw_address_address
from app.models.processor_models import RawFirm
from app.models.enums import FirmType, FirmBusinessType
from sqlalchemy import insert
from build import utils as utils


def get_data_row(raw_firm: RawFirm, address_lookup: dict[int, int]) -> dict:
    return {
        "type": FirmType(raw_firm.Type),
        "name": raw_firm.Name,
        "trade_name": raw_firm.TradeName,
        "description": raw_firm.Description,
        "business_type": None
        if raw_firm.BusinessType is None
        else FirmBusinessType(raw_firm.BusinessType),
        "address_id": address_lookup[raw_firm.address_id],
        "report_id": raw_firm.report_id,
    }


def create_table(session: Session) -> List[Firm]:
    return utils.create_table(
        session, RawFirm, Firm, get_data_row, lookup_address=True
    )
