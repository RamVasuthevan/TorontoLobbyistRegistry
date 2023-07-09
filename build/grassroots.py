from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Grassroot
from app.models.processor_models import RawGrassroot
from sqlalchemy import insert
import build.utils as utils


def get_data_row(raw_funding: RawGrassroot) -> dict:
    return {
        "community": raw_funding.Community,
        "start_date": datetime.strptime(raw_funding.StartDate, "%Y-%m-%d").date(),
        "end_date": datetime.strptime(raw_funding.EndDate, "%Y-%m-%d").date(),
        "target": raw_funding.Target,
        "report_id": raw_funding.report_id,
    }


def create_table(session: Session) -> List[Grassroot]:
    return utils.create_table(session, RawGrassroot, Grassroot, get_data_row)
