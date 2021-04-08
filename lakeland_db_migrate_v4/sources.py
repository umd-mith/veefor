"""Handle input data coming from Airtable."""
import json
import pathlib
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Final, Union, TypeVar, Tuple, DefaultDict, Text
import source_mappings as sm


# TODO: Figure out how to move these dataclass declarations to a separate file without mypy losing track of them
@dataclass(frozen=True)
class AirtableSourceRecord:
    """Base classs for Airtable records"""

    airtable_created_time: str
    airtable_idno: str


@dataclass(frozen=True)
class AccessionSourceRecord(AirtableSourceRecord):
    """An record from the Accessions table in the *source* base."""

    file_count: int
    donation_date: str
    donor_name: str
    file_array: list[str]
    idno: str
    linked_entity_array: list[str] = field(default_factory=list)
    title: str = ""
    description: Text = ""
    legacy_idno_umd: str = ""
    _ldt_check: str = ""


@dataclass(frozen=True)
class ItemSourceRecord(AirtableSourceRecord):
    """A record from the Items table in the *source* base."""

    idno: str


@dataclass(frozen=True)
class EntitySourceRecord(AirtableSourceRecord):
    """A record from the Entities table in the *source* base."""

    name: str
    linked_items_array: list[str] = field(default_factory=list)
    address: str = ""
    alt_name: str = ""
    bio_hist: str = ""
    category: str = ""


# TYPE HINTING STUFF
# A pretty loose type hint for json that comes back from Airtable
AIRTABLE_JSON = dict[str, Union[str, int, list[str]]]

AnyRecord = TypeVar("AnyRecord", AccessionSourceRecord, EntitySourceRecord)


def load_from_file(fname: str) -> Tuple[list[AIRTABLE_JSON], Tuple[str, ...]]:
    """
    Load data from a json file representing the contents of a table from an Airtable base to be migrated.

    :param fname: A string representing the name of the file to load
    :return: A list of dictionaries representing the json data
    """
    V4_SOURCE_DATA_DIR: Final = pathlib.Path().cwd() / "source_data"

    target_file: pathlib.Path = pathlib.Path.joinpath(V4_SOURCE_DATA_DIR, fname)
    target_data: list[AIRTABLE_JSON] = []

    try:
        with pathlib.Path.open(target_file, "r") as fobject:
            target_data = json.loads(fobject.read())
    except FileNotFoundError as err:
        print(err)

    # Grab all the keys actually used in records to check our mappings later
    key_collector: DefaultDict[str, str] = defaultdict()
    for jsonObj in target_data:
        for k in jsonObj.keys():
            key_collector[k] = ""

    uniq_keys: Tuple[str, ...] = tuple(key_collector.keys())

    return (target_data, uniq_keys)


def check_key_mappings(probe: Tuple[str, ...], mapping: dict[str, str]) -> None:
    """
    Check that there aren't keys in the source data that don't exist in our mapping.

    :param probe: A tuple of extant keys found in the source data on import
    :param mapping: A dictionary of source data keys to keys that match dataclasses
    :return: None
    """
    for test_key in probe:
        if test_key not in mapping:
            raise RuntimeError(
                "An extant key in input data not found in fields mapping", test_key
            )


def validate_inputs(fname: str, fieldmap: dict[str, str]) -> Tuple[AnyRecord, ...]:
    """
    Create instances of dataclass from input data loaded from json returned by Airtable API.

    :param fname: String representing the name of the input file to process
    :param fieldmap: A dictionary mapping keys in API data to internal set of keys
    :return: A tuple of dataclass instances representing records
    """

    raw_json, extant_keys = load_from_file(fname)
    validated_inputs: Tuple[AnyRecord, ...] = ()

    validator_switch = {
        "accessions": AccessionSourceRecord,
        "entities": EntitySourceRecord,
        "items": ItemSourceRecord,
    }

    # Matching on the names of the source data files to be processed so we need a check
    try:
        validator = validator_switch[fname.split(".")[0].lower().strip()]
    except KeyError as err:
        print(
            "Unexpected input type: {}. Are you running against correct source data?".format(
                err
            )
        )
        raise

    try:
        check_key_mappings(extant_keys, fieldmap)
    except KeyError as err:
        print("Warning — {}. Key: {}".format(err.args[0], err.args[1]))

    for rec in raw_json:
        # Rename keys to match what dataclass expects
        rec = {fieldmap[name]: val for name, val in rec.items() if name in fieldmap}

        try:
            valid_input_record: AnyRecord = validator(**rec)
            validated_inputs += (valid_input_record,)
        except TypeError as e:
            print("Error loading record {}: {}".format(rec["airtable_idno"], e))

    return validated_inputs


if __name__ == "__main__":
    accessions = validate_inputs(
        "Accessions.json", sm.accessions_source_column_mappings
    )
    print("{} accessions processed without errors.\n".format(len(accessions)))

    entities = validate_inputs("Entities.json", sm.entities_source_column_mappings)
    print("{} entities processed without errors.\n".format(len(entities)))