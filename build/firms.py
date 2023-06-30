from typing import List, Dict


from app import db as app_db
from app.models.models import (
    Firm,
    FirmType,
    FirmBusinessType,
)
from app.models.processor_models import RawFirm
from build.addresses import create_addresses


def create_firms(raw_firms: List[RawFirm]) -> List[Firm]:
    firms = []
    address_dict = {
        raw_firm.address: address
        for raw_firm, address in zip(
            raw_firms, create_addresses(raw_firm.address for raw_firm in raw_firms)
        )
    }

    for raw_firm in raw_firms:
        firm_type = FirmType(raw_firm.Type)
        fiscal_start = (
            None
            if raw_firm.FiscalStart is None
            else datetime.strptime(raw_firm.FiscalStart, "%Y-%m-%d").date()
        )
        fiscal_end = (
            None
            if raw_firm.FiscalEnd is None
            else datetime.strptime(raw_firm.FiscalEnd, "%Y-%m-%d").date()
        )
        business_type = (
            None
            if raw_firm.BusinessType is None
            else FirmBusinessType(raw_firm.BusinessType)
        )
        address = address_dict[raw_firm.address]
        firm = Firm(
            type=firm_type,
            name=raw_firm.Name,
            trade_name=raw_firm.TradeName,
            fiscal_start=fiscal_start,
            fiscal_end=fiscal_end,
            description=raw_firm.Description,
            business_type=business_type,
            address_id=address.id,
            address=address,
            report_id=raw_firm.report_id,
        )
        firms.append(firm)

    db.session.bulk_save_objects(firms)
    db.session.flush()

    return firms
