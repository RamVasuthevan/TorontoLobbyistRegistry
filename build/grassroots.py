from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Grassroot
from app.models.processor_models import RawGrassroot
from sqlalchemy import insert

def get_grassroots_data_row(raw_funding: RawGrassroot) -> dict:
    return {
        "community": raw_funding.Community,
        "start_date": datetime.strptime(raw_funding.StartDate, "%Y-%m-%d").date(),
        "end_date": datetime.strptime(raw_funding.EndDate, "%Y-%m-%d").date(),
        "target": raw_funding.Target,
        "report_id": raw_funding.report_id,
    }

def create_grassroots_table(session: Session, raw_fundings: List[RawGrassroot]) -> List[Grassroot]:
    data = [get_grassroots_data_row(raw_funding) for raw_funding in raw_fundings]

    session.execute(insert(Grassroot), data)
    session.commit()
    return session.query(Grassroot).all()
