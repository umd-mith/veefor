"""Map data to v4 data model."""
from dataclasses import dataclass, InitVar, field
from typing import Text, Tuple
from ulid import ULID


@dataclass
class V4BaseRecord:
    """A shared base class for records in the destination data model."""

    airtable_created_time: InitVar[str]
    airtable_idno: InitVar[str]
    source_record_hash: int = field(init=False)

    def __post_init__(self, airtable_idno: str, airtable_created_time: str) -> None:
        """Create a hash of id, created time for source record."""
        self.source_record_hash = hash((airtable_idno, airtable_created_time))


@dataclass
class DonationGroupingRecord(V4BaseRecord):
    """A representation of a DonationGrouping in the destination data model."""

    idno: str
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
class FileRecord(V4BaseRecord):
    """A representation of a File in the destination data model."""

    idno: str
    donation_grouping: str
    item: str
    created_time: str
    file_format: str
    location: str
    sha256_hexdigest: str
    size: int


@dataclass
class ItemRecord(V4BaseRecord):
    """A representation of an Item in the destination data model."""

    idno: str
    title: str
    description: str
    creation_date: str
    creation_year: int
    item_type: str
