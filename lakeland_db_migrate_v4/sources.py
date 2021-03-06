"""Handle input data coming from Airtable."""
import json
from pathlib import Path
from collections import defaultdict
from dataclasses import InitVar, field
from typing import Final, Union, TypeVar, Tuple, DefaultDict, Text, Optional, Any
from pydantic import Field, ValidationError
from pydantic.dataclasses import dataclass
from .utils import handle_paths


# TYPE HINTING HELPERS
# Loose type hints for json that comes back from Airtable
AIRTABLE_JSON = dict[str, Union[str, int, list[str]]]
# Beyond a certain point it's not worth caring how this data is structured
AIRTABLE_ATTACHMENTS_BLOB = Union[list[dict[str, Any]], dict[str, Any]]

# TODO: Figure out how to move these dataclass declarations
# to a separate file without mypy losing track of them
@dataclass(frozen=True)
class AirtableSourceRecord:
    """Base classs for Airtable records."""

    airtable_created_time: str
    airtable_idno: str


@dataclass(frozen=True)
class AccessionSourceRecord(AirtableSourceRecord):
    """An record from the Accessions table in the *source* base."""

    file_count: int
    donation_date: str
    donor_name: str
    file_array: Union[str, list[str]]
    idno: str
    linked_entity_array: Union[str, list[str]] = Field(default_factory=list)
    title: str = ""
    description: Text = ""
    legacy_idno_umd: str = ""
    ldt_check: str = ""


@dataclass(frozen=True)
class FileSourceRecord(AirtableSourceRecord):
    """A record from the Files table in the *source* base."""

    idno: str
    linked_accession: str
    virtual_location: InitVar[Optional[str]] = ""  # type: ignore[assignment]
    file_path: InitVar[Optional[str]] = ""  # type: ignore[assignment]
    legacy_idno_lchp: str = ""
    legacy_checksum: str = ""
    file_format: Union[str, list[str]] = ""
    part_of_item: str = ""
    locations: list[str] = field(init=False, default_factory=list)
    linked_entity_as_source: Union[str, list[str]] = Field(default_factory=list)

    def __post_init_post_parse__(self, virtual_location: str, file_path: str) -> None:
        """Handle the case of more than one file path."""
        all_locations = []

        if virtual_location is not None and virtual_location != "":
            all_locations.append(virtual_location)
        if file_path is not None:
            if file_path == "":
                object.__setattr__(self, "locations", [])
            if file_path == "NO FILE":
                object.__setattr__(self, "locations", [])
            else:
                paths = file_path.split('","')
                normed_paths = handle_paths(paths)
                all_locations.extend(normed_paths)
                object.__setattr__(self, "locations", all_locations)


@dataclass(frozen=True)
class ItemSourceRecord(AirtableSourceRecord):
    """A record from the Items table in the *source* base."""

    idno: str
    legacy_idno_umd: str
    linked_files_array: Union[str, list[str]]
    title: str = ""
    description: str = ""
    created_date: str = ""
    obj_type: str = ""
    category: Union[str, list[str]] = ""
    collection: str = ""
    lakeland_book_chapter: str = ""
    lakeland_book_page: str = ""
    legacy_idno_lchp: str = ""
    linked_entity_as_creator: Union[str, list[str]] = Field(default_factory=list)
    linked_entity_source: Union[str, list[str]] = Field(default_factory=list)
    linked_people: Union[str, list[str]] = Field(default_factory=list)
    linked_places_orgs: Union[str, list[str]] = Field(default_factory=list)
    linked_subjects: Union[str, list[str]] = Field(default_factory=list)
    linked_entity_interviewers: Union[str, list[str]] = Field(default_factory=list)
    linked_entity_interviewees: Union[str, list[str]] = Field(default_factory=list)
    interview_summary_attachment: AIRTABLE_ATTACHMENTS_BLOB = Field(
        default_factory=list
    )
    lakeland_book: bool = field(default=False)
    lakeland_video: bool = field(default=False)
    remove: str = ""


