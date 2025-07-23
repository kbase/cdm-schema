"""Sanity check script for schemas."""

from typing import TYPE_CHECKING

from linkml_runtime.linkml_model.meta import ClassDefinitionName, ElementName, EnumDefinitionName, TypeDefinitionName
from linkml_runtime.utils.schemaview import SchemaView

if TYPE_CHECKING:
    from linkml_runtime.linkml_model.meta import (
        ClassDefinition,
        ClassDefinitionName,
        EnumDefinition,
        EnumDefinitionName,
        SlotDefinition,
        SlotDefinitionName,
        TypeDefinition,
        TypeDefinitionName,
    )


def check_schema(sv: SchemaView) -> list[str]:
    """Check that a schema is minimally cohesive.

    :param sv: schema loaded into a SchemaView object
    :type sv: SchemaView
    :return: list of potential errors in the schema
    :rtype: list[str]
    """
    all_slots: dict[SlotDefinitionName, SlotDefinition] = sv.all_slots()
    all_types: dict[TypeDefinitionName, TypeDefinition] = sv.all_types()
    all_enums: dict[EnumDefinitionName, EnumDefinition] = sv.all_enums()
    all_classes: dict[ClassDefinitionName, ClassDefinition] = sv.all_classes()
    all_possible_ranges: set[TypeDefinitionName | EnumDefinitionName | ClassDefinitionName] = (
        set(all_types) | set(all_enums) | set(all_classes)
    )
    relationship_classes: dict[ClassDefinitionName, ClassDefinition] = {
        cl: cl_obj for cl, cl_obj in all_classes.items() if cl_obj.represents_relationship
    }

    all_slot_ranges: set[ElementName] = set()
    rslt = []
    rel_ix = {}
    mv_slots = {}
    for class_name in sv.all_classes():
        for slot in sv.class_induced_slots(class_name):
            if slot.name not in all_slots:
                rslt.append(f"{class_name}: {slot.name} not in sv.all_slots()")

            # check slot range is valid
            slot_range: set[ElementName] = set(sv.slot_range_as_union(slot))

            # ensure that if `Any` is in the slot range, there are other values
            if "Any" in slot_range and len(slot_range) == 1:
                rslt.append(f"{class_name}.{slot.name}: slot has range 'Any' with no limiter")

            rslt.extend(
                f"{class_name}.{slot.name}: range {range_name} not found"
                for range_name in slot_range
                if range_name not in all_possible_ranges
            )
            all_slot_ranges.update(slot_range)

            if slot.multivalued:
                mv_slots[f"{class_name}.{slot.name}"] = slot_range

            # if the slot range contains classes, these should be links
            if slot_range.issubset(set(all_classes)):
                rel_ix[f"{class_name}.{slot.name}"] = slot_range

    # if the slot range is a class, make sure that the class has an identifier
    slot_range_classes = {cl for cl in all_slot_ranges if cl in all_classes and cl != "Any"}
    for cl in slot_range_classes:
        id_slot = sv.get_identifier_slot(cl)
        if not id_slot:
            rslt.append(f"{cl}: class with no identifier slot used as range")

    return rslt


if __name__ == "__main__":
    sv = SchemaView("/Users/gwg/code/kbase/cdm-schema/src/schema/linkml/cdm_schema.yaml")
    sanity_checks = check_schema(sv)
    if sanity_checks:
        print("\n".join(sanity_checks))  # noqa: T201
