# Auto generated from cdm_schema.yaml by pythongen.py version: 0.0.1
# Generation date: 2025-07-23T08:55:17
# Schema: cdm_schema
#
# id: http://kbase.github.io/cdm-schema/cdm_schema
# description: Schema for KBase CDM
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, ClassVar, Dict, List, Optional, Union

from jsonasobj2 import JsonObj, as_dict
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from linkml_runtime.utils.formatutils import camelcase, sfx, underscore
from linkml_runtime.utils.metamodelcore import bnode, empty_dict, empty_list
from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_float, extended_int, extended_str
from rdflib import Namespace, URIRef

from linkml_runtime.linkml_model.types import Boolean, Curie, Float, Integer, Ncname, String, Uri, Uriorcurie
from linkml_runtime.utils.metamodelcore import Bool, Curie, NCName, URI, URIorCURIE

metamodel_version = "1.7.0"
version = "0.0.1"

# Namespaces
DATACITE = CurieNamespace("DataCite", "http://example.org/UNKNOWN/DataCite/")
JGI = CurieNamespace("JGI", "http://example.org/UNKNOWN/JGI/")
ORCID = CurieNamespace("ORCID", "http://example.org/UNKNOWN/ORCID/")
OSTI_ARTICLE = CurieNamespace("OSTI_ARTICLE", "http://example.org/UNKNOWN/OSTI.ARTICLE/")
KB_CDM = CurieNamespace("kb_cdm", "http://kbase.github.io/cdm-schema/")
LINKML = CurieNamespace("linkml", "https://w3id.org/linkml/")
MIXS = CurieNamespace("mixs", "https://genomicsstandardsconsortium.github.io/mixs/")
NMDC = CurieNamespace("nmdc", "http://example.org/UNKNOWN/nmdc/")
RDF = CurieNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
SCHEMA = CurieNamespace("schema", "http://schema.org/")
SH = CurieNamespace("sh", "http://www.w3.org/ns/shacl#")
XSD = CurieNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
DEFAULT_ = KB_CDM


# Types
class Iso8601(str):
    """A date in ISO 8601 format, e.g. 2024-04-05T12:34:56Z. "Z" indicates UTC time."""

    type_class_uri = XSD["dateTime"]
    type_class_curie = "xsd:dateTime"
    type_name = "iso8601"
    type_model_uri = KB_CDM.Iso8601


class NodeIdType(Uriorcurie):
    """IDs are either CURIEs, IRI, or blank nodes. IRIs are wrapped in <>s to distinguish them from CURIEs, but in general it is good practice to populate the [prefixes][Prefixes.md] table such that they are shortened to CURIEs. Blank nodes are ids starting with `_:`."""

    type_class_uri = XSD["anyURI"]
    type_class_curie = "xsd:anyURI"
    type_name = "node_id_type"
    type_model_uri = KB_CDM.NodeIdType


class LiteralAsStringType(String):
    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "literal_as_string_type"
    type_model_uri = KB_CDM.LiteralAsStringType


class UUID(Uriorcurie):
    """A universally unique ID, generated using uuid4, with the prefix "CDM:"."""

    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "UUID"
    type_model_uri = KB_CDM.UUID


class LocalCurie(Uriorcurie):
    """A CURIE that exists as a subject in the `statements` table (i.e. `Statements.subject`). Should not be used for external identifiers."""

    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "local_curie"
    type_model_uri = KB_CDM.LocalCurie


class DataSourceUuid(UUID):
    """A UUID that identifies a data source in the CDM."""

    type_class_uri = XSD["string"]
    type_class_curie = "xsd:string"
    type_name = "data_source_uuid"
    type_model_uri = KB_CDM.DataSourceUuid


# Class references
class AssociationAssociationId(UUID):
    pass


class ClusterClusterId(UUID):
    pass


class ContigContigId(UUID):
    pass


class ContigCollectionContigCollectionId(UUID):
    pass


class ContributorContributorId(UUID):
    pass


class DataSourceDataSourceId(UUID):
    pass


class EncodedFeatureEncodedFeatureId(UUID):
    pass


class GoldEnvironmentalContextGoldEnvironmentalContextId(UUID):
    pass


class MixsEnvironmentalContextMixsEnvironmentalContextId(UUID):
    pass


class EventEventId(UUID):
    pass


class ExperimentExperimentId(UUID):
    pass


class FeatureFeatureId(UUID):
    pass


class ProjectProjectId(UUID):
    pass


class ProteinProteinId(UUID):
    pass


class ProtocolProtocolId(UUID):
    pass


class ProtocolParticipantProtocolParticipantId(UUID):
    pass


class PublicationPublicationId(URIorCURIE):
    pass


class SampleSampleId(UUID):
    pass


class MeasurementMeasurementId(UUID):
    pass


class ProcessedMeasurementMeasurementId(MeasurementMeasurementId):
    pass


class EntityEntityId(UUID):
    pass


Any = Any


