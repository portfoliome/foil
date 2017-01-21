from typing import Mapping


def rename_keys(record: Mapping, key_map: Mapping) -> dict:
    """New record with same keys or renamed keys if key found in key_map."""

    new_record = dict()

    for k, v in record.items():
        key = key_map[k] if k in key_map else k
        new_record[key] = v

    return new_record


def replace_keys(record: Mapping, key_map: Mapping) -> dict:
    """New record with renamed keys including keys only found in key_map."""

    return {key_map[k]: v for k, v in record.items() if k in key_map}
