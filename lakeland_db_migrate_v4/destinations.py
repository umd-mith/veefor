"""Map data to v4 data model."""
from dataclasses import InitVar, field
from typing import Text, Tuple, Union
from pydantic import Field
from pydantic.dataclasses import dataclass

__all__ = [
    "DonationGroupingRecord",
    "FileRecord",
    "ItemRecord",
    "ItemLegacyInfoRecord",
    "ItemAdminRecord",
    "SubjectRecord",
    "EntityRecord",
    "LocationRecord",
    "PersonAdminRecord",
    "EntityRelationshipRecord",
]

# TYPE HINTING HELPERS
AIRTABLE_ATTACHMENTS_THUMBNAILS = dict[str, Union[int, str]]
AIRTABLE_ATTACHMENTS = list[dict[str, Union[str, int, AIRTABLE_ATTACHMENTS_THUMBNAILS]]]


@dataclass
class V4BaseRecord:
    """A shared base class for records in the destination data model."""

    idno: str


@dataclass
class MigratedRecord(V4BaseRecord):
    """A shared base class for records in the destination data model."""

    v3_airtable_created_time: str
    v3_airtable_idno: str


@dataclass
class DonationGroupingRecord(MigratedRecord):
    """A representation of a DonationGrouping in the destination data model."""

    donor_name: str
    donation_date: str
    donor_email: str
    donor_phone: str
    description: Text
    v3_files_array: Union[str, list[str]] = field(repr=False, hash=False)
    title: str = ""
    legacy_idno: str = ""
    donation_consent: bool = field(default=False)


@dataclass
class FileRecord(MigratedRecord):
    """A representation of a File in the destination data model."""

    donation_grouping_id: str
    item_id: str = ""  # Not all files have been itemized so could be empty
    created_time: str = field(default="", init=False)
    file_format: str = field(default="", init=False)
    location: str = field(default="", init=False)
    sha256_hexdigest: str = field(default="", init=False)
    size: int = field(default=0, init=False)


@dataclass
class EntityRecord(MigratedRecord):
    """A representation of an Entity in the destination data model."""

    name: str
    entity_type: str
    alt_name: str = ""
    date_of_birth: str = ""
    date_of_death: str = ""
    bio_hist: Text = ""
    legacy_idno_lchp: str = ""
    create_landing_page: bool = field(default=False)


@dataclass
class SubjectRecord(MigratedRecord):
    """A representation of a Subject in the destination data model."""

    name: str
    subject_type: str


@dataclass
class ItemRecord(MigratedRecord):
    """A representation of an Item in the destination data model."""

    title: str
    description: str
    creation_date: str
    item_type: Union[str, list[str]]
    collection: str
    creation_year: int = field(default_factory=int)
    linked_entities: list[EntityRecord] = field(default_factory=list)
    linked_entities_as_donors: list[EntityRecord] = field(default_factory=list)
    linked_entities_as_sources: list[EntityRecord] = field(default_factory=list)
    linked_entities_as_interviewers: list[EntityRecord] = field(default_factory=list)
    linked_entities_as_interviewees: list[EntityRecord] = field(default_factory=list)
    linked_subjects: list[SubjectRecord] = field(default_factory=list)
    duration: str = ""
    interview_summary_attachment: AIRTABLE_ATTACHMENTS = field(default_factory=list)
    interview_transcript_attachment: AIRTABLE_ATTACHMENTS = field(default_factory=list)


@dataclass
class ItemLegacyInfoRecord(V4BaseRecord):
    """A representation of legacy ids about Entities in the destination data model."""

    linked_item: ItemRecord
    legacy_idno_umd: str = ""
    legacy_ldt_image_idno: str = ""
    legacy_associated_filenames: list[str] = field(default_factory=list)


@dataclass
class ItemAdminRecord(V4BaseRecord):
    """A representation of AdminData about Entities in the destination data model."""

    linked_item: ItemRecord
    lakeland_book: bool = field(default=False)
    lakeland_book_chapter: str = ""
    lakeland_book_page: int = field(default_factory=int)
    lakeland_video: bool = field(default=False)
    remove: bool = field(default=False)


@dataclass
class LocationRecord(V4BaseRecord):
    """A representation of a Location in the destination data model."""

    name: str
    linked_entities: list[str]
    address: str
    latitude: float
    longitude: float


@dataclass
class PersonAdminRecord(V4BaseRecord):
    """A representation of AdminData about Entities in the destination data model."""

    name: str
    linked_entities: list[str]
    lchp_team_member: bool = field(default=False)
    title: str = ""
    affiliation: str = ""
    email_address: str = ""


@dataclass
class EntityRelationshipRecord(MigratedRecord):
    """A representation of a pairwise relationship between Entities in the destination data model."""

    name: str
    subject_entity: str
    object_entity: str
    relationship_predicate: str
    relationship_start_date: str = ""
    relationship_end_date: str = ""