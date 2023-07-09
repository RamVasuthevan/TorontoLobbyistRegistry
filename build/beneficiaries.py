from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Beneficiary, raw_address_address
from app.models.processor_models import RawBeneficiary
from app.models.enums import BeneficiaryType
from sqlalchemy import insert
import build.utils as utils


def get_data_row(
    raw_beneficiary: RawBeneficiary, address_lookup: dict[int, int]
) -> dict:
    return {
        "type": BeneficiaryType(raw_beneficiary.Type),
        "name": raw_beneficiary.Name,
        "trade_name": raw_beneficiary.TradeName,
        "address_id": address_lookup.get(raw_beneficiary.address_id),
        "report_id": raw_beneficiary.report_id,
    }


def create_table(session: Session) -> List[Beneficiary]:
    return utils.create_table(
        session, RawBeneficiary, Beneficiary, get_data_row, lookup_address=True
    )