@dataclass(frozen=True)
class EntitySourceRecord(AirtableSourceRecord):
    """A record from the Entities table in the *source* base."""

    name: str
    linked_items_array: Union[str, list[str]] = Field(default_factory=list)
    linked_as_source: Union[str, list[str]] = Field(default_factory=list)
    linked_as_interviewer: Union[str, list[str]] = Field(default_factory=list)
    linked_as_interviewee: Union[str, list[str]] = Field(default_factory=list)
    linked_place_as_subject: Union[str, list[str]] = Field(default_factory=list)
    linked_to_item_as_creator: Union[str, list[str]] = Field(default_factory=list)
    linked_to_files_as_source: Union[str, list[str]] = Field(default_factory=list)
    linked_to_acc_as_donor: Union[str, list[str]] = Field(default_factory=list)
    auth_relations: Union[str, list[str]] = Field(default_factory=list)
    auth_relations_2: Union[str, list[str]] = Field(default_factory=list)
    address: str = ""
    latitude: str = ""
    longitude: str = ""
    alt_name: str = ""
    bio_hist: str = ""
    notes: str = ""
    category: str = ""
    lchp_source_code: str = ""


@dataclass(frozen=True)
class SubjectSourceRecord(AirtableSourceRecord):
    """A record from the Subjects table in the *source* base."""

    name: str
    linked_items_array: Union[str, list[str]]
    category: str = ""


@dataclass(frozen=True)
class EntityRelationshipSourceRecord(AirtableSourceRecord):
    """A record from the Relationships table in the *source* base."""

    name: str
    entity_1: str
    entity_2: str
    relation_type: str
    start_date: str = ""
    end_date: str = ""
    notes: str = ""


AnyRecord = TypeVar(
    "AnyRecord",
    AccessionSourceRecord,
    FileSourceRecord,
    EntitySourceRecord,
    ItemSourceRecord,
    SubjectSourceRecord,
    EntityRelationshipSourceRecord,
)

# LIBRARY FUNCTIONS
def load_from_file(fname: str) -> Tuple[list[AIRTABLE_JSON], Tuple[str, ...]]:
    """
    Load data from a json file representing the contents of a table from an Airtable base to be migrated.

    :param fname: A string representing the name of the file to load
    :return: A list of dictionaries representing the json data
    """
    V4_SOURCE_DATA_DIR: Final = Path().cwd() / "source_data"

    target_file: Path = Path.joinpath(V4_SOURCE_DATA_DIR, fname)
    target_data: list[AIRTABLE_JSON] = []

    try:
        with Path.open(target_file, "r") as fobject:
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
        "files": FileSourceRecord,
        "items": ItemSourceRecord,
        "entities": EntitySourceRecord,
        "items": ItemSourceRecord,
        "subjects": SubjectSourceRecord,
        "relationships": EntityRelationshipSourceRecord,
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
    except RuntimeError as err:
        print("Warning ??? {}. Key: {}".format(err.args[0], err.args[1]))
        raise

    for rec in raw_json:
        # Rename keys we get from Airtable to match what dataclass init expects
        rec = {fieldmap[name]: val for name, val in rec.items() if name in fieldmap}

        # Unwrap singletons
        for k in rec.keys():
            if isinstance(rec[k], list):
                if len(rec[k]) == 1:  # type: ignore[arg-type]
                    rec[k] = rec[k][0]  # type: ignore[index]
            else:
                pass

        try:
            valid_input_record: AirtableSourceRecord = validator(**rec)  # type: ignore[call-arg]
            validated_inputs += (valid_input_record,)
        except ValidationError as err:
            print(err)
        except TypeError as e:
            hint: str = ""
            cls_name = validator.__name__
            if cls_name == "AccessionSourceRecord":
                hint = "??? (Donor) {}".format(rec["donor_name"])
            if cls_name == "FileSourceRecord":
                hint = "??? (File) {}".format(rec["idno"])
            if cls_name == "ItemSourceRecord":
                hint = "??? (Item) {}".format(rec["idno"])
            if cls_name == "EntitySourceRecord":
                hint = "??? (Entity) {}".format(rec["name"])
            if cls_name == "SubjectSourceRecord":
                hint = "??? (Subject) {}".format(rec["name"])
            if cls_name == "EntityRelationshipSourceRecord":
                hint = "??? (Relationship) {}{}".format(rec["entity_1"], rec["name"])
            else:
                pass
            print(
                "Error loading record {} {}: {}".format(rec["airtable_idno"], hint, e)
            )
            pass

    return validated_inputs