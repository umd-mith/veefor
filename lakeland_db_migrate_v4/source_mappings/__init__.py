"""Map object keys we receive to internal keys."""
accessions_source_column_mappings: dict[str, str] = {
    "ID": "idno",
    "Description": "description",
    "Date of Donation": "donation_date",
    "Legacy ID-UMD": "legacy_idno_umd",
    "Donor Name (Form Entry)": "donor_name",
    "Donor Name (Linked)": "linked_entity_array",
    "Files": "file_array",
    "Donation Grouping Title": "title",
    "# Files": "file_count",
    "LDT Check (Temp)": "_ldt_check",
    "airtable_createdTime": "airtable_created_time",
    "airtable_id": "airtable_idno",
}

items_source_column_mappings: dict[str, str] = {
    "ID": "idno",
    "Accession": "linked_accessions_array",
    "File Count": "file_count",
    "Files": "linked_files_array",
    "airtable_createdTime": "airtable_created_time",
    "airtable_id": "airtable_idno",
}

entities_source_column_mappings: dict[str, str] = {
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
    "Linked Oral Histories (Interviewees)": "linked_as_interviewee",
    "Linked Oral Histories (as Interviewer)": "linked_as_interviewer",
    "Linked Digital Objects (to Place)": "linked_to_place",
    "Longitude": "longitude",
    "Linked Digital Objects (Creators)": "linked_to_dobj_as_creator",
    "Linked Digital Objects (as Recipients)": "linked_as_recipient",
    "Linked Digital Objects (to Signatories)": "linked_as_signatory",
    "Accessions (as Donor)": "linked_to_acc_as_donor",
    "Source Code": "lchp_source_code",
    "Linked Digital Objects (Source)": "linked_as_source",
    "Linked Files (as Source)": "linked_to_files_as_source",
    "Items": "linked_items_generic",
    "Linked Items (EntityAsSubject)": "linked_items_array",
    "Linked Items (Place as Subject)": "linked_place_as_subject",
    "Linked Items (as Creator)": "linked_to_item_as_creator",
    "airtable_createdTime": "airtable_created_time",
    "airtable_id": "airtable_idno",
}

subjects_source_column_mappings: dict[str, str] = {
    "Name": "name",
    "Subject Category": "category",
    "Items": "linked_items_array",
    "airtable_createdTime": "airtable_created_time",
    "airtable_id": "airtable_idno",
}
