from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import GovernmentFunding
from app.models.processor_models import RawGmtFunding
from sqlalchemy import insert

def get_government_funding_data_row(raw_funding: RawGmtFunding) -> dict:
    return {
        "government_name": raw_funding.GMTName,
        "program": raw_funding.Program,
        "report_id": raw_funding.report_id,
    }

def create_government_funding_table(session: Session, raw_fundings: List[RawGmtFunding]) -> List[GovernmentFunding]:
    data = [get_government_funding_data_row(raw_funding) for raw_funding in raw_fundings]

    session.execute(insert(GovernmentFunding), data)
    session.commit()
    return session.query(GovernmentFunding).all()

