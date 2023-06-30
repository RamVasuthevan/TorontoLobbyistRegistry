from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Address
from app.models.processor_models import RawAddress
from sqlalchemy import insert

def get_address_data_row(raw_address: RawAddress) -> dict:
    return {
        "data_source_id": raw_address.id,
    }


def create_addresses_table(session: Session, raw_addresses: List[RawAddress]) -> List[Address]:
    data = [get_address_data_row(raw_address) for raw_address in raw_addresses]

    session.execute(insert(Address), data)
    session.commit()
    return session.query(Address).all()