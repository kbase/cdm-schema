# cdm-schema

KBase CDM schema in linkml format.

## Website

[https://kbase.github.io/cdm-schema](https://kbase.github.io/cdm-schema)

## Repository Structure

Please note that the [Pyspark data structures](src/cdm_schema/kbase_cdm_pyspark.py) are the recommended way to create schema-compliant CDM classes.

* [src/](src/) - source files
  * [cdm_schema](src/cdm_schema)
    * [kbase_cdm_pydantic.py](src/cdm_schema/kbase_cdm_pydantic.py) -- CDM schema as Pydantic classes
    * [kbase_cdm_pyspark.py](src/cdm_schema/kbase_cdm_pyspark.py) -- the schema as PySpark data structures
  * [linkml](src/linkml) -- LinkML schema source files

## Developer Documentation

Use the `make` command to generate project artefacts:

* `make gen-artefacts`: generate the Pydantic, pyspark, and JSONschema versions of the schema

* `make deploy`: deploys site

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).
