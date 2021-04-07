"""Handle input data coming from Airtable."""
import json
import pathlib
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Final, Union, Tuple, Text

# A pretty loose type hint for json that comes back from Airtable
AIRTABLE_JSON = dict[str, Union[str, int, list[str]]]


@dataclass(frozen=True)
class AirtableInput:
    airtable_created_time: str
    airtable_idno: str


@dataclass(frozen=True)
class AccessionRecord(AirtableInput):
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
class EntityRecord(AirtableInput):
    """A record from the Entities table in the *source* base."""

    name: str
    linked_items_array: list[str] = field(default_factory=list)
    bio_hist: str = ""
    category: str = ""


def load_from_file(fname: str) -> list[AIRTABLE_JSON]:
def load_from_file(fname: str) -> Tuple[list[AIRTABLE_JSON], Tuple[str, ...]]:
    """
    Load data from a json file representing the contents of a table from an Airtable base to be migrated.

    :param fname: A string representing the name of the file to load
    :return: A list of dictionaries representing the json data
    """
    V4_SOURCE_DATA_DIR: Final = pathlib.Path().cwd() / "source_data"

    target_file: pathlib.Path = pathlib.Path.joinpath(V4_SOURCE_DATA_DIR, fname)
    with pathlib.Path.open(target_file, "r") as fobject:
        target_data: list[AIRTABLE_JSON] = json.loads(fobject.read())

    return target_data
    # Grab all the keys actually used in records to check our mappings later
    key_collector: dict[str, str] = defaultdict()
    for jsonObj in target_data:
        for k in jsonObj.keys():
            key_collector[k] = ""

    uniq_keys: Tuple[str, ...] = tuple(key_collector.keys())

    return (target_data, uniq_keys)


def check_key_mappings(probe: Tuple[str, ...], mapping: dict[str, str]) -> None:
    for test_key in probe:
        if test_key not in mapping:
            raise KeyError(
                "An extant key in input data not found in fields mapping", test_key
            )


# Refactor these later, brute force it for now
def validate_accessions(fname: str) -> Tuple[AccessionRecord, ...]:
    raw_json = load_from_file(fname)
    raw_json, extant_keys = load_from_file(fname)
    accessions: Tuple[AccessionRecord, ...] = ()

    accessions_column_mappings = {
        "# Files": "file_count",
        "Date of Donation": "donation_date",
        "ID": "idno",
        "Description": "description",
        "Date of Donation": "donation_date",
        "Legacy ID-UMD": "legacy_idno_umd",
        "Donor Name (Form Entry)": "donor_name",
        "Donor Name (Linked)": "linked_entity_array",
        "Files": "file_array",
        "ID": "idno",
        "Legacy ID-UMD": "legacy_idno_umd",
        "Donation Grouping Title": "title",
        "# Files": "file_count",
        "LDT Check (Temp)": "_ldt_check",
        "airtable_createdTime": "airtable_created_time",
        "airtable_id": "airtable_idno",
    }

    try:
        check_key_mappings(extant_keys, accessions_column_mappings)
    except KeyError as err:
        print("Warning — {}. Key: {}".format(err.args[0], err.args[1]))

    for rec in raw_json:
        # Rename keys to match what dataclass expects
        rec = {
            accessions_column_mappings[name]: val
            for name, val in rec.items()
            if name in accessions_column_mappings
        }
        try:
            # TOFIX: Figure out why mypy complains about dictionary unpacking
            accession = AccessionRecord(**rec)  # type: ignore
            accessions += (accession,)
        except TypeError as e:
            print(
                "Error loading record {} from donor {}: {}".format(
                    rec["airtable_idno"], rec["donor_name"], e
                )
            )
            pass

    return accessions


def validate_entities(fname: str) -> Tuple[EntityRecord, ...]:
    raw_json = load_from_file(fname)
    raw_json, extant_keys = load_from_file(fname)
    entities: Tuple[EntityRecord, ...] = ()

    entities_column_mappings = {
        "Name": "name",
        "Biography/History": "bio_hist",
        "Notes": "notes",
        "Entity Category": "category",
        "Alternate Name": "alt_name",
        "Address": "address",
        "Date of Birth": "date_of_birth",
        "Date of Death": "date_of_death",
        "Latitude": "latitude",
        "Authority Relationships": "auth_relations",
        "Authority Relationships 2": "auth_relations_2",
        "Linked Oral Histories (Interviewees)": "linked_to_oral_history",
        "Linked Digital Objects (to Place)": "linked_to_place",
        "Longitude": "longitude",
        "Linked Digital Objects (Creators)": "linked_as_creator",
        "Linked Digital Objects (as Recipients)": "linked_as_recipient",
        "Linked Digital Objects (to Signatories)": "linked_as_signatory",
        "Source Code": "lchp_source_code",
        "Linked Digital Objects (Source)": "linked_as_source",
        "Items": "linked_items_generic",
        "Linked Items (EntityAsSubject)": "linked_items_array",
        "airtable_createdTime": "airtable_created_time",
        "airtable_id": "airtable_idno",
    }

    for rec in raw_json:
        rec = {
            entities_column_mappings[name]: val
            for name, val in rec.items()
            if name in entities_column_mappings
        }
        try:
            entity = EntityRecord(**rec)  # type: ignore
            entities += (entity,)
        except TypeError as e:
            print("Error loading record {}: {}".format(rec["name"], e))

    return entities


if __name__ == "__main__":
    ACCESSIONS = validate_accessions("Accessions.json")
    print("{} accessions processed without errors.\n".format(len(ACCESSIONS)))

    ENTITIES = validate_entities("Entities.json")
    print("{} entities processed without errors.\n".format(len(ENTITIES)))