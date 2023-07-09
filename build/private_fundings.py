from typing import List
from sqlalchemy.orm import Session
from app.models.models import PrivateFunding
from app.models.processor_models import RawPrivateFunding
import build.utils as utils


def get_data_row(raw_funding: RawPrivateFunding) -> dict:
    return {
        "funding": raw_funding.Funding,
        "contact": raw_funding.Contact,
        "agent": raw_funding.Agent,
        "agent_contact": raw_funding.AgentContact,
        "report_id": raw_funding.report_id,
    }


def create_table(session: Session) -> List[PrivateFunding]:
    return utils.create_table(session, RawPrivateFunding, PrivateFunding, get_data_row)
