from typing import List, Tuple, Dict, Union
from collections import defaultdict
from app.models.processor_models import RawAddress, RawLobbyist
from app.models.models import Address, Lobbyist

def get_grouped_raw_records(raw_records: Union[List[RawAddress], List[RawLobbyist]], key: Tuple[str, ...]) -> Dict[Tuple, Union[List[Address], List[Lobbyist]]]:
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
                raise AttributeError(f"Record {raw_record} does not have attribute {attr}") from e
        D[key_tuple].append(raw_record)
    return D
