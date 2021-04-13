# Lakeland Digital Archive (LDA) database migration tools

This project contains scripts to migrate data to v4 of the LDA schema. The code here builds on ideas from [lakeland-data-munging](https://github.com/umd-mith/lakeland-data-munging)

## How to use

Set up requires [poetry](https://python-poetry.org/) for now

1. Clone the repository
2. `poetry install`
3. `poetry build`
4. In a virtual environment of your choice: `pip install path/to/dist/gzip`
5. Do what you're gonna do

Data files to be migrated are in `source_data.` I've been using [airtable-export](https://github.com/simonw/airtable-export) to get fresh copies of the data. If data updates are needed, MITH Airtable credentials will be useful.
