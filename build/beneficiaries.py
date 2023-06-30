from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Beneficiary, LobbyingReport
from app.models.processor_models import RawBeneficiary
from app.models.enums import BeneficiaryType
from sqlalchemy import insert

def get_beneficiary_data_row(raw_beneficiary: RawBeneficiary) -> dict:
    return {
        "type": BeneficiaryType(raw_beneficiary.Type),
        "name": raw_beneficiary.Name,
        "trade_name": raw_beneficiary.TradeName,
        "report_id":raw_beneficiary.report_id
    }


def create_beneficiaries_table(session: Session, raw_beneficiaries: List[RawBeneficiary]) -> List[Beneficiary]:
    data = [get_beneficiary_data_row(raw_beneficiary) for raw_beneficiary in raw_beneficiaries]

    session.execute(insert(Beneficiary), data)
    session.commit()
    return session.query(Beneficiary).all()