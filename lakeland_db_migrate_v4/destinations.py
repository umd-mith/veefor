"""Map data to v4 data model."""
import hashlib
from dataclasses import dataclass, InitVar, field
from typing import Text, Tuple


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
    title: str
    donation_date: str
    donor_email: str
    donor_phone: str
    description: Text
    donation_consent: bool = field(default=False)