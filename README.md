# Lakeland Digital Archive (LDA) database migration tools

This project contains bits and pieces to help migrate data to v4 of the LDA schema. The code here builds on ideas from [lakeland-data-munging](https://github.com/umd-mith/lakeland-data-munging)

## How to use this project

1. Grab a copy of the [latest release tarball](https://github.com/umd-mith/veefor/releases/latest)
2. Unpack somewhere on your python path
3. In a virtual environment of your choice: `pip install path/to/dist/gzip`
4. Do what you're gonna do

For an example of using these tools, see [this gist](https://gist.github.com/trevormunoz/8d4f5f1942392bd91c626cbb6b7decdd).

## How to develop on this project

Set up requires [poetry](https://python-poetry.org/) for now

1. Clone the repository
2. `poetry install`

To create a new release package: `poetry build`

I've been using [airtable-export](https://github.com/simonw/airtable-export) to get fresh copies of the source data. If data updates are needed, MITH Airtable credentials will be useful.
