from typing import List, Dict
from sqlalchemy.orm import Session
from app.models.models import Address, CanadianAddress, AmericanAddress, OtherAddress
from app.models.processor_models import RawAddress
from app.models.enums import AddressType
from build.utils import get_grouped_raw_records
from collections import defaultdict


ADDRESS_KEY = (
    "AddressLine1",
    "AddressLine2",
    "City",
    "Country",
    "PostalCode",
    "Province",
    "Phone",
)

# Hardcoded dictionary for the different address types and their classes
ADDRESS_TYPE_TO_CLASS = {
    AddressType.CANADIAN: CanadianAddress,
    AddressType.AMERICAN: AmericanAddress,
    AddressType.OTHER: OtherAddress,
}


def get_address_type(raw_address: RawAddress) -> AddressType:
    country = raw_address.Country
    if country == "Canada":
        return AddressType.CANADIAN
    elif country == "United States":
        return AddressType.AMERICAN
    else:
        return AddressType.OTHER


def get_grouped_raw_addresses(
    raw_addresses: List[RawAddress],
) -> Dict[tuple, List[RawAddress]]:
    D = defaultdict(list)
    for raw_address in raw_addresses:
        key = (
            raw_address.AddressLine1,
            raw_address.AddressLine2,
            raw_address.City,
            raw_address.Country,
            raw_address.PostalCode,
            raw_address.Province,
            raw_address.Phone,
        )
        D[key].append(raw_address)
    return D


def get_canadian_address_data_row(raw_address: RawAddress) -> dict:
    return {
        "address_line1": raw_address.AddressLine1,
        "address_line2": raw_address.AddressLine2,
        "city": raw_address.City,
        "province": raw_address.Province,
        "postal_code": raw_address.PostalCode,
        "phone": raw_address.Phone,
    }


def get_american_address_data_row(raw_address: RawAddress) -> dict:
    return {
        "address_line1": raw_address.AddressLine1,
        "address_line2": raw_address.AddressLine2,
        "city": raw_address.City,
        "state": raw_address.Province,
        "zipcode": raw_address.PostalCode,
        "phone": raw_address.Phone,
    }


def get_other_address_data_row(raw_address: RawAddress) -> dict:
    return {
        "raw_address_line1": raw_address.AddressLine1,
        "raw_address_line2": raw_address.AddressLine2,
        "raw_city": raw_address.City,
        "raw_province": raw_address.Province,
        "raw_postal_code": raw_address.PostalCode,
        "raw_phone": raw_address.Phone,
    }


# Hardcoded dictionary for the different address types and their data extraction functions
ADDRESS_TYPE_TO_DATA_ROW_FUNCTION = {
    AddressType.CANADIAN: get_canadian_address_data_row,
    AddressType.AMERICAN: get_american_address_data_row,
    AddressType.OTHER: get_other_address_data_row,
}


def create_addresses_table(
    session: Session, raw_addresses: List[RawAddress]
) -> List[Address]:
    grouped_raw_addresses = get_grouped_raw_records(raw_addresses, ADDRESS_KEY)

    addresses = []
    for raw_address_list in grouped_raw_addresses.values():
        raw_address = raw_address_list[
            0
        ]  # Just need to use one of the RawAddress objects to get the details
        address_type = get_address_type(raw_address)

        AddressClass = ADDRESS_TYPE_TO_CLASS[address_type]
        data_function = ADDRESS_TYPE_TO_DATA_ROW_FUNCTION[address_type]

        new_address = AddressClass(**data_function(raw_address))
        new_address.data_sources = (
            raw_address_list  # Assign the list of RawAddress objects
        )

        addresses.append(new_address)

    session.add_all(addresses)
    session.commit()

    return Address.query.all()
