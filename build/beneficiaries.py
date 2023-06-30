from typing import List, Dict
import time


from app import db as app_db
from app.models.models import (
    LobbyingReport,
    Beneficiary,
    BeneficiaryType,
)
from app.models.processor_models import (
    RawBeneficiary,
)
from util.sqlalchemy_helpers import  get_one_or_create_all
from build.addresses import create_addresses

def create_beneficiaries(db, raw_beneficiaries: List[RawBeneficiary]) -> List[Beneficiary]:
    start_time = time.time()
    address_dict = {
        raw_beneficiary.address: address
        for raw_beneficiary, address in zip(
            raw_beneficiaries,
            create_addresses(db,
                (raw_beneficiary.address for raw_beneficiary in raw_beneficiaries)
            ),
        )
    }
    end_time = time.time()
    
    print(
        f"Create addresses for create_beneficiaries took {end_time - start_time} seconds"
    )

    beneficiaries_data = [
        {
            "type": BeneficiaryType(raw_beneficiary.Type),
            "name": raw_beneficiary.Name,
            "trade_name": raw_beneficiary.TradeName,
            "address_id": address_dict[raw_beneficiary.address].id,
            "address": address_dict[raw_beneficiary.address],
        }
        for raw_beneficiary in raw_beneficiaries
    ]

    start_time
    beneficiaries = [
        beneficiary_result[0]
        for beneficiary_result in get_one_or_create_all(
            db.session, Beneficiary, beneficiaries_data
        )
    ]
    end_time = time.time()
    print(f"get_one_or_create_all took {end_time - start_time} seconds")

    for beneficiary, raw_beneficiary in zip(beneficiaries, raw_beneficiaries):
        beneficiary.reports.append(
            db.session.get(LobbyingReport, raw_beneficiary.report_id)
        )

    db.session.bulk_save_objects(beneficiaries)
    db.session.flush()

    return beneficiaries

