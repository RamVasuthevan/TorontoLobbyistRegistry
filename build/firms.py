from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Firm, raw_address_address
from app.models.processor_models import RawFirm
from app.models.enums import FirmType,FirmBusinessType
from sqlalchemy import insert

def get_data_row(raw_firm: RawFirm, address_lookup: dict[int,int]) -> dict:
    return {
        "type": FirmType(raw_firm.Type),
        "name": raw_firm.Name,
        "trade_name": raw_firm.TradeName,
        "description": raw_firm.Description,
        "business_type": None if raw_firm.BusinessType is None else FirmBusinessType(raw_firm.BusinessType),
        "address_id": address_lookup[raw_firm.address_id],
        "report_id": raw_firm.report_id,
        
    }

def create_firms_table(session: Session, raw_firms: List[RawFirm]) -> List[Firm]:
    address_lookup = {mapping.raw_address_id: mapping.address_id for mapping in session.query(raw_address_address).all()}

    data = [get_data_row(raw_firm, address_lookup) for raw_firm in raw_firms]

    session.execute(insert(Firm).values(data))
    session.commit()
    return session.query(Firm).all()
