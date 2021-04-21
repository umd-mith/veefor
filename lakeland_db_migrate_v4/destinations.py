"""Map data to v4 data model."""
from dataclasses import dataclass, InitVar, field
from typing import Text, Tuple, Union
from ulid import ULID

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

    idno: ULID


@dataclass
class MigratedRecord(V4BaseRecord):
    """A shared base class for records in the destination data model."""

    airtable_created_time: InitVar[str]
    airtable_idno: InitVar[str]
    source_record_hash: int = field(init=False)

    def __post_init__(self, airtable_idno: str, airtable_created_time: str) -> None:
        """Create a hash of id, created time for source record."""
        self.source_record_hash = hash((airtable_idno, airtable_created_time))


@dataclass
class DonationGroupingRecord(MigratedRecord):
    """A representation of a DonationGrouping in the destination data model."""

    donor_name: str
    donation_date: str
    donor_email: str
    donor_phone: str
    description: Text
    _v3_files_array: list[str] = field(repr=False, hash=False)
    title: str = ""
    legacy_idno: str = ""
    donation_consent: bool = field(default=False)


@dataclass
class FileRecord(MigratedRecord):
    """A representation of a File in the destination data model."""

    donation_grouping: str
    item: str
    created_time: str
    file_format: str
    location: str
    sha256_hexdigest: str
    size: int


@dataclass
class EntityRecord(MigratedRecord):
    """A representation of an Entity in the destination data model."""

    name: str
    entity_type: str
    date_of_birth: str
    date_of_death: str
    bio_hist: Text
    legacy_idno_lchp: str
    create_landing_page: bool = field(default=False)
    lakeland_video: bool = field(default=False)
    remove: bool = field(default=False)


@dataclass
class SubjectRecord(MigratedRecord):
    """A representation of a Subject in the destination data model."""

    name: str
    type: str


@dataclass
class ItemRecord(MigratedRecord):
    """A representation of an Item in the destination data model."""

    title: str
    description: str
    creation_date: str
    creation_year: int
    item_type: str
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
    linked_entities: list[EntityRecord]
    address: str
    latitude: float
    longitude: float


@dataclass
class PersonAdminRecord(V4BaseRecord):
    """A representation of AdminData about Entities in the destination data model."""

    name: str
    linked_entities: list[EntityRecord]
    lchp_team_member: bool = field(default=False)
    title: str = ""
    affiliation: str = ""
    email_address: str = ""


@dataclass
class EntityRelationshipRecord(MigratedRecord):
    """A representation of a pairwise relationship between Entities in the destination data model."""

    name: str
    subject_entity: EntityRecord
    object_entity: EntityRecord
    relationship_predicate: str
    relationship_start_date: str = ""
    relationship_end_date: str = ""