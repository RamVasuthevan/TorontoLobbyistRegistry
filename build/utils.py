from typing import List, Tuple, Dict, Union, Callable
from collections import defaultdict
from sqlalchemy import insert
from sqlalchemy.orm import Session
from app.models.processor_models import (
    RawAddress,
    RawLobbyist,
    RawGrassroot,
    RawPrivateFunding,
    RawPOH,
    RawBeneficiary,
    RawFirm,
)
from app.models.models import (
    Address,
    Lobbyist,
    Grassroot,
    PrivateFunding,
    PublicOfficeHolder,
    Beneficiary,
    Firm,
    raw_address_address,
)
from app import db


def get_grouped_raw_records(
    raw_records: Union[List[RawAddress], List[RawLobbyist]], key: Tuple[str, ...]
) -> Dict[Tuple, Union[List[Address], List[Lobbyist]]]:
    """
    Given a list of raw records, groups them by specified attributes.

    Args:
        raw_records: List of raw records, either RawAddress or RawLobbyist objects.
        key: Tuple of strings representing attribute names.

    Returns:
        If raw_records is a list of RawAddress objects, returns a Dict[Tuple, List[Address]].
        If raw_records is a list of RawLobbyist objects, returns a Dict[Tuple, List[Lobbyist]].

    Raises:
        AttributeError: If a record in raw_records doesn't have an attribute specified in key.
    """
    D = defaultdict(list)
    for raw_record in raw_records:
        key_tuple = ()
        for attr in key:
            try:
                key_tuple += (getattr(raw_record, attr),)
            except AttributeError as e:
                raise AttributeError(
                    f"Record {raw_record} does not have attribute {attr}"
                ) from e
        D[key_tuple].append(raw_record)
    return D


def create_table(
    session: Session,
    raw_model: Union[RawGrassroot, RawPrivateFunding, RawPOH, RawBeneficiary, RawFirm],
    model: Union[Grassroot, PrivateFunding, PublicOfficeHolder, Beneficiary, Firm],
    data_row_func: Callable,
    lookup_address: bool = False,
) -> Union[
    List[RawGrassroot],
    List[PrivateFunding],
    List[PublicOfficeHolder],
    List[Beneficiary],
    List[Firm],
]:
    """
    Creates a table in the database from a given SQLAlchemy model.

    The function fetches all raw records from the raw model, transforms them into the desired model
    structure using the data_row_func, and then inserts them into the database.

    Args:
        session: SQLAlchemy Session object for database interaction.
        raw_model: SQLAlchemy Model representing the raw data to be transformed.
        model: SQLAlchemy Model representing the desired final data structure.
        data_row_func: Function to transform raw data rows into the structure of the final model.
        lookup_address: Bool indicating whether to use a lookup dictionary for address. Default is False.

    Returns:
        List of all records in the newly created table.

    Raises:
        sqlalchemy.exc.SQLAlchemyError: If there is an issue with the database interaction.
    """
    raw_records = raw_model.query.all()
    if lookup_address:
        address_lookup_dict = {
            mapping.raw_address_id: mapping.address_id
            for mapping in session.query(raw_address_address).all()
        }
        data = [
            data_row_func(raw_record, address_lookup_dict) for raw_record in raw_records
        ]
    else:
        data = [data_row_func(raw_record) for raw_record in raw_records]

    session.execute(insert(model), data)
    session.commit()
    return session.query(model).all()
