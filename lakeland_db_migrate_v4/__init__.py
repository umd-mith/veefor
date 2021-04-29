"""Migrate Lakeland Digital Archive Airtable Data."""
import lakeland_db_migrate_v4.source_mappings
from .sources import validate_inputs
from .destinations import *

__version__ = "0.6.5"