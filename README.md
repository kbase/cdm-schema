# cdm-schema

KBase CDM schema in linkml format.

## Website

[https://kbase.github.io/cdm-schema](https://kbase.github.io/cdm-schema)

## Repository Structure

* [src/](src/) - source files
  * [cdm_schema](src/cdm_schema)
    * [kbase_cdm_pydantic.py](src/cdm_schema/kbase_cdm_pydantic.py) -- CDM schema as Pydantic classes
    * [kbase_cdm_pyspark.py](src/cdm_schema/kbase_cdm_pyspark.py) -- the schema as PySpark data structures
    * [kbase_cdm.py](src/cdm_schema/kbase_cdm.py) -- plain old python classes
  * [linkml](src/linkml) -- LinkML schema source files

## Developer Documentation

<details>
Use the `make` command to generate project artefacts:

* `make gen-artefacts`: generate the Pydantic, python, and JSONschema versions of the schema

* `make deploy`: deploys site

</details>

## Credits

This project was made with
[linkml-project-cookiecutter](https://github.com/linkml/linkml-project-cookiecutter).
