from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from app.models.models import Address
from app.models.processor_models import RawAddress
from sqlalchemy import insert
from collections import defaultdict

def get_grouped_raw_addresses(raw_addresses: List[RawAddress]) -> List[dict]:
    D = defaultdict(list)

    for raw_address in raw_addresses:
        key = (
            raw_address.AddressLine1, 
            raw_address.AddressLine2, 
            raw_address.City,
            raw_address.Country, 
            raw_address.PostalCode, 
            raw_address.Province,
            raw_address.Phone
        )
        D[key].append(raw_address.id)

    raw_address_grouped = [
        {
            'AddressLine1': key[0], 
            'AddressLine2': key[1], 
            'City': key[2],
            'Country': key[3], 
            'PostalCode': key[4], 
            'Province': key[5],
            'Phone': key[6],
            'data_sources': [RawAddress.query.get(id) for id in ids]
        } 
        for key, ids in D.items()
    ]
    
    return raw_address_grouped

def create_addresses_table2(session: Session, raw_addresses: List[RawAddress]) -> List[Address]:
    data = get_grouped_raw_addresses(raw_addresses)

    session.execute(insert(Address), data)
    session.commit()
    return session.query(Address).all()

def create_addresses_table(session: Session, raw_addresses: List[RawAddress]) -> List[Address]:
    data = get_grouped_raw_addresses(raw_addresses)

    addresses = []
    for address_data in data:
        new_address = Address()
        new_address.data_sources = address_data['data_sources']
        addresses.append(new_address)

    session.add_all(addresses)
    session.commit()
    return addresses
