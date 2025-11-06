"""Script to generate PySpark tables from a LinkML schema."""

import logging
from pathlib import Path

from linkml_runtime.utils.schemaview import SchemaView
from pyspark.sql.types import (
    ArrayType,
    BooleanType,
    DataType,
    DateType,
    FloatType,
    IntegerType,
    StringType,
    TimestampType,
)

from schema_sanity_check import check_schema

logger = logging.getLogger(__name__)

STRING = "STRING"
BOOL = "BOOLEAN"
FLOAT = "FLOAT"
INT = "INTEGER"
DATE = "DATE"
TS = "TIMESTAMP"

# Map LinkML types to PySpark types
TYPE_MAP = {
    "boolean": BOOL,
    "xsd:boolean": BOOL,
    # numerical
    "decimal": FLOAT,
    "double": FLOAT,
    "float": FLOAT,
    "integer": INT,
    "long": FLOAT,
    # dates and times
    "date": DATE,
    "dateTime": DATE,
    "time": TS,
    "xsd:date": DATE,
    "xsd:dateTime": DATE,
    "xsd:time": TS,
    "linkml:DateOrDatetime": DATE,
    # string-like
    "anyURI": STRING,
    "language": STRING,
    "str": STRING,
    "string": STRING,
    "shex:nonLiteral": STRING,
    "shex:iri": STRING,
}

remap = {
    STRING: StringType(),
    BOOL: BooleanType(),
    FLOAT: FloatType(),
    INT: IntegerType(),
    DATE: DateType(),
    TS: TimestampType(),
}


class SchemaViewWithProcessed(SchemaView):
    def __init__(self, *args, **kwargs) -> None:
        self.PROCESSED = {}
        self.RANGE_TO_TYPE = {}
        super().__init__(*args, **kwargs)


def resolve_slot_range_class_relational(sv: SchemaViewWithProcessed, class_name: str) -> set[str]:
    """Generate the appropriate slot range for a given class.

    :param sv: the schema, via SchemaView
    :type sv: SchemaView
    :param class_name: name of the class being used as a range
    :type class_name: str
    :return: set of spark datatype(s) to use
    :rtype: set[DataType]
    """
    # check for an identifier or a key
    class_id_slot = sv.get_identifier_slot(class_name, use_key=True)

    if not class_id_slot:
        msg = f"No identifier for class {class_name}"
        raise ValueError(msg)

    if not class_id_slot.range:
        msg = f"Class {class_name} identifier {class_id_slot.name} has no range: defaulting to string"
        logger.warning(msg)
        sv.RANGE_TO_TYPE[class_name] = STRING
        return {STRING}

    if class_id_slot.range in sv.all_classes():
        msg = f"Class {class_id_slot.range} used as range for identifier slot of class {class_name}"
        logger.warning(msg)
        sv.RANGE_TO_TYPE[class_name] = STRING
        return {STRING}

    return resolve_slot_range(sv, class_name=class_name, slot_name=class_id_slot.name, slot_range=class_id_slot.range)


def resolve_slot_range_type(sv: SchemaViewWithProcessed, type_name: str) -> set[str]:
    """Generate the appropriate slot range for a given type.

    :param sv: the schema, via SchemaView
    :type sv: SchemaView
    :param type_name: name of the type being used as a range
    :type type_name: str
    :return: set of spark datatype(s) to use
    :rtype: set[DataType]
    """
    type_obj = sv.get_type(type_name)
    type_uri = str(type_obj.uri) or type_obj.base
    if not type_uri:
        msg = f"type {type_name} lacks base and uri fields"
        logger.warning(msg)
        # add it to the mapping
        sv.RANGE_TO_TYPE[type_name] = STRING
        return {STRING}

    type_uri = type_uri.removeprefix("xsd:")
    return {TYPE_MAP.get(type_uri, STRING)}


def resolve_slot_range(sv: SchemaViewWithProcessed, class_name: str, slot_name: str, slot_range: str) -> set[str]:
    """Generate the appropriate spark datatype for a given slot_range.

    :param sv: the schema, via SchemaView
    :type sv: SchemaView
    :param class_name: name of the class that the slot belongs to
    :type class_name: str
    :param slot_name: name of the slot that the range belongs to
    :type slot_name: str
    :param slot_range: the slot range
    :type slot_range: str
    :return: set of spark datatype(s) to use
    :rtype: set[DataType]
    """
    if slot_range in sv.RANGE_TO_TYPE:
        return {sv.RANGE_TO_TYPE[slot_range]}

    if slot_range in sv.all_classes():
        return resolve_slot_range_class_relational(sv, slot_range)

    if slot_range in sv.all_types():
        return resolve_slot_range_type(sv, slot_range)

    # resolve enums as strings for now
    if slot_range in sv.all_enums():
        sv.RANGE_TO_TYPE[slot_range] = STRING
        return {STRING}

    if slot_range not in TYPE_MAP:
        msg = f"{class_name}.{slot_name} range {slot_range}: no type mapping found; using StringType()"
        logger.warning(msg)
        # add it to the mapping
        sv.RANGE_TO_TYPE[slot_range] = STRING
        return {STRING}

    return {TYPE_MAP[slot_range]}