class Table(YAMLRoot):
    """
    root class for all schema entities
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Table"]
    class_class_curie: ClassVar[str] = "kb_cdm:Table"
    class_name: ClassVar[str] = "Table"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Table


@dataclass(repr=False)
class AssociationXPublication(Table):
    """
    Links associations to supporting literature.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["AssociationXPublication"]
    class_class_curie: ClassVar[str] = "kb_cdm:AssociationXPublication"
    class_name: ClassVar[str] = "Association_X_Publication"
    class_model_uri: ClassVar[URIRef] = KB_CDM.AssociationXPublication

    association_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None
    publication_id: Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.association_id):
            self.MissingRequiredField("association_id")
        if not isinstance(self.association_id, list):
            self.association_id = [self.association_id] if self.association_id is not None else []
        self.association_id = [v if isinstance(v, UUID) else UUID(v) for v in self.association_id]

        if self._is_empty(self.publication_id):
            self.MissingRequiredField("publication_id")
        if not isinstance(self.publication_id, list):
            self.publication_id = [self.publication_id] if self.publication_id is not None else []
        self.publication_id = [v if isinstance(v, URIorCURIE) else URIorCURIE(v) for v in self.publication_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AssociationXSupportingObject(Table):
    """
    Links associations to entities to capture supporting objects in an association. ay be a biological entity, such as
    a protein or feature, or a URL to a resource (e.g. a publication) that supports the association. Where possible,
    CDM identifiers should be used.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["AssociationXSupportingObject"]
    class_class_curie: ClassVar[str] = "kb_cdm:AssociationXSupportingObject"
    class_name: ClassVar[str] = "Association_X_SupportingObject"
    class_model_uri: ClassVar[URIRef] = KB_CDM.AssociationXSupportingObject

    association_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None
    entity_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.association_id):
            self.MissingRequiredField("association_id")
        if not isinstance(self.association_id, list):
            self.association_id = [self.association_id] if self.association_id is not None else []
        self.association_id = [v if isinstance(v, UUID) else UUID(v) for v in self.association_id]

        if self._is_empty(self.entity_id):
            self.MissingRequiredField("entity_id")
        if not isinstance(self.entity_id, list):
            self.entity_id = [self.entity_id] if self.entity_id is not None else []
        self.entity_id = [v if isinstance(v, UUID) else UUID(v) for v in self.entity_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContigXContigCollection(Table):
    """
    Captures the relationship between a contig and a contig collection; equivalent to contig part-of contig collection.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContigXContigCollection"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContigXContigCollection"
    class_name: ClassVar[str] = "Contig_X_ContigCollection"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContigXContigCollection

    contig_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None
    contig_collection_id: Union[str, UUID] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_id):
            self.MissingRequiredField("contig_id")
        if not isinstance(self.contig_id, list):
            self.contig_id = [self.contig_id] if self.contig_id is not None else []
        self.contig_id = [v if isinstance(v, UUID) else UUID(v) for v in self.contig_id]

        if self._is_empty(self.contig_collection_id):
            self.MissingRequiredField("contig_collection_id")
        if not isinstance(self.contig_collection_id, UUID):
            self.contig_collection_id = UUID(self.contig_collection_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContigXEncodedFeature(Table):
    """
    Captures the relationship between a contig and an encoded feature.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContigXEncodedFeature"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContigXEncodedFeature"
    class_name: ClassVar[str] = "Contig_X_EncodedFeature"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContigXEncodedFeature

    contig_id: Union[str, UUID] = None
    encoded_feature_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_id):
            self.MissingRequiredField("contig_id")
        if not isinstance(self.contig_id, UUID):
            self.contig_id = UUID(self.contig_id)

        if self._is_empty(self.encoded_feature_id):
            self.MissingRequiredField("encoded_feature_id")
        if not isinstance(self.encoded_feature_id, list):
            self.encoded_feature_id = [self.encoded_feature_id] if self.encoded_feature_id is not None else []
        self.encoded_feature_id = [v if isinstance(v, UUID) else UUID(v) for v in self.encoded_feature_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContigXFeature(Table):
    """
    Captures the relationship between a contig and a feature; equivalent to feature part-of contig.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContigXFeature"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContigXFeature"
    class_name: ClassVar[str] = "Contig_X_Feature"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContigXFeature

    contig_id: Union[str, UUID] = None
    feature_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_id):
            self.MissingRequiredField("contig_id")
        if not isinstance(self.contig_id, UUID):
            self.contig_id = UUID(self.contig_id)

        if self._is_empty(self.feature_id):
            self.MissingRequiredField("feature_id")
        if not isinstance(self.feature_id, list):
            self.feature_id = [self.feature_id] if self.feature_id is not None else []
        self.feature_id = [v if isinstance(v, UUID) else UUID(v) for v in self.feature_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContigXProtein(Table):
    """
    Captures the relationship between a contig and a protein; equivalent to protein is ribosomal translation of
    (http://purl.obolibrary.org/obo/RO_0002512) contig.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContigXProtein"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContigXProtein"
    class_name: ClassVar[str] = "Contig_X_Protein"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContigXProtein

    contig_id: Union[str, UUID] = None
    protein_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_id):
            self.MissingRequiredField("contig_id")
        if not isinstance(self.contig_id, UUID):
            self.contig_id = UUID(self.contig_id)

        if self._is_empty(self.protein_id):
            self.MissingRequiredField("protein_id")
        if not isinstance(self.protein_id, list):
            self.protein_id = [self.protein_id] if self.protein_id is not None else []
        self.protein_id = [v if isinstance(v, UUID) else UUID(v) for v in self.protein_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContigCollectionXEncodedFeature(Table):
    """
    Captures the relationship between a contig collection and an encoded feature.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContigCollectionXEncodedFeature"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContigCollectionXEncodedFeature"
    class_name: ClassVar[str] = "ContigCollection_X_EncodedFeature"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContigCollectionXEncodedFeature

    contig_collection_id: Union[str, UUID] = None
    encoded_feature_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_collection_id):
            self.MissingRequiredField("contig_collection_id")
        if not isinstance(self.contig_collection_id, UUID):
            self.contig_collection_id = UUID(self.contig_collection_id)

        if self._is_empty(self.encoded_feature_id):
            self.MissingRequiredField("encoded_feature_id")
        if not isinstance(self.encoded_feature_id, list):
            self.encoded_feature_id = [self.encoded_feature_id] if self.encoded_feature_id is not None else []
        self.encoded_feature_id = [v if isinstance(v, UUID) else UUID(v) for v in self.encoded_feature_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContigCollectionXFeature(Table):
    """
    Captures the relationship between a contig collection and a feature; equivalent to feature part-of contig
    collection.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContigCollectionXFeature"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContigCollectionXFeature"
    class_name: ClassVar[str] = "ContigCollection_X_Feature"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContigCollectionXFeature

    contig_collection_id: Union[str, UUID] = None
    feature_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_collection_id):
            self.MissingRequiredField("contig_collection_id")
        if not isinstance(self.contig_collection_id, UUID):
            self.contig_collection_id = UUID(self.contig_collection_id)

        if self._is_empty(self.feature_id):
            self.MissingRequiredField("feature_id")
        if not isinstance(self.feature_id, list):
            self.feature_id = [self.feature_id] if self.feature_id is not None else []
        self.feature_id = [v if isinstance(v, UUID) else UUID(v) for v in self.feature_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContigCollectionXProtein(Table):
    """
    Captures the relationship between a contig collection and a protein; equivalent to protein is ribosomal
    translation of (http://purl.obolibrary.org/obo/RO_0002512) contig collection.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContigCollectionXProtein"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContigCollectionXProtein"
    class_name: ClassVar[str] = "ContigCollection_X_Protein"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContigCollectionXProtein

    contig_collection_id: Union[str, UUID] = None
    protein_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_collection_id):
            self.MissingRequiredField("contig_collection_id")
        if not isinstance(self.contig_collection_id, UUID):
            self.contig_collection_id = UUID(self.contig_collection_id)

        if self._is_empty(self.protein_id):
            self.MissingRequiredField("protein_id")
        if not isinstance(self.protein_id, list):
            self.protein_id = [self.protein_id] if self.protein_id is not None else []
        self.protein_id = [v if isinstance(v, UUID) else UUID(v) for v in self.protein_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContributorXRoleXExperiment(Table):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContributorXRoleXExperiment"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContributorXRoleXExperiment"
    class_name: ClassVar[str] = "Contributor_X_Role_X_Experiment"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContributorXRoleXExperiment

    contributor_id: Union[str, UUID] = None
    experiment_id: Union[str, UUID] = None
    contributor_role: Optional[Union[str, "ContributorRole"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contributor_id):
            self.MissingRequiredField("contributor_id")
        if not isinstance(self.contributor_id, UUID):
            self.contributor_id = UUID(self.contributor_id)

        if self._is_empty(self.experiment_id):
            self.MissingRequiredField("experiment_id")
        if not isinstance(self.experiment_id, UUID):
            self.experiment_id = UUID(self.experiment_id)

        if self.contributor_role is not None and not isinstance(self.contributor_role, ContributorRole):
            self.contributor_role = ContributorRole(self.contributor_role)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContributorXRoleXProject(Table):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContributorXRoleXProject"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContributorXRoleXProject"
    class_name: ClassVar[str] = "Contributor_X_Role_X_Project"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContributorXRoleXProject

    contributor_id: Union[str, UUID] = None
    project_id: Union[str, UUID] = None
    contributor_role: Optional[Union[str, "ContributorRole"]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contributor_id):
            self.MissingRequiredField("contributor_id")
        if not isinstance(self.contributor_id, UUID):
            self.contributor_id = UUID(self.contributor_id)

        if self._is_empty(self.project_id):
            self.MissingRequiredField("project_id")
        if not isinstance(self.project_id, UUID):
            self.project_id = UUID(self.project_id)

        if self.contributor_role is not None and not isinstance(self.contributor_role, ContributorRole):
            self.contributor_role = ContributorRole(self.contributor_role)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EncodedFeatureXFeature(Table):
    """
    Captures the relationship between a feature and its transcription product.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["EncodedFeatureXFeature"]
    class_class_curie: ClassVar[str] = "kb_cdm:EncodedFeatureXFeature"
    class_name: ClassVar[str] = "EncodedFeature_X_Feature"
    class_model_uri: ClassVar[URIRef] = KB_CDM.EncodedFeatureXFeature

    encoded_feature_id: Union[str, UUID] = None
    feature_id: Union[str, UUID] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoded_feature_id):
            self.MissingRequiredField("encoded_feature_id")
        if not isinstance(self.encoded_feature_id, UUID):
            self.encoded_feature_id = UUID(self.encoded_feature_id)

        if self._is_empty(self.feature_id):
            self.MissingRequiredField("feature_id")
        if not isinstance(self.feature_id, UUID):
            self.feature_id = UUID(self.feature_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EntityXMeasurement(Table):
    """
    Captures a measurement made on an entity.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["EntityXMeasurement"]
    class_class_curie: ClassVar[str] = "kb_cdm:EntityXMeasurement"
    class_name: ClassVar[str] = "Entity_X_Measurement"
    class_model_uri: ClassVar[URIRef] = KB_CDM.EntityXMeasurement

    entity_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None
    measurement_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.entity_id):
            self.MissingRequiredField("entity_id")
        if not isinstance(self.entity_id, list):
            self.entity_id = [self.entity_id] if self.entity_id is not None else []
        self.entity_id = [v if isinstance(v, UUID) else UUID(v) for v in self.entity_id]

        if self._is_empty(self.measurement_id):
            self.MissingRequiredField("measurement_id")
        if not isinstance(self.measurement_id, list):
            self.measurement_id = [self.measurement_id] if self.measurement_id is not None else []
        self.measurement_id = [v if isinstance(v, UUID) else UUID(v) for v in self.measurement_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExperimentXProject(Table):
    """
    Captures the relationship between an experiment and the project that it is a part of.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ExperimentXProject"]
    class_class_curie: ClassVar[str] = "kb_cdm:ExperimentXProject"
    class_name: ClassVar[str] = "Experiment_X_Project"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ExperimentXProject

    experiment_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None
    project_id: Union[str, UUID] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.experiment_id):
            self.MissingRequiredField("experiment_id")
        if not isinstance(self.experiment_id, list):
            self.experiment_id = [self.experiment_id] if self.experiment_id is not None else []
        self.experiment_id = [v if isinstance(v, UUID) else UUID(v) for v in self.experiment_id]

        if self._is_empty(self.project_id):
            self.MissingRequiredField("project_id")
        if not isinstance(self.project_id, UUID):
            self.project_id = UUID(self.project_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ExperimentXSample(Table):
    """
    Represents the participation of a sample in an experiment.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ExperimentXSample"]
    class_class_curie: ClassVar[str] = "kb_cdm:ExperimentXSample"
    class_name: ClassVar[str] = "Experiment_X_Sample"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ExperimentXSample

    experiment_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None
    sample_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.experiment_id):
            self.MissingRequiredField("experiment_id")
        if not isinstance(self.experiment_id, list):
            self.experiment_id = [self.experiment_id] if self.experiment_id is not None else []
        self.experiment_id = [v if isinstance(v, UUID) else UUID(v) for v in self.experiment_id]

        if self._is_empty(self.sample_id):
            self.MissingRequiredField("sample_id")
        if not isinstance(self.sample_id, list):
            self.sample_id = [self.sample_id] if self.sample_id is not None else []
        self.sample_id = [v if isinstance(v, UUID) else UUID(v) for v in self.sample_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class FeatureXProtein(Table):
    """
    Captures the relationship between a feature and a protein; equivalent to feature encodes protein.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["FeatureXProtein"]
    class_class_curie: ClassVar[str] = "kb_cdm:FeatureXProtein"
    class_name: ClassVar[str] = "Feature_X_Protein"
    class_model_uri: ClassVar[URIRef] = KB_CDM.FeatureXProtein

    feature_id: Union[str, UUID] = None
    protein_id: Union[Union[str, UUID], list[Union[str, UUID]]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.feature_id):
            self.MissingRequiredField("feature_id")
        if not isinstance(self.feature_id, UUID):
            self.feature_id = UUID(self.feature_id)

        if self._is_empty(self.protein_id):
            self.MissingRequiredField("protein_id")
        if not isinstance(self.protein_id, list):
            self.protein_id = [self.protein_id] if self.protein_id is not None else []
        self.protein_id = [v if isinstance(v, UUID) else UUID(v) for v in self.protein_id]

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProtocolXProtocolParticipant(Table):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ProtocolXProtocolParticipant"]
    class_class_curie: ClassVar[str] = "kb_cdm:ProtocolXProtocolParticipant"
    class_name: ClassVar[str] = "Protocol_X_ProtocolParticipant"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ProtocolXProtocolParticipant

    protocol_id: Union[str, UUID] = None
    protocol_participant_id: Union[str, ProtocolParticipantProtocolParticipantId] = None
    participant_type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.protocol_id):
            self.MissingRequiredField("protocol_id")
        if not isinstance(self.protocol_id, UUID):
            self.protocol_id = UUID(self.protocol_id)

        if self._is_empty(self.protocol_participant_id):
            self.MissingRequiredField("protocol_participant_id")
        if not isinstance(self.protocol_participant_id, ProtocolParticipantProtocolParticipantId):
            self.protocol_participant_id = ProtocolParticipantProtocolParticipantId(self.protocol_participant_id)

        if self.participant_type is not None and not isinstance(self.participant_type, str):
            self.participant_type = str(self.participant_type)

        super().__post_init__(**kwargs)


class NamedEntity(Table):
    """
    Represents the link between an entity and its names.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["NamedEntity"]
    class_class_curie: ClassVar[str] = "kb_cdm:NamedEntity"
    class_name: ClassVar[str] = "NamedEntity"
    class_model_uri: ClassVar[URIRef] = KB_CDM.NamedEntity


class IdentifiedEntity(Table):
    """
    Represents the link between an entity and its identifiers.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["IdentifiedEntity"]
    class_class_curie: ClassVar[str] = "kb_cdm:IdentifiedEntity"
    class_name: ClassVar[str] = "IdentifiedEntity"
    class_model_uri: ClassVar[URIRef] = KB_CDM.IdentifiedEntity


class AttributeValueEntity(Table):
    """
    Represents the link between an entity and its attribute values.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["AttributeValueEntity"]
    class_class_curie: ClassVar[str] = "kb_cdm:AttributeValueEntity"
    class_name: ClassVar[str] = "AttributeValueEntity"
    class_model_uri: ClassVar[URIRef] = KB_CDM.AttributeValueEntity


@dataclass(repr=False)
class Association(Table):
    """
    An association between an object--typically an entity such as a protein or a feature--and a classification system
    or ontology, such as the Gene Ontology, the Enzyme Classification, or TIGRFAMS domains.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Association"]
    class_class_curie: ClassVar[str] = "kb_cdm:Association"
    class_name: ClassVar[str] = "Association"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Association

    association_id: Union[str, AssociationAssociationId] = None
    subject: Union[dict, Any] = None
    object: Union[str, LocalCurie] = None
    predicate: Optional[Union[str, LocalCurie]] = None
    negated: Optional[Union[bool, Bool]] = None
    evidence_type: Optional[Union[str, LocalCurie]] = None
    primary_knowledge_source: Optional[Union[str, URIorCURIE]] = None
    aggregator_knowledge_source: Optional[Union[str, URIorCURIE]] = None
    annotation_date: Optional[str] = None
    comments: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.association_id):
            self.MissingRequiredField("association_id")
        if not isinstance(self.association_id, AssociationAssociationId):
            self.association_id = AssociationAssociationId(self.association_id)

        if self._is_empty(self.object):
            self.MissingRequiredField("object")
        if not isinstance(self.object, LocalCurie):
            self.object = LocalCurie(self.object)

        if self.predicate is not None and not isinstance(self.predicate, LocalCurie):
            self.predicate = LocalCurie(self.predicate)

        if self.negated is not None and not isinstance(self.negated, Bool):
            self.negated = Bool(self.negated)

        if self.evidence_type is not None and not isinstance(self.evidence_type, LocalCurie):
            self.evidence_type = LocalCurie(self.evidence_type)

        if self.primary_knowledge_source is not None and not isinstance(self.primary_knowledge_source, URIorCURIE):
            self.primary_knowledge_source = URIorCURIE(self.primary_knowledge_source)

        if self.aggregator_knowledge_source is not None and not isinstance(
            self.aggregator_knowledge_source, URIorCURIE
        ):
            self.aggregator_knowledge_source = URIorCURIE(self.aggregator_knowledge_source)

        if self.annotation_date is not None and not isinstance(self.annotation_date, str):
            self.annotation_date = str(self.annotation_date)

        if self.comments is not None and not isinstance(self.comments, str):
            self.comments = str(self.comments)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Cluster(Table):
    """
    Represents an individual execution of a clustering protocol. See the ClusterMember class for clustering results.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Cluster"]
    class_class_curie: ClassVar[str] = "kb_cdm:Cluster"
    class_name: ClassVar[str] = "Cluster"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Cluster

    cluster_id: Union[str, ClusterClusterId] = None
    entity_type: Union[str, "ClusterType"] = None
    description: Optional[str] = None
    name: Optional[str] = None
    protocol_id: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.cluster_id):
            self.MissingRequiredField("cluster_id")
        if not isinstance(self.cluster_id, ClusterClusterId):
            self.cluster_id = ClusterClusterId(self.cluster_id)

        if self._is_empty(self.entity_type):
            self.MissingRequiredField("entity_type")
        if not isinstance(self.entity_type, ClusterType):
            self.entity_type = ClusterType(self.entity_type)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.protocol_id is not None and not isinstance(self.protocol_id, str):
            self.protocol_id = str(self.protocol_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ClusterMember(Table):
    """
    Relationship representing membership of a cluster. An optional score can be assigned to each cluster member.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ClusterMember"]
    class_class_curie: ClassVar[str] = "kb_cdm:ClusterMember"
    class_name: ClassVar[str] = "ClusterMember"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ClusterMember

    cluster_id: Union[str, UUID] = None
    entity_id: Union[str, UUID] = None
    is_representative: Optional[Union[bool, Bool]] = False
    is_seed: Optional[Union[bool, Bool]] = False
    score: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.cluster_id):
            self.MissingRequiredField("cluster_id")
        if not isinstance(self.cluster_id, UUID):
            self.cluster_id = UUID(self.cluster_id)

        if self._is_empty(self.entity_id):
            self.MissingRequiredField("entity_id")
        if not isinstance(self.entity_id, UUID):
            self.entity_id = UUID(self.entity_id)

        if self.is_representative is not None and not isinstance(self.is_representative, Bool):
            self.is_representative = Bool(self.is_representative)

        if self.is_seed is not None and not isinstance(self.is_seed, Bool):
            self.is_seed = Bool(self.is_seed)

        if self.score is not None and not isinstance(self.score, float):
            self.score = float(self.score)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Contig(Table):
    """
    A contig (derived from the word "contiguous") is a set of DNA segments or sequences that overlap in a way that
    provides a contiguous representation of a genomic region. A contig should not contain any gaps.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Contig"]
    class_class_curie: ClassVar[str] = "kb_cdm:Contig"
    class_name: ClassVar[str] = "Contig"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Contig

    contig_id: Union[str, ContigContigId] = None
    hash: Optional[str] = None
    gc_content: Optional[float] = None
    length: Optional[int] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_id):
            self.MissingRequiredField("contig_id")
        if not isinstance(self.contig_id, ContigContigId):
            self.contig_id = ContigContigId(self.contig_id)

        if self.hash is not None and not isinstance(self.hash, str):
            self.hash = str(self.hash)

        if self.gc_content is not None and not isinstance(self.gc_content, float):
            self.gc_content = float(self.gc_content)

        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ContigCollection(Table):
    """
    A set of individual, overlapping contigs that represent the complete sequenced genome of an organism.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ContigCollection"]
    class_class_curie: ClassVar[str] = "kb_cdm:ContigCollection"
    class_name: ClassVar[str] = "ContigCollection"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ContigCollection

    contig_collection_id: Union[str, ContigCollectionContigCollectionId] = None
    hash: Optional[str] = None
    asm_score: Optional[float] = None
    checkm2_completeness: Optional[float] = None
    checkm2_contamination: Optional[float] = None
    contig_bp: Optional[int] = None
    contig_collection_type: Optional[Union[str, "ContigCollectionType"]] = None
    ctg_L50: Optional[int] = None
    ctg_L90: Optional[int] = None
    ctg_N50: Optional[int] = None
    ctg_N90: Optional[int] = None
    ctg_logsum: Optional[float] = None
    ctg_max: Optional[int] = None
    ctg_powsum: Optional[float] = None
    gap_pct: Optional[float] = None
    gc_avg: Optional[float] = None
    gc_std: Optional[float] = None
    n_contigs: Optional[int] = None
    n_scaffolds: Optional[int] = None
    scaf_L50: Optional[int] = None
    scaf_L90: Optional[int] = None
    scaf_N50: Optional[int] = None
    scaf_N90: Optional[int] = None
    scaf_bp: Optional[int] = None
    scaf_l_gt50k: Optional[int] = None
    scaf_logsum: Optional[float] = None
    scaf_max: Optional[int] = None
    scaf_n_gt50K: Optional[int] = None
    scaf_pct_gt50K: Optional[float] = None
    scaf_powsum: Optional[float] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contig_collection_id):
            self.MissingRequiredField("contig_collection_id")
        if not isinstance(self.contig_collection_id, ContigCollectionContigCollectionId):
            self.contig_collection_id = ContigCollectionContigCollectionId(self.contig_collection_id)

        if self.hash is not None and not isinstance(self.hash, str):
            self.hash = str(self.hash)

        if self.asm_score is not None and not isinstance(self.asm_score, float):
            self.asm_score = float(self.asm_score)

        if self.checkm2_completeness is not None and not isinstance(self.checkm2_completeness, float):
            self.checkm2_completeness = float(self.checkm2_completeness)

        if self.checkm2_contamination is not None and not isinstance(self.checkm2_contamination, float):
            self.checkm2_contamination = float(self.checkm2_contamination)

        if self.contig_bp is not None and not isinstance(self.contig_bp, int):
            self.contig_bp = int(self.contig_bp)

        if self.contig_collection_type is not None and not isinstance(
            self.contig_collection_type, ContigCollectionType
        ):
            self.contig_collection_type = ContigCollectionType(self.contig_collection_type)

        if self.ctg_L50 is not None and not isinstance(self.ctg_L50, int):
            self.ctg_L50 = int(self.ctg_L50)

        if self.ctg_L90 is not None and not isinstance(self.ctg_L90, int):
            self.ctg_L90 = int(self.ctg_L90)

        if self.ctg_N50 is not None and not isinstance(self.ctg_N50, int):
            self.ctg_N50 = int(self.ctg_N50)

        if self.ctg_N90 is not None and not isinstance(self.ctg_N90, int):
            self.ctg_N90 = int(self.ctg_N90)

        if self.ctg_logsum is not None and not isinstance(self.ctg_logsum, float):
            self.ctg_logsum = float(self.ctg_logsum)

        if self.ctg_max is not None and not isinstance(self.ctg_max, int):
            self.ctg_max = int(self.ctg_max)

        if self.ctg_powsum is not None and not isinstance(self.ctg_powsum, float):
            self.ctg_powsum = float(self.ctg_powsum)

        if self.gap_pct is not None and not isinstance(self.gap_pct, float):
            self.gap_pct = float(self.gap_pct)

        if self.gc_avg is not None and not isinstance(self.gc_avg, float):
            self.gc_avg = float(self.gc_avg)

        if self.gc_std is not None and not isinstance(self.gc_std, float):
            self.gc_std = float(self.gc_std)

        if self.n_contigs is not None and not isinstance(self.n_contigs, int):
            self.n_contigs = int(self.n_contigs)

        if self.n_scaffolds is not None and not isinstance(self.n_scaffolds, int):
            self.n_scaffolds = int(self.n_scaffolds)

        if self.scaf_L50 is not None and not isinstance(self.scaf_L50, int):
            self.scaf_L50 = int(self.scaf_L50)

        if self.scaf_L90 is not None and not isinstance(self.scaf_L90, int):
            self.scaf_L90 = int(self.scaf_L90)

        if self.scaf_N50 is not None and not isinstance(self.scaf_N50, int):
            self.scaf_N50 = int(self.scaf_N50)

        if self.scaf_N90 is not None and not isinstance(self.scaf_N90, int):
            self.scaf_N90 = int(self.scaf_N90)

        if self.scaf_bp is not None and not isinstance(self.scaf_bp, int):
            self.scaf_bp = int(self.scaf_bp)

        if self.scaf_l_gt50k is not None and not isinstance(self.scaf_l_gt50k, int):
            self.scaf_l_gt50k = int(self.scaf_l_gt50k)

        if self.scaf_logsum is not None and not isinstance(self.scaf_logsum, float):
            self.scaf_logsum = float(self.scaf_logsum)

        if self.scaf_max is not None and not isinstance(self.scaf_max, int):
            self.scaf_max = int(self.scaf_max)

        if self.scaf_n_gt50K is not None and not isinstance(self.scaf_n_gt50K, int):
            self.scaf_n_gt50K = int(self.scaf_n_gt50K)

        if self.scaf_pct_gt50K is not None and not isinstance(self.scaf_pct_gt50K, float):
            self.scaf_pct_gt50K = float(self.scaf_pct_gt50K)

        if self.scaf_powsum is not None and not isinstance(self.scaf_powsum, float):
            self.scaf_powsum = float(self.scaf_powsum)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Contributor(Table):
    """
    Represents a contributor to the resource.

    Contributors must have a 'contributor_type', either 'Person' or 'Organization', and
    one of the 'name' fields: either 'given_name' and 'family_name' (for a person), or 'name' (for an organization or
    a person).

    The 'contributor_role' field takes values from the DataCite and CRediT contributor
    roles vocabularies. For more information on these resources and choosing
    appropriate roles, please see the following links:

    DataCite contributor roles:
    https://support.datacite.org/docs/datacite-metadata-schema-v44-recommended-and-optional-properties#7a-contributortype

    CRediT contributor role taxonomy: https://credit.niso.org
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Contributor"]
    class_class_curie: ClassVar[str] = "kb_cdm:Contributor"
    class_name: ClassVar[str] = "Contributor"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Contributor

    contributor_id: Union[str, ContributorContributorId] = None
    contributor_type: Optional[Union[str, "ContributorType"]] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.contributor_id):
            self.MissingRequiredField("contributor_id")
        if not isinstance(self.contributor_id, ContributorContributorId):
            self.contributor_id = ContributorContributorId(self.contributor_id)

        if self.contributor_type is not None and not isinstance(self.contributor_type, ContributorType):
            self.contributor_type = ContributorType(self.contributor_type)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.given_name is not None and not isinstance(self.given_name, str):
            self.given_name = str(self.given_name)

        if self.family_name is not None and not isinstance(self.family_name, str):
            self.family_name = str(self.family_name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class DataSource(Table):
    """
    The source dataset from which data within the CDM was extracted. This might be an API query; a set of files
    downloaded from a website or uploaded by a user; a database dump; etc. A given data source should have either
    version information (e.g. UniProt's release number) or an access date to allow the original raw data dump to be
    recapitulated.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["DataSource"]
    class_class_curie: ClassVar[str] = "kb_cdm:DataSource"
    class_name: ClassVar[str] = "DataSource"
    class_model_uri: ClassVar[URIRef] = KB_CDM.DataSource

    data_source_id: Union[str, DataSourceDataSourceId] = None
    name: Optional[str] = None
    comments: Optional[str] = None
    date_accessed: Optional[str] = None
    url: Optional[Union[str, URI]] = None
    version: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.data_source_id):
            self.MissingRequiredField("data_source_id")
        if not isinstance(self.data_source_id, DataSourceDataSourceId):
            self.data_source_id = DataSourceDataSourceId(self.data_source_id)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.comments is not None and not isinstance(self.comments, str):
            self.comments = str(self.comments)

        if self.date_accessed is not None and not isinstance(self.date_accessed, str):
            self.date_accessed = str(self.date_accessed)

        if self.url is not None and not isinstance(self.url, URI):
            self.url = URI(self.url)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EncodedFeature(Table):
    """
    An entity generated from a feature, such as a transcript.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["EncodedFeature"]
    class_class_curie: ClassVar[str] = "kb_cdm:EncodedFeature"
    class_name: ClassVar[str] = "EncodedFeature"
    class_model_uri: ClassVar[URIRef] = KB_CDM.EncodedFeature

    encoded_feature_id: Union[str, EncodedFeatureEncodedFeatureId] = None
    hash: Optional[str] = None
    has_stop_codon: Optional[Union[bool, Bool]] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.encoded_feature_id):
            self.MissingRequiredField("encoded_feature_id")
        if not isinstance(self.encoded_feature_id, EncodedFeatureEncodedFeatureId):
            self.encoded_feature_id = EncodedFeatureEncodedFeatureId(self.encoded_feature_id)

        if self.hash is not None and not isinstance(self.hash, str):
            self.hash = str(self.hash)

        if self.has_stop_codon is not None and not isinstance(self.has_stop_codon, Bool):
            self.has_stop_codon = Bool(self.has_stop_codon)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class GoldEnvironmentalContext(Table):
    """
    Environmental context, described using JGI's five level system.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["GoldEnvironmentalContext"]
    class_class_curie: ClassVar[str] = "kb_cdm:GoldEnvironmentalContext"
    class_name: ClassVar[str] = "GoldEnvironmentalContext"
    class_model_uri: ClassVar[URIRef] = KB_CDM.GoldEnvironmentalContext

    gold_environmental_context_id: Union[str, GoldEnvironmentalContextGoldEnvironmentalContextId] = None
    ecosystem: Optional[str] = None
    ecosystem_category: Optional[str] = None
    ecosystem_subtype: Optional[str] = None
    ecosystem_type: Optional[str] = None
    specific_ecosystem: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.gold_environmental_context_id):
            self.MissingRequiredField("gold_environmental_context_id")
        if not isinstance(self.gold_environmental_context_id, GoldEnvironmentalContextGoldEnvironmentalContextId):
            self.gold_environmental_context_id = GoldEnvironmentalContextGoldEnvironmentalContextId(
                self.gold_environmental_context_id
            )

        if self.ecosystem is not None and not isinstance(self.ecosystem, str):
            self.ecosystem = str(self.ecosystem)

        if self.ecosystem_category is not None and not isinstance(self.ecosystem_category, str):
            self.ecosystem_category = str(self.ecosystem_category)

        if self.ecosystem_subtype is not None and not isinstance(self.ecosystem_subtype, str):
            self.ecosystem_subtype = str(self.ecosystem_subtype)

        if self.ecosystem_type is not None and not isinstance(self.ecosystem_type, str):
            self.ecosystem_type = str(self.ecosystem_type)

        if self.specific_ecosystem is not None and not isinstance(self.specific_ecosystem, str):
            self.specific_ecosystem = str(self.specific_ecosystem)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class MixsEnvironmentalContext(Table):
    """
    Environmental context, described using the MiXS convention of broad and local environment, plus the medium.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["MixsEnvironmentalContext"]
    class_class_curie: ClassVar[str] = "kb_cdm:MixsEnvironmentalContext"
    class_name: ClassVar[str] = "MixsEnvironmentalContext"
    class_model_uri: ClassVar[URIRef] = KB_CDM.MixsEnvironmentalContext

    mixs_environmental_context_id: Union[str, MixsEnvironmentalContextMixsEnvironmentalContextId] = None
    env_broad_scale: Optional[Union[str, URIorCURIE]] = None
    env_local_scale: Optional[Union[str, URIorCURIE]] = None
    env_medium: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.mixs_environmental_context_id):
            self.MissingRequiredField("mixs_environmental_context_id")
        if not isinstance(self.mixs_environmental_context_id, MixsEnvironmentalContextMixsEnvironmentalContextId):
            self.mixs_environmental_context_id = MixsEnvironmentalContextMixsEnvironmentalContextId(
                self.mixs_environmental_context_id
            )

        if self.env_broad_scale is not None and not isinstance(self.env_broad_scale, URIorCURIE):
            self.env_broad_scale = URIorCURIE(self.env_broad_scale)

        if self.env_local_scale is not None and not isinstance(self.env_local_scale, URIorCURIE):
            self.env_local_scale = URIorCURIE(self.env_local_scale)

        if self.env_medium is not None and not isinstance(self.env_medium, URIorCURIE):
            self.env_medium = URIorCURIE(self.env_medium)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Event(Table):
    """
    Something that happened.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Event"]
    class_class_curie: ClassVar[str] = "kb_cdm:Event"
    class_name: ClassVar[str] = "Event"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Event

    event_id: Union[str, EventEventId] = None
    created_at: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.event_id):
            self.MissingRequiredField("event_id")
        if not isinstance(self.event_id, EventEventId):
            self.event_id = EventEventId(self.event_id)

        if self.created_at is not None and not isinstance(self.created_at, str):
            self.created_at = str(self.created_at)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.location is not None and not isinstance(self.location, str):
            self.location = str(self.location)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Experiment(Table):
    """
    A discrete scientific procedure undertaken to make a discovery, test a hypothesis, or demonstrate a known fact.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Experiment"]
    class_class_curie: ClassVar[str] = "kb_cdm:Experiment"
    class_name: ClassVar[str] = "Experiment"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Experiment

    experiment_id: Union[str, ExperimentExperimentId] = None
    created_at: Optional[str] = None
    description: Optional[str] = None
    name: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.experiment_id):
            self.MissingRequiredField("experiment_id")
        if not isinstance(self.experiment_id, ExperimentExperimentId):
            self.experiment_id = ExperimentExperimentId(self.experiment_id)

        if self.created_at is not None and not isinstance(self.created_at, str):
            self.created_at = str(self.created_at)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Feature(Table):
    """
    A feature localized to an interval along a contig.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Feature"]
    class_class_curie: ClassVar[str] = "kb_cdm:Feature"
    class_name: ClassVar[str] = "Feature"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Feature

    feature_id: Union[str, FeatureFeatureId] = None
    hash: Optional[str] = None
    cds_phase: Optional[Union[str, "CdsPhaseType"]] = None
    e_value: Optional[float] = None
    end: Optional[int] = None
    p_value: Optional[float] = None
    start: Optional[int] = None
    strand: Optional[Union[str, "StrandType"]] = None
    source_database: Optional[Union[str, URIorCURIE]] = None
    protocol_id: Optional[Union[str, ProtocolProtocolId]] = None
    type: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.feature_id):
            self.MissingRequiredField("feature_id")
        if not isinstance(self.feature_id, FeatureFeatureId):
            self.feature_id = FeatureFeatureId(self.feature_id)

        if self.hash is not None and not isinstance(self.hash, str):
            self.hash = str(self.hash)

        if self.cds_phase is not None and not isinstance(self.cds_phase, CdsPhaseType):
            self.cds_phase = CdsPhaseType(self.cds_phase)

        if self.e_value is not None and not isinstance(self.e_value, float):
            self.e_value = float(self.e_value)

        if self.end is not None and not isinstance(self.end, int):
            self.end = int(self.end)

        if self.p_value is not None and not isinstance(self.p_value, float):
            self.p_value = float(self.p_value)

        if self.start is not None and not isinstance(self.start, int):
            self.start = int(self.start)

        if self.strand is not None and not isinstance(self.strand, StrandType):
            self.strand = StrandType(self.strand)

        if self.source_database is not None and not isinstance(self.source_database, URIorCURIE):
            self.source_database = URIorCURIE(self.source_database)

        if self.protocol_id is not None and not isinstance(self.protocol_id, ProtocolProtocolId):
            self.protocol_id = ProtocolProtocolId(self.protocol_id)

        if self.type is not None and not isinstance(self.type, URIorCURIE):
            self.type = URIorCURIE(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Project(Table):
    """
    Administrative unit for collecting data related to a certain topic, location, data type, grant funding, and so on.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Project"]
    class_class_curie: ClassVar[str] = "kb_cdm:Project"
    class_name: ClassVar[str] = "Project"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Project

    project_id: Union[str, ProjectProjectId] = None
    description: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.project_id):
            self.MissingRequiredField("project_id")
        if not isinstance(self.project_id, ProjectProjectId):
            self.project_id = ProjectProjectId(self.project_id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Protein(Table):
    """
    Proteins are large, complex molecules made up of one or more long, folded chains of amino acids, whose sequences
    are determined by the DNA sequence of the protein-encoding gene.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Protein"]
    class_class_curie: ClassVar[str] = "kb_cdm:Protein"
    class_name: ClassVar[str] = "Protein"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Protein

    protein_id: Union[str, ProteinProteinId] = None
    hash: Optional[str] = None
    description: Optional[str] = None
    evidence_for_existence: Optional[Union[str, "ProteinEvidenceForExistence"]] = None
    length: Optional[int] = None
    sequence: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.protein_id):
            self.MissingRequiredField("protein_id")
        if not isinstance(self.protein_id, ProteinProteinId):
            self.protein_id = ProteinProteinId(self.protein_id)

        if self.hash is not None and not isinstance(self.hash, str):
            self.hash = str(self.hash)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.evidence_for_existence is not None and not isinstance(
            self.evidence_for_existence, ProteinEvidenceForExistence
        ):
            self.evidence_for_existence = ProteinEvidenceForExistence(self.evidence_for_existence)

        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.sequence is not None and not isinstance(self.sequence, str):
            self.sequence = str(self.sequence)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Protocol(Table):
    """
    Defined method or set of methods.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Protocol"]
    class_class_curie: ClassVar[str] = "kb_cdm:Protocol"
    class_name: ClassVar[str] = "Protocol"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Protocol

    protocol_id: Union[str, ProtocolProtocolId] = None
    doi: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    url: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.protocol_id):
            self.MissingRequiredField("protocol_id")
        if not isinstance(self.protocol_id, ProtocolProtocolId):
            self.protocol_id = ProtocolProtocolId(self.protocol_id)

        if self.doi is not None and not isinstance(self.doi, str):
            self.doi = str(self.doi)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.version is not None and not isinstance(self.version, str):
            self.version = str(self.version)

        if self.url is not None and not isinstance(self.url, str):
            self.url = str(self.url)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProtocolParticipant(Table):
    """
    Either an input or an output of a protocol.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ProtocolParticipant"]
    class_class_curie: ClassVar[str] = "kb_cdm:ProtocolParticipant"
    class_name: ClassVar[str] = "ProtocolParticipant"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ProtocolParticipant

    protocol_participant_id: Union[str, ProtocolParticipantProtocolParticipantId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.protocol_participant_id):
            self.MissingRequiredField("protocol_participant_id")
        if not isinstance(self.protocol_participant_id, ProtocolParticipantProtocolParticipantId):
            self.protocol_participant_id = ProtocolParticipantProtocolParticipantId(self.protocol_participant_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Publication(Table):
    """
    A publication (e.g. journal article).
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Publication"]
    class_class_curie: ClassVar[str] = "kb_cdm:Publication"
    class_name: ClassVar[str] = "Publication"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Publication

    publication_id: Union[str, PublicationPublicationId] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.publication_id):
            self.MissingRequiredField("publication_id")
        if not isinstance(self.publication_id, PublicationPublicationId):
            self.publication_id = PublicationPublicationId(self.publication_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Sample(Table):
    """
    A material entity that can be characterised by an experiment.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Sample"]
    class_class_curie: ClassVar[str] = "kb_cdm:Sample"
    class_name: ClassVar[str] = "Sample"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Sample

    sample_id: Union[str, SampleSampleId] = None
    description: Optional[str] = None
    type: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sample_id):
            self.MissingRequiredField("sample_id")
        if not isinstance(self.sample_id, SampleSampleId):
            self.sample_id = SampleSampleId(self.sample_id)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.type is not None and not isinstance(self.type, str):
            self.type = str(self.type)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Sequence(Table):
    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Sequence"]
    class_class_curie: ClassVar[str] = "kb_cdm:Sequence"
    class_name: ClassVar[str] = "Sequence"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Sequence

    sequence_id: Union[str, UUID] = None
    entity_id: Union[str, UUID] = None
    type: Optional[Union[str, "SequenceType"]] = None
    length: Optional[int] = None
    checksum: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.sequence_id):
            self.MissingRequiredField("sequence_id")
        if not isinstance(self.sequence_id, UUID):
            self.sequence_id = UUID(self.sequence_id)

        if self._is_empty(self.entity_id):
            self.MissingRequiredField("entity_id")
        if not isinstance(self.entity_id, UUID):
            self.entity_id = UUID(self.entity_id)

        if self.type is not None and not isinstance(self.type, SequenceType):
            self.type = SequenceType(self.type)

        if self.length is not None and not isinstance(self.length, int):
            self.length = int(self.length)

        if self.checksum is not None and not isinstance(self.checksum, str):
            self.checksum = str(self.checksum)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class AttributeValue(Table):
    """
    A generic class for capturing tag-value information in a structured form.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["AttributeValue"]
    class_class_curie: ClassVar[str] = "kb_cdm:AttributeValue"
    class_name: ClassVar[str] = "AttributeValue"
    class_model_uri: ClassVar[URIRef] = KB_CDM.AttributeValue

    entity_id: Union[str, UUID] = None
    attribute_name: str = None
    attribute_cv_term_id: Optional[Union[str, LocalCurie]] = None
    raw_value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.entity_id):
            self.MissingRequiredField("entity_id")
        if not isinstance(self.entity_id, UUID):
            self.entity_id = UUID(self.entity_id)

        if self._is_empty(self.attribute_name):
            self.MissingRequiredField("attribute_name")
        if not isinstance(self.attribute_name, str):
            self.attribute_name = str(self.attribute_name)

        if self.attribute_cv_term_id is not None and not isinstance(self.attribute_cv_term_id, LocalCurie):
            self.attribute_cv_term_id = LocalCurie(self.attribute_cv_term_id)

        if self.raw_value is not None and not isinstance(self.raw_value, str):
            self.raw_value = str(self.raw_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Geolocation(AttributeValue):
    """
    A normalized value for a location on the earth's surface
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = NMDC["GeolocationValue"]
    class_class_curie: ClassVar[str] = "nmdc:GeolocationValue"
    class_name: ClassVar[str] = "Geolocation"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Geolocation

    entity_id: Union[str, UUID] = None
    attribute_name: str = None
    latitude: str = None
    longitude: str = None
    raw_value: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.latitude):
            self.MissingRequiredField("latitude")
        if not isinstance(self.latitude, str):
            self.latitude = str(self.latitude)

        if self._is_empty(self.longitude):
            self.MissingRequiredField("longitude")
        if not isinstance(self.longitude, str):
            self.longitude = str(self.longitude)

        if self.raw_value is not None and not isinstance(self.raw_value, str):
            self.raw_value = str(self.raw_value)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class QuantityValue(AttributeValue):
    """
    A simple quantity, e.g. 2cm. May be used to describe a range using the minimum_value and maximum_value fields.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["QuantityValue"]
    class_class_curie: ClassVar[str] = "schema:QuantityValue"
    class_name: ClassVar[str] = "QuantityValue"
    class_model_uri: ClassVar[URIRef] = KB_CDM.QuantityValue

    entity_id: Union[str, UUID] = None
    attribute_name: str = None
    maximum_value: Optional[float] = None
    minimum_value: Optional[float] = None
    value: Optional[float] = None
    unit: Optional[Union[str, Curie]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.maximum_value is not None and not isinstance(self.maximum_value, float):
            self.maximum_value = float(self.maximum_value)

        if self.minimum_value is not None and not isinstance(self.minimum_value, float):
            self.minimum_value = float(self.minimum_value)

        if self.value is not None and not isinstance(self.value, float):
            self.value = float(self.value)

        if self.unit is not None and not isinstance(self.unit, Curie):
            self.unit = Curie(self.unit)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class TextValue(AttributeValue):
    """
    A basic string value
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["TextValue"]
    class_class_curie: ClassVar[str] = "kb_cdm:TextValue"
    class_name: ClassVar[str] = "TextValue"
    class_model_uri: ClassVar[URIRef] = KB_CDM.TextValue

    entity_id: Union[str, UUID] = None
    attribute_name: str = None
    value: str = None
    value_cv_term_id: Optional[Union[str, LocalCurie]] = None
    language: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.value):
            self.MissingRequiredField("value")
        if not isinstance(self.value, str):
            self.value = str(self.value)

        if self.value_cv_term_id is not None and not isinstance(self.value_cv_term_id, LocalCurie):
            self.value_cv_term_id = LocalCurie(self.value_cv_term_id)

        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Measurement(QuantityValue):
    """
    A qualitative or quantitative observation of an attribute of an object or event against a standardized scale, to
    enable it to be compared with other objects or events.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Measurement"]
    class_class_curie: ClassVar[str] = "kb_cdm:Measurement"
    class_name: ClassVar[str] = "Measurement"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Measurement

    measurement_id: Union[str, MeasurementMeasurementId] = None
    entity_id: Union[str, UUID] = None
    attribute_name: str = None
    protocol_id: Union[str, UUID] = None
    created_at: Optional[str] = None
    quality: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.measurement_id):
            self.MissingRequiredField("measurement_id")
        if not isinstance(self.measurement_id, MeasurementMeasurementId):
            self.measurement_id = MeasurementMeasurementId(self.measurement_id)

        if self._is_empty(self.protocol_id):
            self.MissingRequiredField("protocol_id")
        if not isinstance(self.protocol_id, UUID):
            self.protocol_id = UUID(self.protocol_id)

        if self.created_at is not None and not isinstance(self.created_at, str):
            self.created_at = str(self.created_at)

        if self.quality is not None and not isinstance(self.quality, str):
            self.quality = str(self.quality)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class ProcessedMeasurement(Measurement):
    """
    A measurement that requires additional processing to generate a result.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["ProcessedMeasurement"]
    class_class_curie: ClassVar[str] = "kb_cdm:ProcessedMeasurement"
    class_name: ClassVar[str] = "ProcessedMeasurement"
    class_model_uri: ClassVar[URIRef] = KB_CDM.ProcessedMeasurement

    measurement_id: Union[str, ProcessedMeasurementMeasurementId] = None
    entity_id: Union[str, UUID] = None
    attribute_name: str = None
    protocol_id: Union[str, UUID] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.measurement_id):
            self.MissingRequiredField("measurement_id")
        if not isinstance(self.measurement_id, ProcessedMeasurementMeasurementId):
            self.measurement_id = ProcessedMeasurementMeasurementId(self.measurement_id)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Entity(Table):
    """
    A database entity.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Entity"]
    class_class_curie: ClassVar[str] = "kb_cdm:Entity"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Entity

    entity_id: Union[str, EntityEntityId] = None
    data_source_id: Union[str, UUID] = None
    entity_type: Union[str, "EntityType"] = None
    data_source_created: str = None
    created: str = None
    updated: str = None
    data_source_entity_id: Optional[Union[str, URIorCURIE]] = None
    data_source_updated: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.entity_id):
            self.MissingRequiredField("entity_id")
        if not isinstance(self.entity_id, EntityEntityId):
            self.entity_id = EntityEntityId(self.entity_id)

        if self._is_empty(self.data_source_id):
            self.MissingRequiredField("data_source_id")
        if not isinstance(self.data_source_id, UUID):
            self.data_source_id = UUID(self.data_source_id)

        if self._is_empty(self.entity_type):
            self.MissingRequiredField("entity_type")
        if not isinstance(self.entity_type, EntityType):
            self.entity_type = EntityType(self.entity_type)

        if self._is_empty(self.data_source_created):
            self.MissingRequiredField("data_source_created")
        if not isinstance(self.data_source_created, str):
            self.data_source_created = str(self.data_source_created)

        if self._is_empty(self.created):
            self.MissingRequiredField("created")
        if not isinstance(self.created, str):
            self.created = str(self.created)

        if self._is_empty(self.updated):
            self.MissingRequiredField("updated")
        if not isinstance(self.updated, str):
            self.updated = str(self.updated)

        if self.data_source_entity_id is not None and not isinstance(self.data_source_entity_id, URIorCURIE):
            self.data_source_entity_id = URIorCURIE(self.data_source_entity_id)

        if self.data_source_updated is not None and not isinstance(self.data_source_updated, str):
            self.data_source_updated = str(self.data_source_updated)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Identifier(Table):
    """
    A string used as a resolvable (external) identifier for an entity. This should be a URI or CURIE. If the string
    cannot be resolved to an URL, it should be added as a 'name' instead.

    This table is used for capturing external IDs. The internal CDM identifier should be used in the *_id field (e.g.
    feature_id, protein_id, contig_collection_id).
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Identifier"]
    class_class_curie: ClassVar[str] = "kb_cdm:Identifier"
    class_name: ClassVar[str] = "Identifier"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Identifier

    entity_id: Union[str, UUID] = None
    identifier: Union[str, URIorCURIE] = None
    description: Optional[str] = None
    source: Optional[Union[str, DataSourceUuid]] = None
    relationship: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.entity_id):
            self.MissingRequiredField("entity_id")
        if not isinstance(self.entity_id, UUID):
            self.entity_id = UUID(self.entity_id)

        if self._is_empty(self.identifier):
            self.MissingRequiredField("identifier")
        if not isinstance(self.identifier, URIorCURIE):
            self.identifier = URIorCURIE(self.identifier)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.source is not None and not isinstance(self.source, DataSourceUuid):
            self.source = DataSourceUuid(self.source)

        if self.relationship is not None and not isinstance(self.relationship, str):
            self.relationship = str(self.relationship)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Name(Table):
    """
    A string used as the name or label for an entity. This may be a primary name, alternative name, synonym, acronym,
    or any other label used to refer to an entity.

    Identifiers that look like CURIEs or database references, but which cannot be resolved using bioregistry or
    identifiers.org should be added as names.
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["Name"]
    class_class_curie: ClassVar[str] = "kb_cdm:Name"
    class_name: ClassVar[str] = "Name"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Name

    entity_id: Union[str, UUID] = None
    name: str = None
    description: Optional[str] = None
    source: Optional[Union[str, DataSourceUuid]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self._is_empty(self.entity_id):
            self.MissingRequiredField("entity_id")
        if not isinstance(self.entity_id, UUID):
            self.entity_id = UUID(self.entity_id)

        if self._is_empty(self.name):
            self.MissingRequiredField("name")
        if not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.source is not None and not isinstance(self.source, DataSourceUuid):
            self.source = DataSourceUuid(self.source)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Prefix(Table):
    """
    Maps CURIEs to URIs
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = SH["PrefixDeclaration"]
    class_class_curie: ClassVar[str] = "sh:PrefixDeclaration"
    class_name: ClassVar[str] = "Prefix"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Prefix

    prefix: Optional[Union[str, NCName]] = None
    base: Optional[Union[str, URI]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.prefix is not None and not isinstance(self.prefix, NCName):
            self.prefix = NCName(self.prefix)

        if self.base is not None and not isinstance(self.base, URI):
            self.base = URI(self.base)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class Statements(Table):
    """
    Represents an RDF triple
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = RDF["Statement"]
    class_class_curie: ClassVar[str] = "rdf:Statement"
    class_name: ClassVar[str] = "Statements"
    class_model_uri: ClassVar[URIRef] = KB_CDM.Statements

    subject: Optional[Union[str, URIorCURIE]] = None
    predicate: Optional[Union[str, URIorCURIE]] = None
    object: Optional[Union[str, URIorCURIE]] = None
    value: Optional[Union[str, LiteralAsStringType]] = None
    datatype: Optional[str] = None
    language: Optional[str] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.subject is not None and not isinstance(self.subject, URIorCURIE):
            self.subject = URIorCURIE(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, URIorCURIE):
            self.predicate = URIorCURIE(self.predicate)

        if self.object is not None and not isinstance(self.object, URIorCURIE):
            self.object = URIorCURIE(self.object)

        if self.value is not None and not isinstance(self.value, LiteralAsStringType):
            self.value = LiteralAsStringType(self.value)

        if self.datatype is not None and not isinstance(self.datatype, str):
            self.datatype = str(self.datatype)

        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        super().__post_init__(**kwargs)


@dataclass(repr=False)
class EntailedEdge(Table):
    """
    A relation graph edge that is inferred
    """

    _inherited_slots: ClassVar[list[str]] = []

    class_class_uri: ClassVar[URIRef] = KB_CDM["EntailedEdge"]
    class_class_curie: ClassVar[str] = "kb_cdm:EntailedEdge"
    class_name: ClassVar[str] = "EntailedEdge"
    class_model_uri: ClassVar[URIRef] = KB_CDM.EntailedEdge

    subject: Optional[Union[str, URIorCURIE]] = None
    predicate: Optional[Union[str, URIorCURIE]] = None
    object: Optional[Union[str, URIorCURIE]] = None

    def __post_init__(self, *_: str, **kwargs: Any):
        if self.subject is not None and not isinstance(self.subject, URIorCURIE):
            self.subject = URIorCURIE(self.subject)

        if self.predicate is not None and not isinstance(self.predicate, URIorCURIE):
            self.predicate = URIorCURIE(self.predicate)

        if self.object is not None and not isinstance(self.object, URIorCURIE):
            self.object = URIorCURIE(self.object)

        super().__post_init__(**kwargs)


# Enumerations
class CdsPhaseType(EnumDefinitionImpl):
    """
    For features of type CDS (coding sequence), the phase indicates where the feature begins with reference to the
    reading frame. The phase is one of the integers 0, 1, or 2, indicating the number of bases that should be removed
    from the beginning of this feature to reach the first base of the next codon.
    """

    _defn = EnumDefinition(
        name="CdsPhaseType",
        description="""For features of type CDS (coding sequence), the phase indicates where the feature begins with reference to the reading frame. The phase is one of the integers 0, 1, or 2, indicating the number of bases that should be removed from the beginning of this feature to reach the first base of the next codon.""",
    )

    @classmethod
    def _addvals(cls):
        setattr(cls, "0", PermissibleValue(text="0", description="Zero bases from reading frame to feature start."))
        setattr(cls, "1", PermissibleValue(text="1", description="One base from reading frame to feature start."))
        setattr(cls, "2", PermissibleValue(text="2", description="Two bases from reading frame to feature start."))


class ClusterType(EnumDefinitionImpl):
    """
    The type of the entities in a cluster. Must be represented by a table in the CDM schema.
    """

    Protein = PermissibleValue(text="Protein", meaning=KB_CDM["Protein"])
    Feature = PermissibleValue(text="Feature", meaning=KB_CDM["Feature"])
    ContigCollection = PermissibleValue(text="ContigCollection", meaning=KB_CDM["ContigCollection"])

    _defn = EnumDefinition(
        name="ClusterType",
        description="The type of the entities in a cluster. Must be represented by a table in the CDM schema.",
    )


class ContigCollectionType(EnumDefinitionImpl):
    """
    The type of the contig set; the type of the 'omics data set. Terms are taken from the Genomics Standards
    Consortium where possible. See the GSC checklists at https://genomicsstandardsconsortium.github.io/mixs/ for the
    controlled vocabularies used.
    """

    isolate = PermissibleValue(
        text="isolate",
        description="""Sequences assembled from DNA of isolated organism.
Bacteria/Archaea: https://genomicsstandardsconsortium.github.io/mixs/0010003/
Euk: https://genomicsstandardsconsortium.github.io/mixs/0010002/
Virus: https://genomicsstandardsconsortium.github.io/mixs/0010005/
Organelle: https://genomicsstandardsconsortium.github.io/mixs/0010006/
Plasmid: https://genomicsstandardsconsortium.github.io/mixs/0010004/""",
    )
    mag = PermissibleValue(
        text="mag",
        description="""Sequences assembled from DNA of mixed community and binned. MAGs are likely to represent a single taxonomic origin. See checkm2 scores for quality assessment.
https://genomicsstandardsconsortium.github.io/mixs/0010011/""",
        meaning=MIXS["0010011"],
    )
    metagenome = PermissibleValue(
        text="metagenome",
        description="""Sequences assembled from DNA of mixed community.
https://genomicsstandardsconsortium.github.io/mixs/0010007/""",
        meaning=MIXS["0010007"],
    )
    metatranscriptome = PermissibleValue(
        text="metatranscriptome",
        description="""Sequences assembled from RNA of mixed community. Currently not represented by GSC.""",
    )
    sag = PermissibleValue(
        text="sag",
        description="""Sequences assembled from DNA of single cell.
https://genomicsstandardsconsortium.github.io/mixs/0010010/""",
        meaning=MIXS["0010010"],
    )
    virus = PermissibleValue(
        text="virus",
        description="""Sequences assembled from uncultivated virus genome (DNA/RNA).
https://genomicsstandardsconsortium.github.io/mixs/0010012/""",
        meaning=MIXS["0010012"],
    )
    marker = PermissibleValue(
        text="marker",
        description="""Sequences from targeted region of DNA; see protocol for information on targeted region.
specimen: https://genomicsstandardsconsortium.github.io/mixs/0010009/
survey: https://genomicsstandardsconsortium.github.io/mixs/0010008/""",
    )

    _defn = EnumDefinition(
        name="ContigCollectionType",
        description="""The type of the contig set; the type of the 'omics data set. Terms are taken from the Genomics Standards Consortium where possible. See the GSC checklists at  https://genomicsstandardsconsortium.github.io/mixs/ for the controlled vocabularies used.""",
    )


class ContributorRole(EnumDefinitionImpl):
    """
    The role of a contributor to a resource.
    """

    TODO = PermissibleValue(text="TODO")

    _defn = EnumDefinition(
        name="ContributorRole",
        description="The role of a contributor to a resource.",
    )


class ContributorType(EnumDefinitionImpl):
    """
    The type of contributor being represented.
    """

    Person = PermissibleValue(text="Person", description="A person.", meaning=SCHEMA["Person"])
    Organization = PermissibleValue(text="Organization", description="An organization.", meaning=SCHEMA["Organization"])

    _defn = EnumDefinition(
        name="ContributorType",
        description="The type of contributor being represented.",
    )


class EntityType(EnumDefinitionImpl):
    """
    The type of an entity. Must be represented by a table in the CDM schema.
    """

    Cluster = PermissibleValue(text="Cluster", meaning=KB_CDM["Cluster"])
    Contig = PermissibleValue(text="Contig", meaning=KB_CDM["Contig"])
    ContigCollection = PermissibleValue(text="ContigCollection", meaning=KB_CDM["ContigCollection"])
    EncodedFeature = PermissibleValue(
        text="EncodedFeature",
        description="The output of transcribing a sequence; includes mRNA, tRNA, etc.",
        meaning=KB_CDM["EncodedFeature"],
    )
    Feature = PermissibleValue(text="Feature", meaning=KB_CDM["Feature"])
    Protein = PermissibleValue(text="Protein", meaning=KB_CDM["Protein"])
    Sample = PermissibleValue(text="Sample", meaning=KB_CDM["Sample"])
    Organization = PermissibleValue(text="Organization", meaning=KB_CDM["Organization"])
    Contributor = PermissibleValue(text="Contributor", meaning=KB_CDM["Contributor"])
    Project = PermissibleValue(text="Project", meaning=KB_CDM["Project"])
    Experiment = PermissibleValue(text="Experiment", meaning=KB_CDM["Experiment"])

    _defn = EnumDefinition(
        name="EntityType",
        description="The type of an entity. Must be represented by a table in the CDM schema.",
    )


class ProteinEvidenceForExistence(EnumDefinitionImpl):
    """
    The evidence for the existence of a biological entity. See https://www.uniprot.org/help/protein_existence and
    https://www.ncbi.nlm.nih.gov/genbank/evidence/.
    """

    experimental_evidence_at_protein_level = PermissibleValue(
        text="experimental_evidence_at_protein_level",
        description="""Indicates that there is clear experimental evidence for the existence of the protein. The criteria include partial or complete Edman sequencing, clear identification by mass spectrometry, X-ray or NMR structure, good quality protein-protein interaction or detection of the protein by antibodies.""",
    )
    experimental_evidence_at_transcript_level = PermissibleValue(
        text="experimental_evidence_at_transcript_level",
        description="""Indicates that the existence of a protein has not been strictly proven but that expression data (such as existence of cDNA(s), RT-PCR or Northern blots) indicate the existence of a transcript.""",
    )
    protein_inferred_by_homology = PermissibleValue(
        text="protein_inferred_by_homology",
        description="""Indicates that the existence of a protein is probable because clear orthologs exist in closely related species.""",
    )
    protein_predicted = PermissibleValue(
        text="protein_predicted",
        description="Used for entries without evidence at protein, transcript, or homology levels.",
    )
    protein_uncertain = PermissibleValue(
        text="protein_uncertain", description="Indicates that the existence of the protein is unsure."
    )

    _defn = EnumDefinition(
        name="ProteinEvidenceForExistence",
        description="""The evidence for the existence of a biological entity. See https://www.uniprot.org/help/protein_existence and https://www.ncbi.nlm.nih.gov/genbank/evidence/.""",
    )


class RefSeqStatusType(EnumDefinitionImpl):
    """
    RefSeq status codes, taken from https://www.ncbi.nlm.nih.gov/genbank/evidence/.
    """

    MODEL = PermissibleValue(
        text="MODEL",
        description="""The RefSeq record is provided by the NCBI Genome Annotation pipeline and is not subject to individual review or revision between annotation runs.""",
    )
    INFERRED = PermissibleValue(
        text="INFERRED",
        description="""The RefSeq record has been predicted by genome sequence analysis, but it is not yet supported by experimental evidence. The record may be partially supported by homology data.""",
    )
    PREDICTED = PermissibleValue(
        text="PREDICTED",
        description="""The RefSeq record has not yet been subject to individual review, and some aspect of the RefSeq record is predicted.""",
    )
    PROVISIONAL = PermissibleValue(
        text="PROVISIONAL",
        description="""The RefSeq record has not yet been subject to individual review. The initial sequence-to-gene association has been established by outside collaborators or NCBI staff.""",
    )
    REVIEWED = PermissibleValue(
        text="REVIEWED",
        description="""The RefSeq record has been reviewed by NCBI staff or by a collaborator. The NCBI review process includes assessing available sequence data and the literature. Some RefSeq records may incorporate expanded sequence and annotation information.""",
    )
    VALIDATED = PermissibleValue(
        text="VALIDATED",
        description="""The RefSeq record has undergone an initial review to provide the preferred sequence standard. The record has not yet been subject to final review at which time additional functional information may be provided.""",
    )
    WGS = PermissibleValue(
        text="WGS",
        description="""The RefSeq record is provided to represent a collection of whole genome shotgun sequences. These records are not subject to individual review or revisions between genome updates.""",
    )

    _defn = EnumDefinition(
        name="RefSeqStatusType",
        description="""RefSeq status codes, taken from https://www.ncbi.nlm.nih.gov/genbank/evidence/.""",
    )


class SequenceType(EnumDefinitionImpl):
    """
    The type of sequence being represented.
    """

    NucleicAcid = PermissibleValue(text="NucleicAcid", description="A nucleic acid sequence, as found in an FNA file.")
    AminoAcid = PermissibleValue(
        text="AminoAcid", description="An amino acid sequence, as would be found in an FAA file."
    )

    _defn = EnumDefinition(
        name="SequenceType",
        description="The type of sequence being represented.",
    )


class StrandType(EnumDefinitionImpl):
    """
    The strand that a feature appears on relative to a landmark. Also encompasses unknown or irrelevant strandedness.
    """

    negative = PermissibleValue(
        text="negative", description='Represented by "-" in a GFF file; the strand is negative wrt the landmark.'
    )
    positive = PermissibleValue(
        text="positive",
        description='Represented by "+" in a GFF file; the strand is positive with relation to the landmark.',
    )
    unknown = PermissibleValue(
        text="unknown", description='Represented by "?" in a GFF file. The strandedness is relevant but unknown.'
    )
    unstranded = PermissibleValue(
        text="unstranded", description='Represented by "." in a GFF file; the feature is not stranded.'
    )

    _defn = EnumDefinition(
        name="StrandType",
        description="""The strand that a feature appears on relative to a landmark. Also encompasses unknown or irrelevant strandedness.""",
    )


# Slots
class slots:
    pass


slots.description = Slot(
    uri=KB_CDM.description,
    name="description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.description,
    domain=None,
    range=Optional[str],
)

slots.hash = Slot(
    uri=KB_CDM.hash, name="hash", curie=KB_CDM.curie("hash"), model_uri=KB_CDM.hash, domain=None, range=Optional[str]
)

slots.identifier = Slot(
    uri=SCHEMA.identifier,
    name="identifier",
    curie=SCHEMA.curie("identifier"),
    model_uri=KB_CDM.identifier,
    domain=None,
    range=Union[str, URIorCURIE],
)

slots.name = Slot(
    uri=SCHEMA.name, name="name", curie=SCHEMA.curie("name"), model_uri=KB_CDM.name, domain=None, range=Optional[str]
)

slots.source = Slot(
    uri=KB_CDM.source,
    name="source",
    curie=KB_CDM.curie("source"),
    model_uri=KB_CDM.source,
    domain=None,
    range=Optional[Union[str, DataSourceUuid]],
)

slots.association_id = Slot(
    uri=KB_CDM.association_id,
    name="association_id",
    curie=KB_CDM.curie("association_id"),
    model_uri=KB_CDM.association_id,
    domain=None,
    range=Union[str, UUID],
)

slots.cluster_id = Slot(
    uri=KB_CDM.cluster_id,
    name="cluster_id",
    curie=KB_CDM.curie("cluster_id"),
    model_uri=KB_CDM.cluster_id,
    domain=None,
    range=Union[str, UUID],
)

slots.contig_id = Slot(
    uri=KB_CDM.contig_id,
    name="contig_id",
    curie=KB_CDM.curie("contig_id"),
    model_uri=KB_CDM.contig_id,
    domain=None,
    range=Union[str, UUID],
)

slots.contig_collection_id = Slot(
    uri=KB_CDM.contig_collection_id,
    name="contig_collection_id",
    curie=KB_CDM.curie("contig_collection_id"),
    model_uri=KB_CDM.contig_collection_id,
    domain=None,
    range=Union[str, UUID],
)

slots.contributor_id = Slot(
    uri=KB_CDM.contributor_id,
    name="contributor_id",
    curie=KB_CDM.curie("contributor_id"),
    model_uri=KB_CDM.contributor_id,
    domain=None,
    range=Union[str, UUID],
)

slots.data_source_id = Slot(
    uri=KB_CDM.data_source_id,
    name="data_source_id",
    curie=KB_CDM.curie("data_source_id"),
    model_uri=KB_CDM.data_source_id,
    domain=None,
    range=Union[str, UUID],
)

slots.encoded_feature_id = Slot(
    uri=KB_CDM.encoded_feature_id,
    name="encoded_feature_id",
    curie=KB_CDM.curie("encoded_feature_id"),
    model_uri=KB_CDM.encoded_feature_id,
    domain=None,
    range=Union[str, UUID],
)

slots.entity_id = Slot(
    uri=KB_CDM.entity_id,
    name="entity_id",
    curie=KB_CDM.curie("entity_id"),
    model_uri=KB_CDM.entity_id,
    domain=None,
    range=Union[str, UUID],
)

slots.event_id = Slot(
    uri=KB_CDM.event_id,
    name="event_id",
    curie=KB_CDM.curie("event_id"),
    model_uri=KB_CDM.event_id,
    domain=None,
    range=Union[str, UUID],
)

slots.experiment_id = Slot(
    uri=KB_CDM.experiment_id,
    name="experiment_id",
    curie=KB_CDM.curie("experiment_id"),
    model_uri=KB_CDM.experiment_id,
    domain=None,
    range=Union[str, UUID],
)

slots.feature_id = Slot(
    uri=KB_CDM.feature_id,
    name="feature_id",
    curie=KB_CDM.curie("feature_id"),
    model_uri=KB_CDM.feature_id,
    domain=None,
    range=Union[str, UUID],
)

slots.gold_environmental_context_id = Slot(
    uri=KB_CDM.gold_environmental_context_id,
    name="gold_environmental_context_id",
    curie=KB_CDM.curie("gold_environmental_context_id"),
    model_uri=KB_CDM.gold_environmental_context_id,
    domain=None,
    range=Union[str, UUID],
)

slots.measurement_id = Slot(
    uri=KB_CDM.measurement_id,
    name="measurement_id",
    curie=KB_CDM.curie("measurement_id"),
    model_uri=KB_CDM.measurement_id,
    domain=None,
    range=Union[str, UUID],
)

slots.mixs_environmental_context_id = Slot(
    uri=KB_CDM.mixs_environmental_context_id,
    name="mixs_environmental_context_id",
    curie=KB_CDM.curie("mixs_environmental_context_id"),
    model_uri=KB_CDM.mixs_environmental_context_id,
    domain=None,
    range=Union[str, UUID],
)

slots.project_id = Slot(
    uri=KB_CDM.project_id,
    name="project_id",
    curie=KB_CDM.curie("project_id"),
    model_uri=KB_CDM.project_id,
    domain=None,
    range=Union[str, UUID],
)

slots.protein_id = Slot(
    uri=KB_CDM.protein_id,
    name="protein_id",
    curie=KB_CDM.curie("protein_id"),
    model_uri=KB_CDM.protein_id,
    domain=None,
    range=Union[str, UUID],
)

slots.protocol_id = Slot(
    uri=KB_CDM.protocol_id,
    name="protocol_id",
    curie=KB_CDM.curie("protocol_id"),
    model_uri=KB_CDM.protocol_id,
    domain=None,
    range=Union[str, UUID],
)

slots.publication_id = Slot(
    uri=KB_CDM.publication_id,
    name="publication_id",
    curie=KB_CDM.curie("publication_id"),
    model_uri=KB_CDM.publication_id,
    domain=None,
    range=Union[str, URIorCURIE],
)

slots.sample_id = Slot(
    uri=KB_CDM.sample_id,
    name="sample_id",
    curie=KB_CDM.curie("sample_id"),
    model_uri=KB_CDM.sample_id,
    domain=None,
    range=Union[str, UUID],
)

slots.sequence_id = Slot(
    uri=KB_CDM.sequence_id,
    name="sequence_id",
    curie=KB_CDM.curie("sequence_id"),
    model_uri=KB_CDM.sequence_id,
    domain=None,
    range=Union[str, UUID],
)

slots.contributor_role = Slot(
    uri=SCHEMA.Role,
    name="contributor_role",
    curie=SCHEMA.curie("Role"),
    model_uri=KB_CDM.contributor_role,
    domain=None,
    range=Optional[Union[str, "ContributorRole"]],
)

slots.id = Slot(uri=KB_CDM.id, name="id", curie=KB_CDM.curie("id"), model_uri=KB_CDM.id, domain=None, range=URIRef)

slots.prefix = Slot(
    uri=SH.prefix,
    name="prefix",
    curie=SH.curie("prefix"),
    model_uri=KB_CDM.prefix,
    domain=None,
    range=Optional[Union[str, NCName]],
)

slots.base = Slot(
    uri=SH.namespace,
    name="base",
    curie=SH.curie("namespace"),
    model_uri=KB_CDM.base,
    domain=None,
    range=Optional[Union[str, URI]],
)

slots.subject = Slot(
    uri=RDF.subject,
    name="subject",
    curie=RDF.curie("subject"),
    model_uri=KB_CDM.subject,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.predicate = Slot(
    uri=RDF.predicate,
    name="predicate",
    curie=RDF.curie("predicate"),
    model_uri=KB_CDM.predicate,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.object = Slot(
    uri=RDF.object,
    name="object",
    curie=RDF.curie("object"),
    model_uri=KB_CDM.object,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.value = Slot(
    uri=RDF.object,
    name="value",
    curie=RDF.curie("object"),
    model_uri=KB_CDM.value,
    domain=None,
    range=Optional[Union[str, LiteralAsStringType]],
)

slots.datatype = Slot(
    uri=KB_CDM.datatype,
    name="datatype",
    curie=KB_CDM.curie("datatype"),
    model_uri=KB_CDM.datatype,
    domain=None,
    range=Optional[str],
)

slots.language = Slot(
    uri=KB_CDM.language,
    name="language",
    curie=KB_CDM.curie("language"),
    model_uri=KB_CDM.language,
    domain=None,
    range=Optional[str],
)

slots.protocolXProtocolParticipant__protocol_participant_id = Slot(
    uri=KB_CDM.protocol_participant_id,
    name="protocolXProtocolParticipant__protocol_participant_id",
    curie=KB_CDM.curie("protocol_participant_id"),
    model_uri=KB_CDM.protocolXProtocolParticipant__protocol_participant_id,
    domain=None,
    range=Union[str, ProtocolParticipantProtocolParticipantId],
)

slots.protocolXProtocolParticipant__participant_type = Slot(
    uri=KB_CDM.participant_type,
    name="protocolXProtocolParticipant__participant_type",
    curie=KB_CDM.curie("participant_type"),
    model_uri=KB_CDM.protocolXProtocolParticipant__participant_type,
    domain=None,
    range=Optional[str],
)

slots.association__negated = Slot(
    uri=KB_CDM.negated,
    name="association__negated",
    curie=KB_CDM.curie("negated"),
    model_uri=KB_CDM.association__negated,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.association__evidence_type = Slot(
    uri=KB_CDM.evidence_type,
    name="association__evidence_type",
    curie=KB_CDM.curie("evidence_type"),
    model_uri=KB_CDM.association__evidence_type,
    domain=None,
    range=Optional[Union[str, LocalCurie]],
    pattern=re.compile(r"^ECO:\d+$"),
)

slots.association__primary_knowledge_source = Slot(
    uri=KB_CDM.primary_knowledge_source,
    name="association__primary_knowledge_source",
    curie=KB_CDM.curie("primary_knowledge_source"),
    model_uri=KB_CDM.association__primary_knowledge_source,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.association__aggregator_knowledge_source = Slot(
    uri=KB_CDM.aggregator_knowledge_source,
    name="association__aggregator_knowledge_source",
    curie=KB_CDM.curie("aggregator_knowledge_source"),
    model_uri=KB_CDM.association__aggregator_knowledge_source,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.association__annotation_date = Slot(
    uri=KB_CDM.annotation_date,
    name="association__annotation_date",
    curie=KB_CDM.curie("annotation_date"),
    model_uri=KB_CDM.association__annotation_date,
    domain=None,
    range=Optional[str],
)

slots.association__comments = Slot(
    uri=KB_CDM.comments,
    name="association__comments",
    curie=KB_CDM.curie("comments"),
    model_uri=KB_CDM.association__comments,
    domain=None,
    range=Optional[str],
)

slots.cluster__name = Slot(
    uri=KB_CDM.name,
    name="cluster__name",
    curie=KB_CDM.curie("name"),
    model_uri=KB_CDM.cluster__name,
    domain=None,
    range=Optional[str],
)

slots.cluster__entity_type = Slot(
    uri=KB_CDM.entity_type,
    name="cluster__entity_type",
    curie=KB_CDM.curie("entity_type"),
    model_uri=KB_CDM.cluster__entity_type,
    domain=None,
    range=Union[str, "ClusterType"],
)

slots.cluster__protocol_id = Slot(
    uri=KB_CDM.protocol_id,
    name="cluster__protocol_id",
    curie=KB_CDM.curie("protocol_id"),
    model_uri=KB_CDM.cluster__protocol_id,
    domain=None,
    range=Optional[str],
)

slots.clusterMember__is_representative = Slot(
    uri=KB_CDM.is_representative,
    name="clusterMember__is_representative",
    curie=KB_CDM.curie("is_representative"),
    model_uri=KB_CDM.clusterMember__is_representative,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.clusterMember__is_seed = Slot(
    uri=KB_CDM.is_seed,
    name="clusterMember__is_seed",
    curie=KB_CDM.curie("is_seed"),
    model_uri=KB_CDM.clusterMember__is_seed,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.clusterMember__score = Slot(
    uri=KB_CDM.score,
    name="clusterMember__score",
    curie=KB_CDM.curie("score"),
    model_uri=KB_CDM.clusterMember__score,
    domain=None,
    range=Optional[float],
)

slots.contig__gc_content = Slot(
    uri=KB_CDM.gc_content,
    name="contig__gc_content",
    curie=KB_CDM.curie("gc_content"),
    model_uri=KB_CDM.contig__gc_content,
    domain=None,
    range=Optional[float],
)

slots.contig__length = Slot(
    uri=KB_CDM.length,
    name="contig__length",
    curie=KB_CDM.curie("length"),
    model_uri=KB_CDM.contig__length,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__asm_score = Slot(
    uri=KB_CDM.asm_score,
    name="contigCollection__asm_score",
    curie=KB_CDM.curie("asm_score"),
    model_uri=KB_CDM.contigCollection__asm_score,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__checkm2_completeness = Slot(
    uri=KB_CDM.checkm2_completeness,
    name="contigCollection__checkm2_completeness",
    curie=KB_CDM.curie("checkm2_completeness"),
    model_uri=KB_CDM.contigCollection__checkm2_completeness,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__checkm2_contamination = Slot(
    uri=KB_CDM.checkm2_contamination,
    name="contigCollection__checkm2_contamination",
    curie=KB_CDM.curie("checkm2_contamination"),
    model_uri=KB_CDM.contigCollection__checkm2_contamination,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__contig_bp = Slot(
    uri=KB_CDM.contig_bp,
    name="contigCollection__contig_bp",
    curie=KB_CDM.curie("contig_bp"),
    model_uri=KB_CDM.contigCollection__contig_bp,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__contig_collection_type = Slot(
    uri=KB_CDM.contig_collection_type,
    name="contigCollection__contig_collection_type",
    curie=KB_CDM.curie("contig_collection_type"),
    model_uri=KB_CDM.contigCollection__contig_collection_type,
    domain=None,
    range=Optional[Union[str, "ContigCollectionType"]],
)

slots.contigCollection__ctg_L50 = Slot(
    uri=KB_CDM.ctg_L50,
    name="contigCollection__ctg_L50",
    curie=KB_CDM.curie("ctg_L50"),
    model_uri=KB_CDM.contigCollection__ctg_L50,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__ctg_L90 = Slot(
    uri=KB_CDM.ctg_L90,
    name="contigCollection__ctg_L90",
    curie=KB_CDM.curie("ctg_L90"),
    model_uri=KB_CDM.contigCollection__ctg_L90,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__ctg_N50 = Slot(
    uri=KB_CDM.ctg_N50,
    name="contigCollection__ctg_N50",
    curie=KB_CDM.curie("ctg_N50"),
    model_uri=KB_CDM.contigCollection__ctg_N50,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__ctg_N90 = Slot(
    uri=KB_CDM.ctg_N90,
    name="contigCollection__ctg_N90",
    curie=KB_CDM.curie("ctg_N90"),
    model_uri=KB_CDM.contigCollection__ctg_N90,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__ctg_logsum = Slot(
    uri=KB_CDM.ctg_logsum,
    name="contigCollection__ctg_logsum",
    curie=KB_CDM.curie("ctg_logsum"),
    model_uri=KB_CDM.contigCollection__ctg_logsum,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__ctg_max = Slot(
    uri=KB_CDM.ctg_max,
    name="contigCollection__ctg_max",
    curie=KB_CDM.curie("ctg_max"),
    model_uri=KB_CDM.contigCollection__ctg_max,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__ctg_powsum = Slot(
    uri=KB_CDM.ctg_powsum,
    name="contigCollection__ctg_powsum",
    curie=KB_CDM.curie("ctg_powsum"),
    model_uri=KB_CDM.contigCollection__ctg_powsum,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__gap_pct = Slot(
    uri=KB_CDM.gap_pct,
    name="contigCollection__gap_pct",
    curie=KB_CDM.curie("gap_pct"),
    model_uri=KB_CDM.contigCollection__gap_pct,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__gc_avg = Slot(
    uri=KB_CDM.gc_avg,
    name="contigCollection__gc_avg",
    curie=KB_CDM.curie("gc_avg"),
    model_uri=KB_CDM.contigCollection__gc_avg,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__gc_std = Slot(
    uri=KB_CDM.gc_std,
    name="contigCollection__gc_std",
    curie=KB_CDM.curie("gc_std"),
    model_uri=KB_CDM.contigCollection__gc_std,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__n_contigs = Slot(
    uri=KB_CDM.n_contigs,
    name="contigCollection__n_contigs",
    curie=KB_CDM.curie("n_contigs"),
    model_uri=KB_CDM.contigCollection__n_contigs,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__n_scaffolds = Slot(
    uri=KB_CDM.n_scaffolds,
    name="contigCollection__n_scaffolds",
    curie=KB_CDM.curie("n_scaffolds"),
    model_uri=KB_CDM.contigCollection__n_scaffolds,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_L50 = Slot(
    uri=KB_CDM.scaf_L50,
    name="contigCollection__scaf_L50",
    curie=KB_CDM.curie("scaf_L50"),
    model_uri=KB_CDM.contigCollection__scaf_L50,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_L90 = Slot(
    uri=KB_CDM.scaf_L90,
    name="contigCollection__scaf_L90",
    curie=KB_CDM.curie("scaf_L90"),
    model_uri=KB_CDM.contigCollection__scaf_L90,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_N50 = Slot(
    uri=KB_CDM.scaf_N50,
    name="contigCollection__scaf_N50",
    curie=KB_CDM.curie("scaf_N50"),
    model_uri=KB_CDM.contigCollection__scaf_N50,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_N90 = Slot(
    uri=KB_CDM.scaf_N90,
    name="contigCollection__scaf_N90",
    curie=KB_CDM.curie("scaf_N90"),
    model_uri=KB_CDM.contigCollection__scaf_N90,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_bp = Slot(
    uri=KB_CDM.scaf_bp,
    name="contigCollection__scaf_bp",
    curie=KB_CDM.curie("scaf_bp"),
    model_uri=KB_CDM.contigCollection__scaf_bp,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_l_gt50k = Slot(
    uri=KB_CDM.scaf_l_gt50k,
    name="contigCollection__scaf_l_gt50k",
    curie=KB_CDM.curie("scaf_l_gt50k"),
    model_uri=KB_CDM.contigCollection__scaf_l_gt50k,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_logsum = Slot(
    uri=KB_CDM.scaf_logsum,
    name="contigCollection__scaf_logsum",
    curie=KB_CDM.curie("scaf_logsum"),
    model_uri=KB_CDM.contigCollection__scaf_logsum,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__scaf_max = Slot(
    uri=KB_CDM.scaf_max,
    name="contigCollection__scaf_max",
    curie=KB_CDM.curie("scaf_max"),
    model_uri=KB_CDM.contigCollection__scaf_max,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_n_gt50K = Slot(
    uri=KB_CDM.scaf_n_gt50K,
    name="contigCollection__scaf_n_gt50K",
    curie=KB_CDM.curie("scaf_n_gt50K"),
    model_uri=KB_CDM.contigCollection__scaf_n_gt50K,
    domain=None,
    range=Optional[int],
)

slots.contigCollection__scaf_pct_gt50K = Slot(
    uri=KB_CDM.scaf_pct_gt50K,
    name="contigCollection__scaf_pct_gt50K",
    curie=KB_CDM.curie("scaf_pct_gt50K"),
    model_uri=KB_CDM.contigCollection__scaf_pct_gt50K,
    domain=None,
    range=Optional[float],
)

slots.contigCollection__scaf_powsum = Slot(
    uri=KB_CDM.scaf_powsum,
    name="contigCollection__scaf_powsum",
    curie=KB_CDM.curie("scaf_powsum"),
    model_uri=KB_CDM.contigCollection__scaf_powsum,
    domain=None,
    range=Optional[float],
)

slots.contributor__contributor_type = Slot(
    uri=SCHEMA["@type"],
    name="contributor__contributor_type",
    curie=SCHEMA.curie("@type"),
    model_uri=KB_CDM.contributor__contributor_type,
    domain=None,
    range=Optional[Union[str, "ContributorType"]],
)

slots.contributor__name = Slot(
    uri=SCHEMA.name,
    name="contributor__name",
    curie=SCHEMA.curie("name"),
    model_uri=KB_CDM.contributor__name,
    domain=None,
    range=Optional[str],
)

slots.contributor__given_name = Slot(
    uri=KB_CDM.given_name,
    name="contributor__given_name",
    curie=KB_CDM.curie("given_name"),
    model_uri=KB_CDM.contributor__given_name,
    domain=None,
    range=Optional[str],
)

slots.contributor__family_name = Slot(
    uri=KB_CDM.family_name,
    name="contributor__family_name",
    curie=KB_CDM.curie("family_name"),
    model_uri=KB_CDM.contributor__family_name,
    domain=None,
    range=Optional[str],
)

slots.dataSource__comments = Slot(
    uri=KB_CDM.comments,
    name="dataSource__comments",
    curie=KB_CDM.curie("comments"),
    model_uri=KB_CDM.dataSource__comments,
    domain=None,
    range=Optional[str],
)

slots.dataSource__date_accessed = Slot(
    uri=KB_CDM.date_accessed,
    name="dataSource__date_accessed",
    curie=KB_CDM.curie("date_accessed"),
    model_uri=KB_CDM.dataSource__date_accessed,
    domain=None,
    range=Optional[str],
)

slots.dataSource__url = Slot(
    uri=KB_CDM.url,
    name="dataSource__url",
    curie=KB_CDM.curie("url"),
    model_uri=KB_CDM.dataSource__url,
    domain=None,
    range=Optional[Union[str, URI]],
)

slots.dataSource__version = Slot(
    uri=KB_CDM.version,
    name="dataSource__version",
    curie=KB_CDM.curie("version"),
    model_uri=KB_CDM.dataSource__version,
    domain=None,
    range=Optional[str],
)

slots.encodedFeature__has_stop_codon = Slot(
    uri=KB_CDM.has_stop_codon,
    name="encodedFeature__has_stop_codon",
    curie=KB_CDM.curie("has_stop_codon"),
    model_uri=KB_CDM.encodedFeature__has_stop_codon,
    domain=None,
    range=Optional[Union[bool, Bool]],
)

slots.encodedFeature__type = Slot(
    uri=KB_CDM.type,
    name="encodedFeature__type",
    curie=KB_CDM.curie("type"),
    model_uri=KB_CDM.encodedFeature__type,
    domain=None,
    range=Optional[str],
    pattern=re.compile(r"^SO:\d+$"),
)

slots.goldEnvironmentalContext__ecosystem = Slot(
    uri=KB_CDM.ecosystem,
    name="goldEnvironmentalContext__ecosystem",
    curie=KB_CDM.curie("ecosystem"),
    model_uri=KB_CDM.goldEnvironmentalContext__ecosystem,
    domain=None,
    range=Optional[str],
)

slots.goldEnvironmentalContext__ecosystem_category = Slot(
    uri=KB_CDM.ecosystem_category,
    name="goldEnvironmentalContext__ecosystem_category",
    curie=KB_CDM.curie("ecosystem_category"),
    model_uri=KB_CDM.goldEnvironmentalContext__ecosystem_category,
    domain=None,
    range=Optional[str],
)

slots.goldEnvironmentalContext__ecosystem_subtype = Slot(
    uri=KB_CDM.ecosystem_subtype,
    name="goldEnvironmentalContext__ecosystem_subtype",
    curie=KB_CDM.curie("ecosystem_subtype"),
    model_uri=KB_CDM.goldEnvironmentalContext__ecosystem_subtype,
    domain=None,
    range=Optional[str],
)

slots.goldEnvironmentalContext__ecosystem_type = Slot(
    uri=KB_CDM.ecosystem_type,
    name="goldEnvironmentalContext__ecosystem_type",
    curie=KB_CDM.curie("ecosystem_type"),
    model_uri=KB_CDM.goldEnvironmentalContext__ecosystem_type,
    domain=None,
    range=Optional[str],
)

slots.goldEnvironmentalContext__specific_ecosystem = Slot(
    uri=KB_CDM.specific_ecosystem,
    name="goldEnvironmentalContext__specific_ecosystem",
    curie=KB_CDM.curie("specific_ecosystem"),
    model_uri=KB_CDM.goldEnvironmentalContext__specific_ecosystem,
    domain=None,
    range=Optional[str],
)

slots.mixsEnvironmentalContext__env_broad_scale = Slot(
    uri=MIXS["0000012"],
    name="mixsEnvironmentalContext__env_broad_scale",
    curie=MIXS.curie("0000012"),
    model_uri=KB_CDM.mixsEnvironmentalContext__env_broad_scale,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.mixsEnvironmentalContext__env_local_scale = Slot(
    uri=MIXS["0000013"],
    name="mixsEnvironmentalContext__env_local_scale",
    curie=MIXS.curie("0000013"),
    model_uri=KB_CDM.mixsEnvironmentalContext__env_local_scale,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.mixsEnvironmentalContext__env_medium = Slot(
    uri=MIXS["0000014"],
    name="mixsEnvironmentalContext__env_medium",
    curie=MIXS.curie("0000014"),
    model_uri=KB_CDM.mixsEnvironmentalContext__env_medium,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.event__created_at = Slot(
    uri=KB_CDM.created_at,
    name="event__created_at",
    curie=KB_CDM.curie("created_at"),
    model_uri=KB_CDM.event__created_at,
    domain=None,
    range=Optional[str],
)

slots.event__description = Slot(
    uri=KB_CDM.description,
    name="event__description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.event__description,
    domain=None,
    range=Optional[str],
)

slots.event__name = Slot(
    uri=KB_CDM.name,
    name="event__name",
    curie=KB_CDM.curie("name"),
    model_uri=KB_CDM.event__name,
    domain=None,
    range=Optional[str],
)

slots.event__location = Slot(
    uri=KB_CDM.location,
    name="event__location",
    curie=KB_CDM.curie("location"),
    model_uri=KB_CDM.event__location,
    domain=None,
    range=Optional[str],
)

slots.experiment__created_at = Slot(
    uri=KB_CDM.created_at,
    name="experiment__created_at",
    curie=KB_CDM.curie("created_at"),
    model_uri=KB_CDM.experiment__created_at,
    domain=None,
    range=Optional[str],
)

slots.experiment__description = Slot(
    uri=KB_CDM.description,
    name="experiment__description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.experiment__description,
    domain=None,
    range=Optional[str],
)

slots.experiment__name = Slot(
    uri=KB_CDM.name,
    name="experiment__name",
    curie=KB_CDM.curie("name"),
    model_uri=KB_CDM.experiment__name,
    domain=None,
    range=Optional[str],
)

slots.feature__cds_phase = Slot(
    uri=KB_CDM.cds_phase,
    name="feature__cds_phase",
    curie=KB_CDM.curie("cds_phase"),
    model_uri=KB_CDM.feature__cds_phase,
    domain=None,
    range=Optional[Union[str, "CdsPhaseType"]],
)

slots.feature__e_value = Slot(
    uri=KB_CDM.e_value,
    name="feature__e_value",
    curie=KB_CDM.curie("e_value"),
    model_uri=KB_CDM.feature__e_value,
    domain=None,
    range=Optional[float],
)

slots.feature__end = Slot(
    uri=KB_CDM.end,
    name="feature__end",
    curie=KB_CDM.curie("end"),
    model_uri=KB_CDM.feature__end,
    domain=None,
    range=Optional[int],
)

slots.feature__p_value = Slot(
    uri=KB_CDM.p_value,
    name="feature__p_value",
    curie=KB_CDM.curie("p_value"),
    model_uri=KB_CDM.feature__p_value,
    domain=None,
    range=Optional[float],
)

slots.feature__start = Slot(
    uri=KB_CDM.start,
    name="feature__start",
    curie=KB_CDM.curie("start"),
    model_uri=KB_CDM.feature__start,
    domain=None,
    range=Optional[int],
)

slots.feature__strand = Slot(
    uri=KB_CDM.strand,
    name="feature__strand",
    curie=KB_CDM.curie("strand"),
    model_uri=KB_CDM.feature__strand,
    domain=None,
    range=Optional[Union[str, "StrandType"]],
)

slots.feature__source_database = Slot(
    uri=KB_CDM.source_database,
    name="feature__source_database",
    curie=KB_CDM.curie("source_database"),
    model_uri=KB_CDM.feature__source_database,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.feature__protocol_id = Slot(
    uri=KB_CDM.protocol_id,
    name="feature__protocol_id",
    curie=KB_CDM.curie("protocol_id"),
    model_uri=KB_CDM.feature__protocol_id,
    domain=None,
    range=Optional[Union[str, ProtocolProtocolId]],
)

slots.feature__type = Slot(
    uri=KB_CDM.type,
    name="feature__type",
    curie=KB_CDM.curie("type"),
    model_uri=KB_CDM.feature__type,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
    pattern=re.compile(r"^SO:\d+$"),
)

slots.project__description = Slot(
    uri=KB_CDM.description,
    name="project__description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.project__description,
    domain=None,
    range=Optional[str],
)

slots.protein__description = Slot(
    uri=KB_CDM.description,
    name="protein__description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.protein__description,
    domain=None,
    range=Optional[str],
)

slots.protein__evidence_for_existence = Slot(
    uri=KB_CDM.evidence_for_existence,
    name="protein__evidence_for_existence",
    curie=KB_CDM.curie("evidence_for_existence"),
    model_uri=KB_CDM.protein__evidence_for_existence,
    domain=None,
    range=Optional[Union[str, "ProteinEvidenceForExistence"]],
)

slots.protein__length = Slot(
    uri=KB_CDM.length,
    name="protein__length",
    curie=KB_CDM.curie("length"),
    model_uri=KB_CDM.protein__length,
    domain=None,
    range=Optional[int],
)

slots.protein__sequence = Slot(
    uri=KB_CDM.sequence,
    name="protein__sequence",
    curie=KB_CDM.curie("sequence"),
    model_uri=KB_CDM.protein__sequence,
    domain=None,
    range=Optional[str],
)

slots.protocol__doi = Slot(
    uri=KB_CDM.doi,
    name="protocol__doi",
    curie=KB_CDM.curie("doi"),
    model_uri=KB_CDM.protocol__doi,
    domain=None,
    range=Optional[str],
)

slots.protocol__description = Slot(
    uri=KB_CDM.description,
    name="protocol__description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.protocol__description,
    domain=None,
    range=Optional[str],
)

slots.protocol__version = Slot(
    uri=KB_CDM.version,
    name="protocol__version",
    curie=KB_CDM.curie("version"),
    model_uri=KB_CDM.protocol__version,
    domain=None,
    range=Optional[str],
)

slots.protocol__url = Slot(
    uri=KB_CDM.url,
    name="protocol__url",
    curie=KB_CDM.curie("url"),
    model_uri=KB_CDM.protocol__url,
    domain=None,
    range=Optional[str],
)

slots.protocolParticipant__protocol_participant_id = Slot(
    uri=KB_CDM.protocol_participant_id,
    name="protocolParticipant__protocol_participant_id",
    curie=KB_CDM.curie("protocol_participant_id"),
    model_uri=KB_CDM.protocolParticipant__protocol_participant_id,
    domain=None,
    range=URIRef,
)

slots.sample__description = Slot(
    uri=KB_CDM.description,
    name="sample__description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.sample__description,
    domain=None,
    range=Optional[str],
)

slots.sample__type = Slot(
    uri=KB_CDM.type,
    name="sample__type",
    curie=KB_CDM.curie("type"),
    model_uri=KB_CDM.sample__type,
    domain=None,
    range=Optional[str],
)

slots.sequence__type = Slot(
    uri=KB_CDM.type,
    name="sequence__type",
    curie=KB_CDM.curie("type"),
    model_uri=KB_CDM.sequence__type,
    domain=None,
    range=Optional[Union[str, "SequenceType"]],
)

slots.sequence__length = Slot(
    uri=KB_CDM.length,
    name="sequence__length",
    curie=KB_CDM.curie("length"),
    model_uri=KB_CDM.sequence__length,
    domain=None,
    range=Optional[int],
)

slots.sequence__checksum = Slot(
    uri=KB_CDM.checksum,
    name="sequence__checksum",
    curie=KB_CDM.curie("checksum"),
    model_uri=KB_CDM.sequence__checksum,
    domain=None,
    range=Optional[str],
)

slots.geolocation__latitude = Slot(
    uri=KB_CDM.latitude,
    name="geolocation__latitude",
    curie=KB_CDM.curie("latitude"),
    model_uri=KB_CDM.geolocation__latitude,
    domain=None,
    range=str,
)

slots.geolocation__longitude = Slot(
    uri=KB_CDM.longitude,
    name="geolocation__longitude",
    curie=KB_CDM.curie("longitude"),
    model_uri=KB_CDM.geolocation__longitude,
    domain=None,
    range=str,
)

slots.geolocation__raw_value = Slot(
    uri=KB_CDM.raw_value,
    name="geolocation__raw_value",
    curie=KB_CDM.curie("raw_value"),
    model_uri=KB_CDM.geolocation__raw_value,
    domain=None,
    range=Optional[str],
)

slots.attributeValue__attribute_name = Slot(
    uri=KB_CDM.attribute_name,
    name="attributeValue__attribute_name",
    curie=KB_CDM.curie("attribute_name"),
    model_uri=KB_CDM.attributeValue__attribute_name,
    domain=None,
    range=str,
)

slots.attributeValue__attribute_cv_term_id = Slot(
    uri=KB_CDM.attribute_cv_term_id,
    name="attributeValue__attribute_cv_term_id",
    curie=KB_CDM.curie("attribute_cv_term_id"),
    model_uri=KB_CDM.attributeValue__attribute_cv_term_id,
    domain=None,
    range=Optional[Union[str, LocalCurie]],
)

slots.attributeValue__raw_value = Slot(
    uri=KB_CDM.raw_value,
    name="attributeValue__raw_value",
    curie=KB_CDM.curie("raw_value"),
    model_uri=KB_CDM.attributeValue__raw_value,
    domain=None,
    range=Optional[str],
)

slots.quantityValue__maximum_value = Slot(
    uri=KB_CDM.maximum_value,
    name="quantityValue__maximum_value",
    curie=KB_CDM.curie("maximum_value"),
    model_uri=KB_CDM.quantityValue__maximum_value,
    domain=None,
    range=Optional[float],
)

slots.quantityValue__minimum_value = Slot(
    uri=KB_CDM.minimum_value,
    name="quantityValue__minimum_value",
    curie=KB_CDM.curie("minimum_value"),
    model_uri=KB_CDM.quantityValue__minimum_value,
    domain=None,
    range=Optional[float],
)

slots.quantityValue__value = Slot(
    uri=KB_CDM.value,
    name="quantityValue__value",
    curie=KB_CDM.curie("value"),
    model_uri=KB_CDM.quantityValue__value,
    domain=None,
    range=Optional[float],
)

slots.quantityValue__unit = Slot(
    uri=KB_CDM.unit,
    name="quantityValue__unit",
    curie=KB_CDM.curie("unit"),
    model_uri=KB_CDM.quantityValue__unit,
    domain=None,
    range=Optional[Union[str, Curie]],
)

slots.textValue__value = Slot(
    uri=KB_CDM.value,
    name="textValue__value",
    curie=KB_CDM.curie("value"),
    model_uri=KB_CDM.textValue__value,
    domain=None,
    range=str,
)

slots.textValue__value_cv_term_id = Slot(
    uri=KB_CDM.value_cv_term_id,
    name="textValue__value_cv_term_id",
    curie=KB_CDM.curie("value_cv_term_id"),
    model_uri=KB_CDM.textValue__value_cv_term_id,
    domain=None,
    range=Optional[Union[str, LocalCurie]],
)

slots.textValue__language = Slot(
    uri=KB_CDM.language,
    name="textValue__language",
    curie=KB_CDM.curie("language"),
    model_uri=KB_CDM.textValue__language,
    domain=None,
    range=Optional[str],
)

slots.measurement__created_at = Slot(
    uri=KB_CDM.created_at,
    name="measurement__created_at",
    curie=KB_CDM.curie("created_at"),
    model_uri=KB_CDM.measurement__created_at,
    domain=None,
    range=Optional[str],
)

slots.measurement__quality = Slot(
    uri=KB_CDM.quality,
    name="measurement__quality",
    curie=KB_CDM.curie("quality"),
    model_uri=KB_CDM.measurement__quality,
    domain=None,
    range=Optional[str],
)

slots.entity__entity_type = Slot(
    uri=KB_CDM.entity_type,
    name="entity__entity_type",
    curie=KB_CDM.curie("entity_type"),
    model_uri=KB_CDM.entity__entity_type,
    domain=None,
    range=Union[str, "EntityType"],
)

slots.entity__data_source_entity_id = Slot(
    uri=KB_CDM.data_source_entity_id,
    name="entity__data_source_entity_id",
    curie=KB_CDM.curie("data_source_entity_id"),
    model_uri=KB_CDM.entity__data_source_entity_id,
    domain=None,
    range=Optional[Union[str, URIorCURIE]],
)

slots.entity__data_source_created = Slot(
    uri=KB_CDM.data_source_created,
    name="entity__data_source_created",
    curie=KB_CDM.curie("data_source_created"),
    model_uri=KB_CDM.entity__data_source_created,
    domain=None,
    range=str,
)

slots.entity__data_source_updated = Slot(
    uri=KB_CDM.data_source_updated,
    name="entity__data_source_updated",
    curie=KB_CDM.curie("data_source_updated"),
    model_uri=KB_CDM.entity__data_source_updated,
    domain=None,
    range=Optional[str],
)

slots.entity__created = Slot(
    uri=KB_CDM.created,
    name="entity__created",
    curie=KB_CDM.curie("created"),
    model_uri=KB_CDM.entity__created,
    domain=None,
    range=str,
)

slots.entity__updated = Slot(
    uri=KB_CDM.updated,
    name="entity__updated",
    curie=KB_CDM.curie("updated"),
    model_uri=KB_CDM.entity__updated,
    domain=None,
    range=str,
)

slots.identifier__relationship = Slot(
    uri=KB_CDM.relationship,
    name="identifier__relationship",
    curie=KB_CDM.curie("relationship"),
    model_uri=KB_CDM.identifier__relationship,
    domain=None,
    range=Optional[str],
)

slots.Association_X_Publication_association_id = Slot(
    uri=KB_CDM.association_id,
    name="Association_X_Publication_association_id",
    curie=KB_CDM.curie("association_id"),
    model_uri=KB_CDM.Association_X_Publication_association_id,
    domain=AssociationXPublication,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Association_X_Publication_publication_id = Slot(
    uri=KB_CDM.publication_id,
    name="Association_X_Publication_publication_id",
    curie=KB_CDM.curie("publication_id"),
    model_uri=KB_CDM.Association_X_Publication_publication_id,
    domain=AssociationXPublication,
    range=Union[Union[str, URIorCURIE], list[Union[str, URIorCURIE]]],
)

slots.Association_X_SupportingObject_association_id = Slot(
    uri=KB_CDM.association_id,
    name="Association_X_SupportingObject_association_id",
    curie=KB_CDM.curie("association_id"),
    model_uri=KB_CDM.Association_X_SupportingObject_association_id,
    domain=AssociationXSupportingObject,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Association_X_SupportingObject_entity_id = Slot(
    uri=KB_CDM.entity_id,
    name="Association_X_SupportingObject_entity_id",
    curie=KB_CDM.curie("entity_id"),
    model_uri=KB_CDM.Association_X_SupportingObject_entity_id,
    domain=AssociationXSupportingObject,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Contig_X_ContigCollection_contig_id = Slot(
    uri=KB_CDM.contig_id,
    name="Contig_X_ContigCollection_contig_id",
    curie=KB_CDM.curie("contig_id"),
    model_uri=KB_CDM.Contig_X_ContigCollection_contig_id,
    domain=ContigXContigCollection,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Contig_X_EncodedFeature_encoded_feature_id = Slot(
    uri=KB_CDM.encoded_feature_id,
    name="Contig_X_EncodedFeature_encoded_feature_id",
    curie=KB_CDM.curie("encoded_feature_id"),
    model_uri=KB_CDM.Contig_X_EncodedFeature_encoded_feature_id,
    domain=ContigXEncodedFeature,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Contig_X_Feature_feature_id = Slot(
    uri=KB_CDM.feature_id,
    name="Contig_X_Feature_feature_id",
    curie=KB_CDM.curie("feature_id"),
    model_uri=KB_CDM.Contig_X_Feature_feature_id,
    domain=ContigXFeature,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Contig_X_Protein_protein_id = Slot(
    uri=KB_CDM.protein_id,
    name="Contig_X_Protein_protein_id",
    curie=KB_CDM.curie("protein_id"),
    model_uri=KB_CDM.Contig_X_Protein_protein_id,
    domain=ContigXProtein,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.ContigCollection_X_EncodedFeature_encoded_feature_id = Slot(
    uri=KB_CDM.encoded_feature_id,
    name="ContigCollection_X_EncodedFeature_encoded_feature_id",
    curie=KB_CDM.curie("encoded_feature_id"),
    model_uri=KB_CDM.ContigCollection_X_EncodedFeature_encoded_feature_id,
    domain=ContigCollectionXEncodedFeature,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.ContigCollection_X_Feature_feature_id = Slot(
    uri=KB_CDM.feature_id,
    name="ContigCollection_X_Feature_feature_id",
    curie=KB_CDM.curie("feature_id"),
    model_uri=KB_CDM.ContigCollection_X_Feature_feature_id,
    domain=ContigCollectionXFeature,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.ContigCollection_X_Protein_protein_id = Slot(
    uri=KB_CDM.protein_id,
    name="ContigCollection_X_Protein_protein_id",
    curie=KB_CDM.curie("protein_id"),
    model_uri=KB_CDM.ContigCollection_X_Protein_protein_id,
    domain=ContigCollectionXProtein,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Entity_X_Measurement_entity_id = Slot(
    uri=KB_CDM.entity_id,
    name="Entity_X_Measurement_entity_id",
    curie=KB_CDM.curie("entity_id"),
    model_uri=KB_CDM.Entity_X_Measurement_entity_id,
    domain=EntityXMeasurement,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Entity_X_Measurement_measurement_id = Slot(
    uri=KB_CDM.measurement_id,
    name="Entity_X_Measurement_measurement_id",
    curie=KB_CDM.curie("measurement_id"),
    model_uri=KB_CDM.Entity_X_Measurement_measurement_id,
    domain=EntityXMeasurement,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Experiment_X_Project_experiment_id = Slot(
    uri=KB_CDM.experiment_id,
    name="Experiment_X_Project_experiment_id",
    curie=KB_CDM.curie("experiment_id"),
    model_uri=KB_CDM.Experiment_X_Project_experiment_id,
    domain=ExperimentXProject,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Experiment_X_Sample_experiment_id = Slot(
    uri=KB_CDM.experiment_id,
    name="Experiment_X_Sample_experiment_id",
    curie=KB_CDM.curie("experiment_id"),
    model_uri=KB_CDM.Experiment_X_Sample_experiment_id,
    domain=ExperimentXSample,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Experiment_X_Sample_sample_id = Slot(
    uri=KB_CDM.sample_id,
    name="Experiment_X_Sample_sample_id",
    curie=KB_CDM.curie("sample_id"),
    model_uri=KB_CDM.Experiment_X_Sample_sample_id,
    domain=ExperimentXSample,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Feature_X_Protein_protein_id = Slot(
    uri=KB_CDM.protein_id,
    name="Feature_X_Protein_protein_id",
    curie=KB_CDM.curie("protein_id"),
    model_uri=KB_CDM.Feature_X_Protein_protein_id,
    domain=FeatureXProtein,
    range=Union[Union[str, UUID], list[Union[str, UUID]]],
)

slots.Association_association_id = Slot(
    uri=KB_CDM.association_id,
    name="Association_association_id",
    curie=KB_CDM.curie("association_id"),
    model_uri=KB_CDM.Association_association_id,
    domain=Association,
    range=Union[str, AssociationAssociationId],
)

slots.Association_subject = Slot(
    uri=RDF.subject,
    name="Association_subject",
    curie=RDF.curie("subject"),
    model_uri=KB_CDM.Association_subject,
    domain=Association,
    range=Union[dict, Any],
)

slots.Association_predicate = Slot(
    uri=RDF.predicate,
    name="Association_predicate",
    curie=RDF.curie("predicate"),
    model_uri=KB_CDM.Association_predicate,
    domain=Association,
    range=Optional[Union[str, LocalCurie]],
)

slots.Association_object = Slot(
    uri=RDF.object,
    name="Association_object",
    curie=RDF.curie("object"),
    model_uri=KB_CDM.Association_object,
    domain=Association,
    range=Union[str, LocalCurie],
)

slots.Cluster_cluster_id = Slot(
    uri=KB_CDM.cluster_id,
    name="Cluster_cluster_id",
    curie=KB_CDM.curie("cluster_id"),
    model_uri=KB_CDM.Cluster_cluster_id,
    domain=Cluster,
    range=Union[str, ClusterClusterId],
)

slots.Contig_contig_id = Slot(
    uri=KB_CDM.contig_id,
    name="Contig_contig_id",
    curie=KB_CDM.curie("contig_id"),
    model_uri=KB_CDM.Contig_contig_id,
    domain=Contig,
    range=Union[str, ContigContigId],
)

slots.ContigCollection_contig_collection_id = Slot(
    uri=KB_CDM.contig_collection_id,
    name="ContigCollection_contig_collection_id",
    curie=KB_CDM.curie("contig_collection_id"),
    model_uri=KB_CDM.ContigCollection_contig_collection_id,
    domain=ContigCollection,
    range=Union[str, ContigCollectionContigCollectionId],
)

slots.Contributor_contributor_id = Slot(
    uri=KB_CDM.contributor_id,
    name="Contributor_contributor_id",
    curie=KB_CDM.curie("contributor_id"),
    model_uri=KB_CDM.Contributor_contributor_id,
    domain=Contributor,
    range=Union[str, ContributorContributorId],
)

slots.DataSource_data_source_id = Slot(
    uri=KB_CDM.data_source_id,
    name="DataSource_data_source_id",
    curie=KB_CDM.curie("data_source_id"),
    model_uri=KB_CDM.DataSource_data_source_id,
    domain=DataSource,
    range=Union[str, DataSourceDataSourceId],
)

slots.DataSource_name = Slot(
    uri=SCHEMA.name,
    name="DataSource_name",
    curie=SCHEMA.curie("name"),
    model_uri=KB_CDM.DataSource_name,
    domain=DataSource,
    range=Optional[str],
)

slots.EncodedFeature_encoded_feature_id = Slot(
    uri=KB_CDM.encoded_feature_id,
    name="EncodedFeature_encoded_feature_id",
    curie=KB_CDM.curie("encoded_feature_id"),
    model_uri=KB_CDM.EncodedFeature_encoded_feature_id,
    domain=EncodedFeature,
    range=Union[str, EncodedFeatureEncodedFeatureId],
)

slots.GoldEnvironmentalContext_gold_environmental_context_id = Slot(
    uri=KB_CDM.gold_environmental_context_id,
    name="GoldEnvironmentalContext_gold_environmental_context_id",
    curie=KB_CDM.curie("gold_environmental_context_id"),
    model_uri=KB_CDM.GoldEnvironmentalContext_gold_environmental_context_id,
    domain=GoldEnvironmentalContext,
    range=Union[str, GoldEnvironmentalContextGoldEnvironmentalContextId],
)

slots.MixsEnvironmentalContext_mixs_environmental_context_id = Slot(
    uri=KB_CDM.mixs_environmental_context_id,
    name="MixsEnvironmentalContext_mixs_environmental_context_id",
    curie=KB_CDM.curie("mixs_environmental_context_id"),
    model_uri=KB_CDM.MixsEnvironmentalContext_mixs_environmental_context_id,
    domain=MixsEnvironmentalContext,
    range=Union[str, MixsEnvironmentalContextMixsEnvironmentalContextId],
)

slots.Event_event_id = Slot(
    uri=KB_CDM.event_id,
    name="Event_event_id",
    curie=KB_CDM.curie("event_id"),
    model_uri=KB_CDM.Event_event_id,
    domain=Event,
    range=Union[str, EventEventId],
)

slots.Experiment_experiment_id = Slot(
    uri=KB_CDM.experiment_id,
    name="Experiment_experiment_id",
    curie=KB_CDM.curie("experiment_id"),
    model_uri=KB_CDM.Experiment_experiment_id,
    domain=Experiment,
    range=Union[str, ExperimentExperimentId],
)

slots.Feature_feature_id = Slot(
    uri=KB_CDM.feature_id,
    name="Feature_feature_id",
    curie=KB_CDM.curie("feature_id"),
    model_uri=KB_CDM.Feature_feature_id,
    domain=Feature,
    range=Union[str, FeatureFeatureId],
)

slots.Project_project_id = Slot(
    uri=KB_CDM.project_id,
    name="Project_project_id",
    curie=KB_CDM.curie("project_id"),
    model_uri=KB_CDM.Project_project_id,
    domain=Project,
    range=Union[str, ProjectProjectId],
)

slots.Protein_protein_id = Slot(
    uri=KB_CDM.protein_id,
    name="Protein_protein_id",
    curie=KB_CDM.curie("protein_id"),
    model_uri=KB_CDM.Protein_protein_id,
    domain=Protein,
    range=Union[str, ProteinProteinId],
)

slots.Protocol_protocol_id = Slot(
    uri=KB_CDM.protocol_id,
    name="Protocol_protocol_id",
    curie=KB_CDM.curie("protocol_id"),
    model_uri=KB_CDM.Protocol_protocol_id,
    domain=Protocol,
    range=Union[str, ProtocolProtocolId],
)

slots.Publication_publication_id = Slot(
    uri=KB_CDM.publication_id,
    name="Publication_publication_id",
    curie=KB_CDM.curie("publication_id"),
    model_uri=KB_CDM.Publication_publication_id,
    domain=Publication,
    range=Union[str, PublicationPublicationId],
)

slots.Sample_sample_id = Slot(
    uri=KB_CDM.sample_id,
    name="Sample_sample_id",
    curie=KB_CDM.curie("sample_id"),
    model_uri=KB_CDM.Sample_sample_id,
    domain=Sample,
    range=Union[str, SampleSampleId],
)

slots.Sequence_entity_id = Slot(
    uri=KB_CDM.entity_id,
    name="Sequence_entity_id",
    curie=KB_CDM.curie("entity_id"),
    model_uri=KB_CDM.Sequence_entity_id,
    domain=Sequence,
    range=Union[str, UUID],
)

slots.AttributeValue_entity_id = Slot(
    uri=KB_CDM.entity_id,
    name="AttributeValue_entity_id",
    curie=KB_CDM.curie("entity_id"),
    model_uri=KB_CDM.AttributeValue_entity_id,
    domain=AttributeValue,
    range=Union[str, UUID],
)

slots.Measurement_measurement_id = Slot(
    uri=KB_CDM.measurement_id,
    name="Measurement_measurement_id",
    curie=KB_CDM.curie("measurement_id"),
    model_uri=KB_CDM.Measurement_measurement_id,
    domain=Measurement,
    range=Union[str, MeasurementMeasurementId],
)

slots.Measurement_protocol_id = Slot(
    uri=KB_CDM.protocol_id,
    name="Measurement_protocol_id",
    curie=KB_CDM.curie("protocol_id"),
    model_uri=KB_CDM.Measurement_protocol_id,
    domain=Measurement,
    range=Union[str, UUID],
)

slots.Entity_entity_id = Slot(
    uri=KB_CDM.entity_id,
    name="Entity_entity_id",
    curie=KB_CDM.curie("entity_id"),
    model_uri=KB_CDM.Entity_entity_id,
    domain=Entity,
    range=Union[str, EntityEntityId],
)

slots.Identifier_description = Slot(
    uri=KB_CDM.description,
    name="Identifier_description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.Identifier_description,
    domain=Identifier,
    range=Optional[str],
)

slots.Name_description = Slot(
    uri=KB_CDM.description,
    name="Name_description",
    curie=KB_CDM.curie("description"),
    model_uri=KB_CDM.Name_description,
    domain=Name,
    range=Optional[str],
)

slots.Name_name = Slot(
    uri=SCHEMA.name, name="Name_name", curie=SCHEMA.curie("name"), model_uri=KB_CDM.Name_name, domain=Name, range=str
)
