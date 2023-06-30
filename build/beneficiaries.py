from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Beneficiary, raw_address_address
from app.models.processor_models import RawBeneficiary
from app.models.enums import BeneficiaryType
from sqlalchemy import insert

def get_beneficiary_data_row(raw_beneficiary: RawBeneficiary, address_lookup: dict[int,int]) -> dict:
    return {
        "type": BeneficiaryType(raw_beneficiary.Type),
        "name": raw_beneficiary.Name,
        "trade_name": raw_beneficiary.TradeName,
        "address_id": address_lookup.get(raw_beneficiary.address_id), 
        "report_id": raw_beneficiary.report_id
    }

def create_beneficiaries_table(session: Session, raw_beneficiaries: List[RawBeneficiary]) -> List[Beneficiary]:
    address_lookup = {mapping.raw_address_id: mapping.address_id for mapping in session.query(raw_address_address).all()}

    data = [get_beneficiary_data_row(raw_beneficiary, address_lookup) for raw_beneficiary in raw_beneficiaries]

    session.execute(insert(Beneficiary).values(data))
    session.commit()
    return session.query(Beneficiary).all()
