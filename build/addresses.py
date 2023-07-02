from typing import List
from sqlalchemy.orm import Session
from app.models.models import Address, CanadianAddress, AmericanAddress, OtherAddress
from app.models.processor_models import RawAddress
from app.models.enums import AddressType
from collections import defaultdict


def get_address_type(raw_address: dict) -> AddressType:
    if raw_address["Country"] == "Canada":
        return AddressType.CANADIAN
    elif raw_address["Country"] == "United States":
        return AddressType.AMERICAN
    else:
        return AddressType.OTHER

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

def create_addresses_table(session: Session, raw_addresses: List[RawAddress]) -> List[Address]:
    data = get_grouped_raw_addresses(raw_addresses)

    addresses = []
    for address_data in data:
        address_type = get_address_type(address_data)

        if address_type == AddressType.CANADIAN:
            new_address = CanadianAddress(
                address_line1=address_data['AddressLine1'],
                address_line2=address_data['AddressLine2'],
                city=address_data['City'],
                province=address_data['Province'],
                postal_code=address_data['PostalCode'],
                phone=address_data['Phone']
            )
        elif address_type == AddressType.AMERICAN:
            new_address = AmericanAddress(
                address_line1=address_data['AddressLine1'],
                address_line2=address_data['AddressLine2'],
                city=address_data['City'],
                state=address_data['Province'],
                zipcode=address_data['PostalCode'],
                phone=address_data['Phone']
            )
        else:
            new_address = OtherAddress(
                raw_address_line1=address_data['AddressLine1'],
                raw_address_line2=address_data['AddressLine2'],
                raw_city=address_data['City'],
                raw_province=address_data['Province'],
                raw_postal_code=address_data['PostalCode'],
                raw_phone=address_data['Phone']
            )

        new_address.data_sources = address_data['data_sources']
        addresses.append(new_address)

    session.add_all(addresses)
    session.commit()
    return addresses
