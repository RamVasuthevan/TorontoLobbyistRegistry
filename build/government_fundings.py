from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import GovernmentFunding
from app.models.processor_models import RawGmtFunding
from sqlalchemy import insert
import build.utils as utils


def get_data_row(raw_funding: RawGmtFunding) -> dict:
    return {
        "government_name": raw_funding.GMTName,
        "program": raw_funding.Program,
        "report_id": raw_funding.report_id,
    }


def create_table(session: Session) -> List[GovernmentFunding]:
    return utils.create_table(session, RawGmtFunding, GovernmentFunding, get_data_row)