def build_struct_for_class(
    sv: SchemaViewWithProcessed, class_name: str
) -> dict[str, tuple[str, DataType, bool]] | None:
    """Generate the appropriate Spark schema for a class in a LinkML schema.

    :param sv: the schema, via SchemaView
    :type sv: SchemaView
    :param class_name: LinkML schema class name
    :type class_name: str
    :return: the schema for the class, as a pyspark struct
    :rtype: StructType | None
    """
    if class_name in sv.PROCESSED:
        return sv.PROCESSED[class_name]

    # don't keep mixins or abstract classes
    class_def = sv.get_class(class_name, strict=True)
    if class_def.abstract or class_def.mixin:
        # skip it
        msg = f"{class_name}: skipping table generation: abstract or mixin class"
        logger.info(msg)
        sv.PROCESSED[class_name] = None
        return sv.PROCESSED[class_name]

    # don't do anything with the "Any" class
    if class_def.class_uri == "linkml:Any":
        # skip it
        msg = f"{class_name}: skipping table generation for `Any` class"
        logger.info(msg)
        sv.PROCESSED[class_name] = None
        return sv.PROCESSED[class_name]

    fields = {}
    for slot in sv.class_induced_slots(class_name):
        slot_range_set_raw = set(sv.slot_range_as_union(slot))
        if len(slot_range_set_raw) > 1 and "Any" in slot_range_set_raw:
            slot_range_set_raw.discard("Any")

        slot_range_resolved = set()

        for slot_range in slot_range_set_raw:
            # work out the type of each slot range
            slot_range_resolved.update(resolve_slot_range(sv, class_name, slot.name, slot_range))

        if len(slot_range_resolved) > 1:
            msg = f"WARNING: {class_name}.{slot.name}: more than one possible slot range: {', '.join(slot_range_resolved)}"
            logger.warning(msg)
            slot_range_resolved = {STRING}

        if len(slot_range_resolved) == 0:
            msg = f"ERROR: {class_name}.{slot.name} slot_range_set length is 0"
            logger.error(msg)

        multivalued = (slot.multivalued and not class_def.represents_relationship) or False
        if multivalued:
            msg = f"WARNING: {class_name}.{slot.name} is multivalued"
            logger.warning(msg)

        required = slot.required or False
        nested_type = slot_range_resolved.pop()
        dtype = ArrayType(nested_type, containsNull=False) if multivalued else nested_type
        fields[slot.name] = (dtype, not required)

    return fields


def generate_pyspark_from_sv(
    sv: SchemaViewWithProcessed, classes: list[str] | None = None
) -> dict[str, dict[str, tuple[DataType, bool]]]:
    """Generate pyspark tables from a LinkML schema.

    The schema should be flat (or flattened) into a relational form.

    :param sv: a LinkML schema, loaded into a SchemaView
    :type sv: SchemaView
    :param classes: list of class names to parse; defaults to None
    :type classes: list[str] | None
    :return: dictionary containing annotations for each field in each class of the schema, excluding abstract classes and mixins
    :rtype: dict[str, dict[str, tuple[DataType, bool]]]
    """
    spark_schemas = {}

    for class_name in classes or sv.all_classes():
        spark_schema = build_struct_for_class(sv, class_name)
        if spark_schema:
            spark_schemas[class_name] = spark_schema

    return spark_schemas


def write_output(
    sv: SchemaViewWithProcessed, output_path: Path, spark_schemas: dict[str, dict[str, tuple[DataType, bool]]]
) -> None:
    indent = " " * 4
    # extract all the types from the StructFields
    all_types = {remap[dt] for table_fields in spark_schemas.values() for dt, _ in table_fields.values()}
    header_material = [
        f'"""Automated conversion of {sv.schema.name} to PySpark."""',
        "",
        f"from pyspark.sql.types import {', '.join(sorted(['StructField', 'StructType', *[type(t).__name__ for t in all_types]]))}",
        "",
        "schema = {\n",
    ]

    with output_path.open("w") as f:
        f.write("\n".join(header_material))
        for table_name, table in sorted(spark_schemas.items()):
            f.write(
                "\n".join(
                    [
                        f'{indent}"{table_name}": StructType([',
                        *[
                            f'{indent}{indent}StructField("{name}", {remap[dtype]}, nullable={nullable}),'
                            for name, (dtype, nullable) in table.items()
                        ],
                        f"{indent}" + "]),\n",
                    ]
                )
            )
        f.write("}\n")

    print(f"PySpark schema written to {output_path}")


if __name__ == "__main__":
    sv = SchemaViewWithProcessed("./src/linkml/cdm_schema.yaml")

    sanity_checks = check_schema(sv)
    if sanity_checks:
        logger.warning("\n".join(sanity_checks))

    spark_schemas = generate_pyspark_from_sv(sv)
    output_path = Path(__file__).parent / "src" / "cdm_schema" / "kbase_cdm_pyspark.py"
    write_output(sv, output_path, spark_schemas)
