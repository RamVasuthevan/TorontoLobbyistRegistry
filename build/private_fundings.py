from typing import List
from sqlalchemy.orm import Session
from app.models.models import PrivateFunding
from app.models.processor_models import RawPrivateFunding
from sqlalchemy import insert

def get_data_row(raw_funding: RawPrivateFunding) -> dict:
    return {
        "funding": raw_funding.Funding,
        "contact": raw_funding.Contact,
        "agent": raw_funding.Agent,
        "agent_contact": raw_funding.AgentContact,
        "report_id": raw_funding.report_id,
    }


def create_private_funding_table(session: Session, raw_fundings: List[RawPrivateFunding]) -> List[PrivateFunding]:
    data = [get_data_row(raw_funding) for raw_funding in raw_fundings]

    session.execute(insert(PrivateFunding), data)
    session.commit()
    return session.query(PrivateFunding).all()

