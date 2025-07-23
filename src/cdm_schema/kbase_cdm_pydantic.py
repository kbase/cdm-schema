from __future__ import annotations

import re
import sys
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, field_validator


metamodel_version = "None"
version = "0.0.1"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )
    pass


class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta(
    {
        "default_curi_maps": ["semweb_context"],
        "default_prefix": "kb_cdm",
        "default_range": "string",
        "description": "Schema for KBase CDM",
        "id": "http://kbase.github.io/cdm-schema/cdm_schema",
        "imports": ["linkml:types", "cdm_components", "cdm_to_review"],
        "name": "cdm_schema",
        "prefixes": {
            "kb_cdm": {"prefix_prefix": "kb_cdm", "prefix_reference": "http://kbase.github.io/cdm-schema/"},
            "linkml": {"prefix_prefix": "linkml", "prefix_reference": "https://w3id.org/linkml/"},
            "mixs": {
                "prefix_prefix": "mixs",
                "prefix_reference": "https://genomicsstandardsconsortium.github.io/mixs/",
            },
            "schema": {"prefix_prefix": "schema", "prefix_reference": "http://schema.org/"},
        },
        "source_file": "src/linkml/cdm_schema.yaml",
    }
)


class CdsPhaseType(str, Enum):
    """
    For features of type CDS (coding sequence), the phase indicates where the feature begins with reference to the reading frame. The phase is one of the integers 0, 1, or 2, indicating the number of bases that should be removed from the beginning of this feature to reach the first base of the next codon.
    """

    number_0 = "0"
    """
    Zero bases from reading frame to feature start.
    """
    number_1 = "1"
    """
    One base from reading frame to feature start.
    """
    number_2 = "2"
    """
    Two bases from reading frame to feature start.
    """


class ClusterType(str, Enum):
    """
    The type of the entities in a cluster. Must be represented by a table in the CDM schema.
    """

    Protein = "Protein"
    Feature = "Feature"
    ContigCollection = "ContigCollection"


class ContigCollectionType(str, Enum):
    """
    The type of the contig set; the type of the 'omics data set. Terms are taken from the Genomics Standards Consortium where possible. See the GSC checklists at  https://genomicsstandardsconsortium.github.io/mixs/ for the controlled vocabularies used.
    """

    isolate = "isolate"
    """
    Sequences assembled from DNA of isolated organism.
    Bacteria/Archaea: https://genomicsstandardsconsortium.github.io/mixs/0010003/
    Euk: https://genomicsstandardsconsortium.github.io/mixs/0010002/
    Virus: https://genomicsstandardsconsortium.github.io/mixs/0010005/
    Organelle: https://genomicsstandardsconsortium.github.io/mixs/0010006/
    Plasmid: https://genomicsstandardsconsortium.github.io/mixs/0010004/

    """
    Metagenome_Assembled_Genome = "mag"
    """
    Sequences assembled from DNA of mixed community and binned. MAGs are likely to represent a single taxonomic origin. See checkm2 scores for quality assessment.
    https://genomicsstandardsconsortium.github.io/mixs/0010011/

    """
    metagenome = "metagenome"
    """
    Sequences assembled from DNA of mixed community.
    https://genomicsstandardsconsortium.github.io/mixs/0010007/

    """
    metatranscriptome = "metatranscriptome"
    """
    Sequences assembled from RNA of mixed community. Currently not represented by GSC.

    """
    Single_Amplified_Genome = "sag"
    """
    Sequences assembled from DNA of single cell.
    https://genomicsstandardsconsortium.github.io/mixs/0010010/

    """
    virus = "virus"
    """
    Sequences assembled from uncultivated virus genome (DNA/RNA).
    https://genomicsstandardsconsortium.github.io/mixs/0010012/

    """
    marker = "marker"
    """
    Sequences from targeted region of DNA; see protocol for information on targeted region.
    specimen: https://genomicsstandardsconsortium.github.io/mixs/0010009/
    survey: https://genomicsstandardsconsortium.github.io/mixs/0010008/

    """


class ContributorRole(str, Enum):
    """
    The role of a contributor to a resource.
    """

    TODO = "TODO"


class ContributorType(str, Enum):
    """
    The type of contributor being represented.
    """

    Person = "Person"
    """
    A person.
    """
    Organization = "Organization"
    """
    An organization.
    """


class EntityType(str, Enum):
    """
    The type of an entity. Must be represented by a table in the CDM schema.
    """

    Cluster = "Cluster"
    Contig = "Contig"
    ContigCollection = "ContigCollection"
    EncodedFeature = "EncodedFeature"
    """
    The output of transcribing a sequence; includes mRNA, tRNA, etc.
    """
    Feature = "Feature"
    Protein = "Protein"
    Sample = "Sample"
    Organization = "Organization"
    Contributor = "Contributor"
    Project = "Project"
    Experiment = "Experiment"


class ProteinEvidenceForExistence(str, Enum):
    """
    The evidence for the existence of a biological entity. See https://www.uniprot.org/help/protein_existence and https://www.ncbi.nlm.nih.gov/genbank/evidence/.
    """

    experimental_evidence_at_protein_level = "experimental_evidence_at_protein_level"
    """
    Indicates that there is clear experimental evidence for the existence of the protein. The criteria include partial or complete Edman sequencing, clear identification by mass spectrometry, X-ray or NMR structure, good quality protein-protein interaction or detection of the protein by antibodies.
    """
    experimental_evidence_at_transcript_level = "experimental_evidence_at_transcript_level"
    """
    Indicates that the existence of a protein has not been strictly proven but that expression data (such as existence of cDNA(s), RT-PCR or Northern blots) indicate the existence of a transcript.
    """
    protein_inferred_by_homology = "protein_inferred_by_homology"
    """
    Indicates that the existence of a protein is probable because clear orthologs exist in closely related species.
    """
    protein_predicted = "protein_predicted"
    """
    Used for entries without evidence at protein, transcript, or homology levels.
    """
    protein_uncertain = "protein_uncertain"
    """
    Indicates that the existence of the protein is unsure.
    """


class RefSeqStatusType(str, Enum):
    """
    RefSeq status codes, taken from https://www.ncbi.nlm.nih.gov/genbank/evidence/.

    """

    MODEL = "MODEL"
    """
    The RefSeq record is provided by the NCBI Genome Annotation pipeline and is not subject to individual review or revision between annotation runs.
    """
    INFERRED = "INFERRED"
    """
    The RefSeq record has been predicted by genome sequence analysis, but it is not yet supported by experimental evidence. The record may be partially supported by homology data.
    """
    PREDICTED = "PREDICTED"
    """
    The RefSeq record has not yet been subject to individual review, and some aspect of the RefSeq record is predicted.
    """
    PROVISIONAL = "PROVISIONAL"
    """
    The RefSeq record has not yet been subject to individual review. The initial sequence-to-gene association has been established by outside collaborators or NCBI staff.
    """
    REVIEWED = "REVIEWED"
    """
    The RefSeq record has been reviewed by NCBI staff or by a collaborator. The NCBI review process includes assessing available sequence data and the literature. Some RefSeq records may incorporate expanded sequence and annotation information.
    """
    VALIDATED = "VALIDATED"
    """
    The RefSeq record has undergone an initial review to provide the preferred sequence standard. The record has not yet been subject to final review at which time additional functional information may be provided.
    """
    WGS = "WGS"
    """
    The RefSeq record is provided to represent a collection of whole genome shotgun sequences. These records are not subject to individual review or revisions between genome updates.
    """


class SequenceType(str, Enum):
    """
    The type of sequence being represented.
    """

    NucleicAcid = "NucleicAcid"
    """
    A nucleic acid sequence, as found in an FNA file.
    """
    AminoAcid = "AminoAcid"
    """
    An amino acid sequence, as would be found in an FAA file.
    """


class StrandType(str, Enum):
    """
    The strand that a feature appears on relative to a landmark. Also encompasses unknown or irrelevant strandedness.
    """

    negative = "negative"
    """
    Represented by "-" in a GFF file; the strand is negative wrt the landmark.
    """
    positive = "positive"
    """
    Represented by "+" in a GFF file; the strand is positive with relation to the landmark.
    """
    unknown = "unknown"
    """
    Represented by "?" in a GFF file. The strandedness is relevant but unknown.
    """
    unstranded = "unstranded"
    """
    Represented by "." in a GFF file; the feature is not stranded.
    """


class Table(ConfiguredBaseModel):
    """
    root class for all schema entities
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"abstract": True, "from_schema": "http://kbase.github.io/cdm-schema/cdm_base", "tree_root": True}
    )

    pass


class Association(Table):
    """
    An association between an object--typically an entity such as a protein or a feature--and a classification system or ontology, such as the Gene Ontology, the Enzyme Classification, or TIGRFAMS domains.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": [
                "annotation",
                "functional annotation",
                "gene annotation",
                "structural annotation",
                "protein annotation",
            ],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {
                "association_id": {"identifier": True, "name": "association_id"},
                "object": {
                    "description": "The object of an association. "
                    "Should be an ontology term or "
                    "database cross-reference.",
                    "name": "object",
                    "range": "local_curie",
                    "required": True,
                },
                "predicate": {
                    "description": "The relationship between subject "
                    "and object in an association. "
                    "Should be a term from the "
                    "Relation Ontology.",
                    "name": "predicate",
                    "range": "local_curie",
                },
                "subject": {
                    "any_of": [{"range": "Feature"}, {"range": "Protein"}, {"range": "ContigCollection"}],
                    "description": "The subject of an association.",
                    "name": "subject",
                    "range": "Any",
                    "required": True,
                },
            },
        }
    )

    association_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an association.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "association_id",
                "domain_of": ["Association", "Association_X_Publication", "Association_X_SupportingObject"],
            }
        },
    )
    subject: str = Field(
        default=...,
        description="""The subject of an association.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "subject",
                "aliases": ["about", "source", "head", "subject_id"],
                "any_of": [{"range": "Feature"}, {"range": "Protein"}, {"range": "ContigCollection"}],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:subject",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )
    object: str = Field(
        default=...,
        description="""The object of an association. Should be an ontology term or database cross-reference.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "object",
                "aliases": ["target", "sink", "tail", "object_id"],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:object",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )
    predicate: Optional[str] = Field(
        default=None,
        description="""The relationship between subject and object in an association. Should be a term from the Relation Ontology.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "predicate",
                "aliases": ["relationship", "relationship type", "property", "predicate_id"],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:predicate",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )
    negated: Optional[bool] = Field(
        default=None,
        description="""If true, the relationship between the subject and object is negated. For example, consider an association where the subject is a protein ID, the object is the GO term for \"glucose biosynthesis\", and the predicate is \"involved in\". With the \"negated\" field set to false, the association is interpreted as \"<protein ID> is involved in glucose biosynthesis\". With the \"negated\" field set to true, the association is interpreted as \"<protein ID> is not involved in glucose biosynthesis\".""",
        json_schema_extra={"linkml_meta": {"alias": "negated", "domain_of": ["Association"]}},
    )
    evidence_type: Optional[str] = Field(
        default=None,
        description="""The type of evidence supporting the association. Should be a term from the Evidence and Conclusion Ontology (ECO).""",
        json_schema_extra={"linkml_meta": {"alias": "evidence_type", "domain_of": ["Association"]}},
    )
    primary_knowledge_source: Optional[str] = Field(
        default=None,
        description="""The knowledge source that created the association. Should be a UUID from the DataSource table.""",
        json_schema_extra={"linkml_meta": {"alias": "primary_knowledge_source", "domain_of": ["Association"]}},
    )
    aggregator_knowledge_source: Optional[str] = Field(
        default=None,
        description="""The knowledge source that aggregated the association. Should be a UUID from the DataSource table.""",
        json_schema_extra={"linkml_meta": {"alias": "aggregator_knowledge_source", "domain_of": ["Association"]}},
    )
    annotation_date: Optional[str] = Field(
        default=None,
        description="""The date when the annotation was made.""",
        json_schema_extra={"linkml_meta": {"alias": "annotation_date", "domain_of": ["Association"]}},
    )
    comments: Optional[str] = Field(
        default=None,
        description="""Any comments about the association.""",
        json_schema_extra={"linkml_meta": {"alias": "comments", "domain_of": ["Association", "DataSource"]}},
    )

    @field_validator("evidence_type")
    def pattern_evidence_type(cls, v):
        pattern = re.compile(r"^ECO:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid evidence_type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid evidence_type format: {v}"
            raise ValueError(err_msg)
        return v


class Cluster(Table):
    """
    Represents an individual execution of a clustering protocol. See the ClusterMember class for clustering results.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"cluster_id": {"identifier": True, "name": "cluster_id"}},
        }
    )

    cluster_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a cluster.""",
        json_schema_extra={"linkml_meta": {"alias": "cluster_id", "domain_of": ["Cluster", "ClusterMember"]}},
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief textual definition or description.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""Name of the cluster, if available.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Cluster", "Contributor", "DataSource", "Event", "Experiment", "Name"],
            }
        },
    )
    entity_type: ClusterType = Field(
        default=...,
        description="""Type of entity being clustered.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_type",
                "domain_of": ["Cluster", "Entity"],
                "todos": ["This should be an enum: Protein, Feature, strain/species/other?"],
            }
        },
    )
    protocol_id: Optional[str] = Field(
        default=None,
        description="""Protocol used to generate the cluster.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protocol_id",
                "domain_of": ["Cluster", "Feature", "Protocol", "Measurement", "Protocol_X_ProtocolParticipant"],
            }
        },
    )


class ClusterMember(Table):
    """
    Relationship representing membership of a cluster. An optional score can be assigned to each cluster member.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "http://kbase.github.io/cdm-schema/cdm_components"})

    cluster_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a cluster.""",
        json_schema_extra={"linkml_meta": {"alias": "cluster_id", "domain_of": ["Cluster", "ClusterMember"]}},
    )
    entity_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    is_representative: Optional[bool] = Field(
        default=False,
        description="""Whether or not this member is the representative for the cluster. If 'is_representative' is false, it is assumed that this is a cluster member.""",
        json_schema_extra={
            "linkml_meta": {"alias": "is_representative", "domain_of": ["ClusterMember"], "ifabsent": "false"}
        },
    )
    is_seed: Optional[bool] = Field(
        default=False,
        description="""Whether or not this is the seed for this cluster.""",
        json_schema_extra={"linkml_meta": {"alias": "is_seed", "domain_of": ["ClusterMember"], "ifabsent": "false"}},
    )
    score: Optional[float] = Field(
        default=None,
        description="""Output from the clustering protocol indicating how closely a member matches the representative.""",
        json_schema_extra={"linkml_meta": {"alias": "score", "domain_of": ["ClusterMember"]}},
    )


class Contig(Table):
    """
    A contig (derived from the word \"contiguous\") is a set of DNA segments or sequences that overlap in a way that provides a contiguous representation of a genomic region. A contig should not contain any gaps.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"contig_id": {"identifier": True, "name": "contig_id"}},
        }
    )

    contig_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_id",
                "domain_of": [
                    "Contig",
                    "Contig_X_ContigCollection",
                    "Contig_X_EncodedFeature",
                    "Contig_X_Feature",
                    "Contig_X_Protein",
                ],
            }
        },
    )
    hash: Optional[str] = Field(
        default=None,
        description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "hash",
                "domain_of": ["Contig", "ContigCollection", "EncodedFeature", "Feature", "Protein"],
            }
        },
    )
    gc_content: Optional[float] = Field(
        default=None,
        description="""GC content of the contig, expressed as a percentage.""",
        json_schema_extra={"linkml_meta": {"alias": "gc_content", "domain_of": ["Contig"]}},
    )
    length: Optional[int] = Field(
        default=None,
        description="""Length of the contig in bp.""",
        json_schema_extra={"linkml_meta": {"alias": "length", "domain_of": ["Contig", "Protein", "Sequence"]}},
    )


class ContigCollection(Table):
    """
    A set of individual, overlapping contigs that represent the complete sequenced genome of an organism.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": ["genome", "biological subject", "assembly", "contig collection", "contig set"],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"contig_collection_id": {"identifier": True, "name": "contig_collection_id"}},
        }
    )

    contig_collection_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig collection.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_collection_id",
                "domain_of": [
                    "ContigCollection",
                    "Contig_X_ContigCollection",
                    "ContigCollection_X_EncodedFeature",
                    "ContigCollection_X_Feature",
                    "ContigCollection_X_Protein",
                ],
            }
        },
    )
    hash: Optional[str] = Field(
        default=None,
        description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "hash",
                "domain_of": ["Contig", "ContigCollection", "EncodedFeature", "Feature", "Protein"],
            }
        },
    )
    asm_score: Optional[float] = Field(
        default=None,
        description="""A composite score for comparing contig collection quality""",
        json_schema_extra={"linkml_meta": {"alias": "asm_score", "domain_of": ["ContigCollection"]}},
    )
    checkm2_completeness: Optional[float] = Field(
        default=None,
        description="""Estimate of the completeness of a contig collection (MAG or genome), estimated by CheckM2 tool""",
        json_schema_extra={"linkml_meta": {"alias": "checkm2_completeness", "domain_of": ["ContigCollection"]}},
    )
    checkm2_contamination: Optional[float] = Field(
        default=None,
        description="""Estimate of the contamination of a contig collection (MAG or genome), estimated by CheckM2 tool""",
        json_schema_extra={"linkml_meta": {"alias": "checkm2_contamination", "domain_of": ["ContigCollection"]}},
    )
    contig_bp: Optional[int] = Field(
        default=None,
        description="""Total size in bp of all contigs""",
        json_schema_extra={"linkml_meta": {"alias": "contig_bp", "domain_of": ["ContigCollection"]}},
    )
    contig_collection_type: Optional[ContigCollectionType] = Field(
        default=None,
        description="""The type of contig collection.""",
        json_schema_extra={"linkml_meta": {"alias": "contig_collection_type", "domain_of": ["ContigCollection"]}},
    )
    ctg_L50: Optional[int] = Field(
        default=None,
        description="""Given a set of contigs, the L50 is defined as the sequence length of the shortest contig at 50% of the total contig collection length""",
        json_schema_extra={"linkml_meta": {"alias": "ctg_L50", "domain_of": ["ContigCollection"]}},
    )
    ctg_L90: Optional[int] = Field(
        default=None,
        description="""The L90 statistic is less than or equal to the L50 statistic; it is the length for which the collection of all contigs of that length or longer contains at least 90% of the sum of the lengths of all contigs""",
        json_schema_extra={"linkml_meta": {"alias": "ctg_L90", "domain_of": ["ContigCollection"]}},
    )
    ctg_N50: Optional[int] = Field(
        default=None,
        description="""Given a set of contigs, each with its own length, the N50 count is defined as the smallest number_of_contigs whose length sum makes up half of contig collection size""",
        json_schema_extra={"linkml_meta": {"alias": "ctg_N50", "domain_of": ["ContigCollection"]}},
    )
    ctg_N90: Optional[int] = Field(
        default=None,
        description="""Given a set of contigs, each with its own length, the N90 count is defined as the smallest number of contigs whose length sum makes up 90% of contig collection size""",
        json_schema_extra={"linkml_meta": {"alias": "ctg_N90", "domain_of": ["ContigCollection"]}},
    )
    ctg_logsum: Optional[float] = Field(
        default=None,
        description="""The sum of the (length*log(length)) of all contigs, times some constant.""",
        json_schema_extra={"linkml_meta": {"alias": "ctg_logsum", "domain_of": ["ContigCollection"]}},
    )
    ctg_max: Optional[int] = Field(
        default=None,
        description="""Maximum contig length""",
        json_schema_extra={"linkml_meta": {"alias": "ctg_max", "domain_of": ["ContigCollection"]}},
    )
    ctg_powsum: Optional[float] = Field(
        default=None,
        description="""Powersum of all contigs is the same as logsum except that it uses the sum of (length*(length^P)) for some power P (default P=0.25)""",
        json_schema_extra={"linkml_meta": {"alias": "ctg_powsum", "domain_of": ["ContigCollection"]}},
    )
    gap_pct: Optional[float] = Field(
        default=None,
        description="""The gap size percentage of all scaffolds""",
        json_schema_extra={"linkml_meta": {"alias": "gap_pct", "domain_of": ["ContigCollection"]}},
    )
    gc_avg: Optional[float] = Field(
        default=None,
        description="""The average GC content of the contig collection, expressed as a percentage""",
        json_schema_extra={"linkml_meta": {"alias": "gc_avg", "domain_of": ["ContigCollection"]}},
    )
    gc_std: Optional[float] = Field(
        default=None,
        description="""The standard deviation of GC content across the contig collection""",
        json_schema_extra={"linkml_meta": {"alias": "gc_std", "domain_of": ["ContigCollection"]}},
    )
    n_contigs: Optional[int] = Field(
        default=None,
        description="""Total number of contigs""",
        json_schema_extra={"linkml_meta": {"alias": "n_contigs", "domain_of": ["ContigCollection"]}},
    )
    n_scaffolds: Optional[int] = Field(
        default=None,
        description="""Total number of scaffolds""",
        json_schema_extra={"linkml_meta": {"alias": "n_scaffolds", "domain_of": ["ContigCollection"]}},
    )
    scaf_L50: Optional[int] = Field(
        default=None,
        description="""Given a set of scaffolds, the L50 is defined as the sequence length of the shortest scaffold at 50% of the total contig collection length""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_L50", "domain_of": ["ContigCollection"]}},
    )
    scaf_L90: Optional[int] = Field(
        default=None,
        description="""The L90 statistic is less than or equal to the L50 statistic; it is the length for which the collection of all scaffolds of that length or longer contains at least 90% of the sum of the lengths of all scaffolds.""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_L90", "domain_of": ["ContigCollection"]}},
    )
    scaf_N50: Optional[int] = Field(
        default=None,
        description="""Given a set of scaffolds, each with its own length, the N50 count is defined as the smallest number of scaffolds whose length sum makes up half of contig collection size""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_N50", "domain_of": ["ContigCollection"]}},
    )
    scaf_N90: Optional[int] = Field(
        default=None,
        description="""Given a set of scaffolds, each with its own length, the N90 count is defined as the smallest number of scaffolds whose length sum makes up 90% of contig collection size""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_N90", "domain_of": ["ContigCollection"]}},
    )
    scaf_bp: Optional[int] = Field(
        default=None,
        description="""Total size in bp of all scaffolds""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_bp", "domain_of": ["ContigCollection"]}},
    )
    scaf_l_gt50k: Optional[int] = Field(
        default=None,
        description="""The total length of scaffolds longer than 50,000 base pairs""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_l_gt50k", "domain_of": ["ContigCollection"]}},
    )
    scaf_logsum: Optional[float] = Field(
        default=None,
        description="""The sum of the (length*log(length)) of all scaffolds, times some constant. Increase the contiguity, the score will increase""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_logsum", "domain_of": ["ContigCollection"]}},
    )
    scaf_max: Optional[int] = Field(
        default=None,
        description="""Maximum scaffold length""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_max", "domain_of": ["ContigCollection"]}},
    )
    scaf_n_gt50K: Optional[int] = Field(
        default=None,
        description="""The number of scaffolds longer than 50,000 base pairs.""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_n_gt50K", "domain_of": ["ContigCollection"]}},
    )
    scaf_pct_gt50K: Optional[float] = Field(
        default=None,
        description="""The percentage of the total assembly length represented by scaffolds longer than 50,000 base pairs""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_pct_gt50K", "domain_of": ["ContigCollection"]}},
    )
    scaf_powsum: Optional[float] = Field(
        default=None,
        description="""Powersum of all scaffolds is the same as logsum except that it uses the sum of (length*(length^P)) for some power P (default P=0.25).""",
        json_schema_extra={"linkml_meta": {"alias": "scaf_powsum", "domain_of": ["ContigCollection"]}},
    )


class Contributor(Table):
    """
    Represents a contributor to the resource.

    Contributors must have a 'contributor_type', either 'Person' or 'Organization', and
    one of the 'name' fields: either 'given_name' and 'family_name' (for a person), or 'name' (for an organization or a person).

    The 'contributor_role' field takes values from the DataCite and CRediT contributor
    roles vocabularies. For more information on these resources and choosing
    appropriate roles, please see the following links:

    DataCite contributor roles: https://support.datacite.org/docs/datacite-metadata-schema-v44-recommended-and-optional-properties#7a-contributortype

    CRediT contributor role taxonomy: https://credit.niso.org

    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "any_of": [
                {
                    "slot_conditions": {
                        "family_name": {"name": "family_name", "required": True},
                        "given_name": {"name": "given_name", "required": True},
                    }
                },
                {"slot_conditions": {"name": {"name": "name", "required": True}}},
            ],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"contributor_id": {"identifier": True, "name": "contributor_id"}},
        }
    )

    contributor_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contributor.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contributor_id",
                "domain_of": ["Contributor", "Contributor_X_Role_X_Experiment", "Contributor_X_Role_X_Project"],
            }
        },
    )
    contributor_type: Optional[ContributorType] = Field(
        default=None,
        description="""Must be either 'Person' or 'Organization'.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contributor_type",
                "domain_of": ["Contributor"],
                "exact_mappings": [
                    "DataCite:attributes.contributors.name_type",
                    "DataCite:attributes.creators.name_type",
                ],
                "examples": [{"value": "Person"}, {"value": "Organization"}],
                "slot_uri": "schema:@type",
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""Contributor name. For organizations, this should be the full (unabbreviated) name; can also be used for a person if the given name/family name format is not applicable.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "close_mappings": ["OSTI.ARTICLE:author", "OSTI.ARTICLE:contributor"],
                "domain_of": ["Cluster", "Contributor", "DataSource", "Event", "Experiment", "Name"],
                "exact_mappings": ["JGI:organisms.pi.name", "ORCID:name"],
                "examples": [
                    {"value": "National Institute of Mental Health"},
                    {"value": "Madonna"},
                    {"value": "Ransome the Clown"},
                ],
                "related_mappings": ["DataCite:attributes.creators.name", "DataCite:attributes.contributors.name"],
                "slot_uri": "schema:name",
            }
        },
    )
    given_name: Optional[str] = Field(
        default=None,
        description="""The given name(s) of the contributor.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "given_name",
                "domain_of": ["Contributor"],
                "examples": [{"value": "Marionetta Cecille de la"}, {"value": "Helena"}, {"value": "Hubert George"}],
                "related_mappings": [
                    "DataCite:attributes.contributors.givenName",
                    "DataCite:attributes.creators.givenName",
                ],
            }
        },
    )
    family_name: Optional[str] = Field(
        default=None,
        description="""The family name(s) of the contributor.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "family_name",
                "domain_of": ["Contributor"],
                "examples": [{"value": "Carte-Postale"}, {"value": "Bonham Carter"}, {"value": "Wells"}],
                "related_mappings": [
                    "DataCite:attributes.contributors.familyName",
                    "DataCite:attributes.creators.familyName",
                ],
            }
        },
    )


class DataSource(Table):
    """
    The source dataset from which data within the CDM was extracted. This might be an API query; a set of files downloaded from a website or uploaded by a user; a database dump; etc. A given data source should have either version information (e.g. UniProt's release number) or an access date to allow the original raw data dump to be recapitulated.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {
                "data_source_id": {"identifier": True, "name": "data_source_id"},
                "name": {
                    "description": "The name of the data source.",
                    "examples": [{"value": "UniProt"}, {"value": "NMDC Runtime API"}],
                    "name": "name",
                },
            },
        }
    )

    data_source_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a data source.""",
        json_schema_extra={"linkml_meta": {"alias": "data_source_id", "domain_of": ["DataSource", "Entity"]}},
    )
    name: Optional[str] = Field(
        default=None,
        description="""The name of the data source.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Cluster", "Contributor", "DataSource", "Event", "Experiment", "Name"],
                "examples": [{"value": "UniProt"}, {"value": "NMDC Runtime API"}],
                "slot_uri": "schema:name",
            }
        },
    )
    comments: Optional[str] = Field(
        default=None,
        description="""Additional details about the dataset.""",
        json_schema_extra={"linkml_meta": {"alias": "comments", "domain_of": ["Association", "DataSource"]}},
    )
    date_accessed: Optional[str] = Field(
        default=None,
        description="""The date when the data was downloaded from the data source.""",
        json_schema_extra={"linkml_meta": {"alias": "date_accessed", "domain_of": ["DataSource"]}},
    )
    url: Optional[str] = Field(
        default=None,
        description="""The URL from which the data was loaded.""",
        json_schema_extra={"linkml_meta": {"alias": "url", "domain_of": ["DataSource", "Protocol"]}},
    )
    version: Optional[str] = Field(
        default=None,
        description="""For versioned data sources, the version of the dataset.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "version",
                "domain_of": ["DataSource", "Protocol"],
                "examples": [{"value": "115"}, {"value": "v1.5.3"}],
            }
        },
    )


class EncodedFeature(Table):
    """
    An entity generated from a feature, such as a transcript.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"encoded_feature_id": {"identifier": True, "name": "encoded_feature_id"}},
        }
    )

    encoded_feature_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an encoded feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "encoded_feature_id",
                "domain_of": [
                    "EncodedFeature",
                    "Contig_X_EncodedFeature",
                    "ContigCollection_X_EncodedFeature",
                    "EncodedFeature_X_Feature",
                ],
            }
        },
    )
    hash: Optional[str] = Field(
        default=None,
        description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "hash",
                "domain_of": ["Contig", "ContigCollection", "EncodedFeature", "Feature", "Protein"],
            }
        },
    )
    has_stop_codon: Optional[bool] = Field(
        default=None,
        description="""Captures whether or not the sequence includes stop coordinates.""",
        json_schema_extra={"linkml_meta": {"alias": "has_stop_codon", "domain_of": ["EncodedFeature"]}},
    )
    type: Optional[str] = Field(
        default=None,
        description="""The type of the entity. Should be a term from the sequence ontology.""",
        json_schema_extra={
            "linkml_meta": {"alias": "type", "domain_of": ["EncodedFeature", "Feature", "Sample", "Sequence"]}
        },
    )

    @field_validator("type")
    def pattern_type(cls, v):
        pattern = re.compile(r"^SO:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid type format: {v}"
            raise ValueError(err_msg)
        return v


class GoldEnvironmentalContext(Table):
    """
    Environmental context, described using JGI's five level system.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {
                "gold_environmental_context_id": {"identifier": True, "name": "gold_environmental_context_id"}
            },
        }
    )

    gold_environmental_context_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a GOLD environmental context.""",
        json_schema_extra={
            "linkml_meta": {"alias": "gold_environmental_context_id", "domain_of": ["GoldEnvironmentalContext"]}
        },
    )
    ecosystem: Optional[str] = Field(
        default=None,
        description="""JGI GOLD descriptor representing the top level ecosystem categorization.""",
        json_schema_extra={"linkml_meta": {"alias": "ecosystem", "domain_of": ["GoldEnvironmentalContext"]}},
    )
    ecosystem_category: Optional[str] = Field(
        default=None,
        description="""JGI GOLD descriptor representing the ecosystem category.""",
        json_schema_extra={"linkml_meta": {"alias": "ecosystem_category", "domain_of": ["GoldEnvironmentalContext"]}},
    )
    ecosystem_subtype: Optional[str] = Field(
        default=None,
        description="""JGI GOLD descriptor representing the subtype of ecosystem. May be \"Unclassified\".""",
        json_schema_extra={"linkml_meta": {"alias": "ecosystem_subtype", "domain_of": ["GoldEnvironmentalContext"]}},
    )
    ecosystem_type: Optional[str] = Field(
        default=None,
        description="""JGI GOLD descriptor representing the ecosystem type. May be \"Unclassified\".""",
        json_schema_extra={"linkml_meta": {"alias": "ecosystem_type", "domain_of": ["GoldEnvironmentalContext"]}},
    )
    specific_ecosystem: Optional[str] = Field(
        default=None,
        description="""JGI GOLD descriptor representing the most specific level of ecosystem categorization. May be \"Unclassified\".""",
        json_schema_extra={"linkml_meta": {"alias": "specific_ecosystem", "domain_of": ["GoldEnvironmentalContext"]}},
    )


class MixsEnvironmentalContext(Table):
    """
    Environmental context, described using the MiXS convention of broad and local environment, plus the medium.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {
                "mixs_environmental_context_id": {"identifier": True, "name": "mixs_environmental_context_id"}
            },
        }
    )

    mixs_environmental_context_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a mixs environmental context.""",
        json_schema_extra={
            "linkml_meta": {"alias": "mixs_environmental_context_id", "domain_of": ["MixsEnvironmentalContext"]}
        },
    )
    env_broad_scale: Optional[str] = Field(
        default=None,
        title="broad-scale environmental context",
        description="""Report the major environmental system the sample or specimen came from. The system(s) identified should have a coarse spatial grain, to provide the general environmental context of where the sampling was done (e.g. in the desert or a rainforest). We recommend using subclasses of EnvO's biome class: http://purl.obolibrary.org/obo/ENVO_00000428. EnvO documentation about how to use the field: https://github.com/EnvironmentOntology/envo/wiki/Using-ENVO-with-MIxS""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "env_broad_scale",
                "aliases": ["broad-scale environmental context"],
                "annotations": {
                    "expected_value": {
                        "tag": "expected_value",
                        "value": "The major environment type(s) "
                        "where the sample was collected. "
                        "Recommend subclasses of biome "
                        "[ENVO:00000428]. Multiple terms "
                        "can be separated by one or more "
                        "pipes.",
                    },
                    "tooltip": {
                        "tag": "tooltip",
                        "value": "The biome or major environmental system "
                        "where the sample or specimen "
                        "originated. Choose values from "
                        "subclasses of the 'biome' class "
                        "[ENVO:00000428] in the Environment "
                        "Ontology (ENVO). For host-associated or "
                        "plant-associated samples, use terms "
                        "from the UBERON or Plant Ontology to "
                        "describe the broad anatomical or "
                        "morphological context",
                    },
                },
                "domain_of": ["MixsEnvironmentalContext"],
                "examples": [
                    {
                        "value": "oceanic epipelagic zone biome [ENVO:01000033] for "
                        "annotating a water sample from the photic zone in "
                        "middle of the Atlantic Ocean"
                    }
                ],
                "slot_uri": "mixs:0000012",
                "string_serialization": "{termLabel} {[termID]}",
            }
        },
    )
    env_local_scale: Optional[str] = Field(
        default=None,
        title="local environmental context",
        description="""Report the entity or entities which are in the sample or specimen's local vicinity and which you believe have significant causal influences on your sample or specimen. We recommend using EnvO terms which are of smaller spatial grain than your entry for env_broad_scale. Terms, such as anatomical sites, from other OBO Library ontologies which interoperate with EnvO (e.g. UBERON) are accepted in this field. EnvO documentation about how to use the field: https://github.com/EnvironmentOntology/envo/wiki/Using-ENVO-with-MIxS.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "env_local_scale",
                "aliases": ["local environmental context"],
                "annotations": {
                    "expected_value": {
                        "tag": "expected_value",
                        "value": "Environmental entities having causal influences upon the entity at time of sampling.",
                    },
                    "tooltip": {
                        "tag": "tooltip",
                        "value": "The specific environmental  entities or "
                        "features near the sample or specimen "
                        "that significantly influence its "
                        "characteristics or composition. These "
                        "entities are typically smaller in scale "
                        "than the broad environmental context. "
                        "Values for this field should be "
                        "countable, material nouns and must be "
                        "chosen from subclasses of BFO:0000040 "
                        "(material entity) that appear in the "
                        "Environment Ontology (ENVO). For "
                        "host-associated or plant-associated "
                        "samples, use terms from the UBERON or "
                        "Plant Ontology to describe specific "
                        "anatomical structures or plant parts.",
                    },
                },
                "domain_of": ["MixsEnvironmentalContext"],
                "examples": [
                    {
                        "value": "litter layer [ENVO:01000338]; Annotating a pooled "
                        "sample taken from various vegetation layers in a "
                        "forest consider: canopy [ENVO:00000047]|herb and fern "
                        "layer [ENVO:01000337]|litter layer "
                        "[ENVO:01000338]|understory [01000335]|shrub layer "
                        "[ENVO:01000336]."
                    }
                ],
                "slot_uri": "mixs:0000013",
                "string_serialization": "{termLabel} {[termID]}",
            }
        },
    )
    env_medium: Optional[str] = Field(
        default=None,
        title="environmental medium",
        description="""Report the environmental material(s) immediately surrounding the sample or specimen at the time of sampling. We recommend using subclasses of 'environmental material' (http://purl.obolibrary.org/obo/ENVO_00010483). EnvO documentation about how to use the field: https://github.com/EnvironmentOntology/envo/wiki/Using-ENVO-with-MIxS . Terms from other OBO ontologies are permissible as long as they reference mass/volume nouns (e.g. air, water, blood) and not discrete, countable entities (e.g. a tree, a leaf, a table top).""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "env_medium",
                "aliases": ["environmental medium"],
                "annotations": {
                    "expected_value": {
                        "tag": "expected_value",
                        "value": "The material displaced by the "
                        "entity at time of sampling. "
                        "Recommend subclasses of "
                        "environmental material "
                        "[ENVO:00010483].",
                    },
                    "tooltip": {
                        "tag": "tooltip",
                        "value": "The predominant environmental material "
                        "or substrate that directly surrounds or "
                        "hosts the sample or specimen at the "
                        "time of sampling. Choose values from "
                        "subclasses of the 'environmental "
                        "material' class [ENVO:00010483] in the "
                        "Environment Ontology (ENVO). Values for "
                        "this field should be measurable or mass "
                        "material nouns, representing continuous "
                        "environmental materials. For "
                        "host-associated or plant-associated "
                        "samples, use terms from the UBERON or "
                        "Plant Ontology to indicate a tissue, "
                        "organ, or plant structure",
                    },
                },
                "domain_of": ["MixsEnvironmentalContext"],
                "examples": [
                    {
                        "value": "soil [ENVO:00001998]; Annotating a fish swimming in "
                        "the upper 100 m of the Atlantic Ocean, consider: "
                        "ocean water [ENVO:00002151]. Example: Annotating a "
                        "duck on a pond consider: pond water "
                        "[ENVO:00002228]|air [ENVO_00002005]"
                    }
                ],
                "slot_uri": "mixs:0000014",
                "string_serialization": "{termLabel} {[termID]}",
            }
        },
    )


class Event(Table):
    """
    Something that happened.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"event_id": {"identifier": True, "name": "event_id"}},
        }
    )

    event_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an event.""",
        json_schema_extra={"linkml_meta": {"alias": "event_id", "domain_of": ["Event"]}},
    )
    created_at: Optional[str] = Field(
        default=None,
        description="""The time at which the event started or was created.""",
        json_schema_extra={"linkml_meta": {"alias": "created_at", "domain_of": ["Event", "Experiment", "Measurement"]}},
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief text description of what actually happened.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
                "todos": ["Create controlled vocab for events?"],
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""Name or title for the event.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Cluster", "Contributor", "DataSource", "Event", "Experiment", "Name"],
            }
        },
    )
    location: Optional[str] = Field(
        default=None,
        description="""The location for this event. May be described in terms of coordinates.""",
        json_schema_extra={"linkml_meta": {"alias": "location", "domain_of": ["Event"]}},
    )


class Experiment(Table):
    """
    A discrete scientific procedure undertaken to make a discovery, test a hypothesis, or demonstrate a known fact.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"experiment_id": {"identifier": True, "name": "experiment_id"}},
        }
    )

    experiment_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an experiment.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "experiment_id",
                "domain_of": [
                    "Experiment",
                    "Contributor_X_Role_X_Experiment",
                    "Experiment_X_Project",
                    "Experiment_X_Sample",
                ],
            }
        },
    )
    created_at: Optional[str] = Field(
        default=None,
        description="""The start time of the experiment.""",
        json_schema_extra={"linkml_meta": {"alias": "created_at", "domain_of": ["Event", "Experiment", "Measurement"]}},
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief explanation of what was done.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
            }
        },
    )
    name: Optional[str] = Field(
        default=None,
        description="""Name or title of the experiment.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Cluster", "Contributor", "DataSource", "Event", "Experiment", "Name"],
            }
        },
    )


class Feature(Table):
    """
    A feature localized to an interval along a contig.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "comments": ["corresponds to an entry in GFF3"],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "see_also": ["https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md"],
            "slot_usage": {"feature_id": {"identifier": True, "name": "feature_id"}},
        }
    )

    feature_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "feature_id",
                "domain_of": [
                    "Feature",
                    "Contig_X_Feature",
                    "ContigCollection_X_Feature",
                    "EncodedFeature_X_Feature",
                    "Feature_X_Protein",
                ],
            }
        },
    )
    hash: Optional[str] = Field(
        default=None,
        description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "hash",
                "domain_of": ["Contig", "ContigCollection", "EncodedFeature", "Feature", "Protein"],
            }
        },
    )
    cds_phase: Optional[CdsPhaseType] = Field(
        default=None,
        description="""For features of type CDS, the phase indicates where the next codon begins relative to the 5' end (where the 5' end of the CDS is relative to the strand of the CDS feature) of the current CDS feature. cds_phase is required if the feature type is CDS.""",
        json_schema_extra={"linkml_meta": {"alias": "cds_phase", "domain_of": ["Feature"]}},
    )
    e_value: Optional[float] = Field(
        default=None,
        description="""The 'score' of the feature. The semantics of this field are ill-defined. E-values should be used for sequence similarity features.""",
        json_schema_extra={"linkml_meta": {"alias": "e_value", "domain_of": ["Feature"]}},
    )
    end: Optional[int] = Field(
        default=None,
        description="""The start and end coordinates of the feature are given in positive 1-based int coordinates, relative to the landmark given in column one. Start is always less than or equal to end. For features that cross the origin of a circular feature (e.g. most bacterial genomes, plasmids, and some viral genomes), the requirement for start to be less than or equal to end is satisfied by making end = the position of the end + the length of the landmark feature. For zero-length features, such as insertion sites, start equals end and the implied site is to the right of the indicated base in the direction of the landmark.""",
        json_schema_extra={"linkml_meta": {"alias": "end", "domain_of": ["Feature"]}},
    )
    p_value: Optional[float] = Field(
        default=None,
        description="""The 'score' of the feature. The semantics of this field are ill-defined. P-values should be used for ab initio gene prediction features.""",
        json_schema_extra={"linkml_meta": {"alias": "p_value", "domain_of": ["Feature"]}},
    )
    start: Optional[int] = Field(
        default=None,
        description="""The start and end coordinates of the feature are given in positive 1-based int coordinates, relative to the landmark given in column one. Start is always less than or equal to end. For features that cross the origin of a circular feature (e.g. most bacterial genomes, plasmids, and some viral genomes), the requirement for start to be less than or equal to end is satisfied by making end = the position of the end + the length of the landmark feature. For zero-length features, such as insertion sites, start equals end and the implied site is to the right of the indicated base in the direction of the landmark.""",
        json_schema_extra={"linkml_meta": {"alias": "start", "domain_of": ["Feature"]}},
    )
    strand: Optional[StrandType] = Field(
        default=None,
        description="""The strand of the feature.""",
        json_schema_extra={"linkml_meta": {"alias": "strand", "domain_of": ["Feature"]}},
    )
    source_database: Optional[str] = Field(
        default=None,
        description="""ID of the data source from which this entity came.""",
        json_schema_extra={"linkml_meta": {"alias": "source_database", "domain_of": ["Feature"]}},
    )
    protocol_id: Optional[str] = Field(
        default=None,
        description="""ID of the protocol used to generate the feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protocol_id",
                "aliases": ["generated by"],
                "domain_of": ["Cluster", "Feature", "Protocol", "Measurement", "Protocol_X_ProtocolParticipant"],
            }
        },
    )
    type: Optional[str] = Field(
        default=None,
        description="""The type of the feature; constrained to be either a term from the Sequence Ontology or an SO accession number. Must be sequence_feature (SO:0000110) or an is_a child of it.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "type",
                "aliases": ["feature type"],
                "domain_of": ["EncodedFeature", "Feature", "Sample", "Sequence"],
            }
        },
    )

    @field_validator("type")
    def pattern_type(cls, v):
        pattern = re.compile(r"^SO:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid type format: {v}"
            raise ValueError(err_msg)
        return v


class Project(Table):
    """
    Administrative unit for collecting data related to a certain topic, location, data type, grant funding, and so on.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": [
                "proposal",
                "research proposal",
                "research study",
                "investigation",
                "project",
                "study",
                "umbrella project",
                "research initiative",
            ],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"project_id": {"identifier": True, "name": "project_id"}},
        }
    )

    project_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a project.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "project_id",
                "domain_of": ["Project", "Contributor_X_Role_X_Project", "Experiment_X_Project"],
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief text description of the project.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
            }
        },
    )


class Protein(Table):
    """
    Proteins are large, complex molecules made up of one or more long, folded chains of amino acids, whose sequences are determined by the DNA sequence of the protein-encoding gene.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"protein_id": {"identifier": True, "name": "protein_id"}},
        }
    )

    protein_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a protein.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protein_id",
                "domain_of": ["Protein", "Contig_X_Protein", "ContigCollection_X_Protein", "Feature_X_Protein"],
            }
        },
    )
    hash: Optional[str] = Field(
        default=None,
        description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "hash",
                "domain_of": ["Contig", "ContigCollection", "EncodedFeature", "Feature", "Protein"],
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief text description of the entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
            }
        },
    )
    evidence_for_existence: Optional[ProteinEvidenceForExistence] = Field(
        default=None,
        description="""The evidence that this protein exists. For example, the protein may have been isolated from a cell, or it may be predicted based on sequence features.""",
        json_schema_extra={"linkml_meta": {"alias": "evidence_for_existence", "domain_of": ["Protein"]}},
    )
    length: Optional[int] = Field(
        default=None,
        description="""The length of the protein.""",
        json_schema_extra={"linkml_meta": {"alias": "length", "domain_of": ["Contig", "Protein", "Sequence"]}},
    )
    sequence: Optional[str] = Field(
        default=None,
        description="""The protein amino acid sequence.""",
        json_schema_extra={"linkml_meta": {"alias": "sequence", "domain_of": ["Protein"]}},
    )


class Protocol(Table):
    """
    Defined method or set of methods.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"protocol_id": {"identifier": True, "name": "protocol_id"}},
        }
    )

    protocol_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a protocol.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protocol_id",
                "domain_of": ["Cluster", "Feature", "Protocol", "Measurement", "Protocol_X_ProtocolParticipant"],
            }
        },
    )
    doi: Optional[str] = Field(
        default=None,
        description="""The DOI for a protocol.""",
        json_schema_extra={"linkml_meta": {"alias": "doi", "domain_of": ["Protocol"]}},
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief text description of the protocol.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
            }
        },
    )
    version: Optional[str] = Field(
        default=None,
        description="""The version of the protocol that has been used.""",
        json_schema_extra={"linkml_meta": {"alias": "version", "domain_of": ["DataSource", "Protocol"]}},
    )
    url: Optional[str] = Field(
        default=None,
        description="""The URL for a protocol.""",
        json_schema_extra={"linkml_meta": {"alias": "url", "domain_of": ["DataSource", "Protocol"]}},
    )


class ProtocolParticipant(Table):
    """
    Either an input or an output of a protocol.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "http://kbase.github.io/cdm-schema/cdm_components", "todos": ["finish this!"]}
    )

    protocol_participant_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protocol_participant_id",
                "domain_of": ["ProtocolParticipant", "Protocol_X_ProtocolParticipant"],
            }
        },
    )


class Publication(Table):
    """
    A publication (e.g. journal article).
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"publication_id": {"identifier": True, "name": "publication_id"}},
        }
    )

    publication_id: str = Field(
        default=...,
        description="""Unique identifier for a publication - e.g. PMID, DOI, URL, etc.""",
        json_schema_extra={
            "linkml_meta": {"alias": "publication_id", "domain_of": ["Publication", "Association_X_Publication"]}
        },
    )


class Sample(Table):
    """
    A material entity that can be characterised by an experiment.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {"sample_id": {"identifier": True, "name": "sample_id"}},
        }
    )

    sample_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a sample.""",
        json_schema_extra={"linkml_meta": {"alias": "sample_id", "domain_of": ["Sample", "Experiment_X_Sample"]}},
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief textual description of the sample.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
            }
        },
    )
    type: Optional[str] = Field(
        default=None,
        description="""The type of entity that the sample is. Vocab TBD.""",
        json_schema_extra={
            "linkml_meta": {"alias": "type", "domain_of": ["EncodedFeature", "Feature", "Sample", "Sequence"]}
        },
    )


class Sequence(Table):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_components",
            "slot_usage": {
                "entity_id": {"description": "The entity to which this sequence belongs.", "name": "entity_id"}
            },
        }
    )

    sequence_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a sequence.""",
        json_schema_extra={"linkml_meta": {"alias": "sequence_id", "domain_of": ["Sequence"]}},
    )
    entity_id: str = Field(
        default=...,
        description="""The entity to which this sequence belongs.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    type: Optional[SequenceType] = Field(
        default=None,
        description="""The type of the sequence, either \"Nucleotide\" or \"Amino Acid\".""",
        json_schema_extra={
            "linkml_meta": {"alias": "type", "domain_of": ["EncodedFeature", "Feature", "Sample", "Sequence"]}
        },
    )
    length: Optional[int] = Field(
        default=None,
        description="""The length of the sequence in base pairs (for nucleotide sequences) or amino acids (for amino acid sequences).""",
        json_schema_extra={"linkml_meta": {"alias": "length", "domain_of": ["Contig", "Protein", "Sequence"]}},
    )
    checksum: Optional[str] = Field(
        default=None,
        description="""The checksum of the sequence, used to verify its integrity.""",
        json_schema_extra={"linkml_meta": {"alias": "checksum", "domain_of": ["Sequence"]}},
    )


class Entity(Table):
    """
    A database entity.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_base",
            "slot_usage": {"entity_id": {"identifier": True, "name": "entity_id"}},
        }
    )

    entity_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    data_source_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a data source.""",
        json_schema_extra={"linkml_meta": {"alias": "data_source_id", "domain_of": ["DataSource", "Entity"]}},
    )
    entity_type: EntityType = Field(
        default=...,
        description="""The class of the entity. Must be a valid CDM class.""",
        json_schema_extra={"linkml_meta": {"alias": "entity_type", "domain_of": ["Cluster", "Entity"]}},
    )
    data_source_entity_id: Optional[str] = Field(
        default=None,
        description="""The primary ID of the entity at the data source.""",
        json_schema_extra={"linkml_meta": {"alias": "data_source_entity_id", "domain_of": ["Entity"]}},
    )
    data_source_created: str = Field(
        default=...,
        description="""Date/timestamp for when the entity was created or added to the data source.""",
        json_schema_extra={"linkml_meta": {"alias": "data_source_created", "domain_of": ["Entity"]}},
    )
    data_source_updated: Optional[str] = Field(
        default=None,
        description="""Date/timestamp for when the entity was updated in the data source.""",
        json_schema_extra={"linkml_meta": {"alias": "data_source_updated", "domain_of": ["Entity"]}},
    )
    created: str = Field(
        default=...,
        description="""Date/timestamp for when the entity was created or added to the CDM.""",
        json_schema_extra={"linkml_meta": {"alias": "created", "domain_of": ["Entity"]}},
    )
    updated: str = Field(
        default=...,
        description="""Date/timestamp for when the entity was updated in the CDM.""",
        json_schema_extra={"linkml_meta": {"alias": "updated", "domain_of": ["Entity"]}},
    )


class Identifier(Table):
    """
    A string used as a resolvable (external) identifier for an entity. This should be a URI or CURIE. If the string cannot be resolved to an URL, it should be added as a 'name' instead.

    This table is used for capturing external IDs. The internal CDM identifier should be used in the *_id field (e.g. feature_id, protein_id, contig_collection_id).

    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_base",
            "slot_usage": {
                "description": {"description": "Brief description of the identifier.", "name": "description"}
            },
        }
    )

    entity_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    identifier: str = Field(
        default=...,
        description="""Fully-qualified URL or CURIE used as an identifier for an entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "identifier",
                "domain_of": ["Identifier"],
                "examples": [{"value": "UniProt:Q8KCD6"}, {"value": "EC:5.2.3.14"}],
                "slot_uri": "schema:identifier",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief description of the identifier.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
            }
        },
    )
    source: Optional[str] = Field(
        default=None,
        description="""The source for a specific piece of information; should be a CDM internal ID of a source in the DataSource table.""",
        json_schema_extra={"linkml_meta": {"alias": "source", "domain_of": ["Identifier", "Name"]}},
    )
    relationship: Optional[str] = Field(
        default=None,
        description="""Relationship between this identifier and the entity in the `entity_id` field.""",
        json_schema_extra={"linkml_meta": {"alias": "relationship", "domain_of": ["Identifier"]}},
    )


class Name(Table):
    """
    A string used as the name or label for an entity. This may be a primary name, alternative name, synonym, acronym, or any other label used to refer to an entity.

    Identifiers that look like CURIEs or database references, but which cannot be resolved using bioregistry or identifiers.org should be added as names.

    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_base",
            "slot_usage": {
                "description": {
                    "description": "Brief description of the name and/or its relationship to the entity.",
                    "examples": [{"value": "UniProt recommended full name"}],
                    "name": "description",
                },
                "name": {
                    "description": "The string used as a name.",
                    "examples": [
                        {"value": "Heat-inducible transcription repressor HrcA"},
                        {"value": "Uncharacterized protein 002R"},
                    ],
                    "name": "name",
                    "required": True,
                    "slot_uri": "schema:name",
                },
            },
        }
    )

    entity_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    name: str = Field(
        default=...,
        description="""The string used as a name.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "name",
                "domain_of": ["Cluster", "Contributor", "DataSource", "Event", "Experiment", "Name"],
                "examples": [
                    {"value": "Heat-inducible transcription repressor HrcA"},
                    {"value": "Uncharacterized protein 002R"},
                ],
                "slot_uri": "schema:name",
            }
        },
    )
    description: Optional[str] = Field(
        default=None,
        description="""Brief description of the name and/or its relationship to the entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "description",
                "domain_of": [
                    "Cluster",
                    "Event",
                    "Experiment",
                    "Project",
                    "Protein",
                    "Protocol",
                    "Sample",
                    "Identifier",
                    "Name",
                ],
                "examples": [{"value": "UniProt recommended full name"}],
            }
        },
    )
    source: Optional[str] = Field(
        default=None,
        description="""The source for a specific piece of information; should be a CDM internal ID of a source in the DataSource table.""",
        json_schema_extra={"linkml_meta": {"alias": "source", "domain_of": ["Identifier", "Name"]}},
    )


class AttributeValue(Table):
    """
    A generic class for capturing tag-value information in a structured form.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "abstract": True,
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_attr_value",
            "slot_usage": {
                "entity_id": {
                    "description": "The database entity (sample, "
                    "feature, protein, etc.) to which "
                    "the attribute-value annotation "
                    "refers.",
                    "name": "entity_id",
                }
            },
        }
    )

    entity_id: str = Field(
        default=...,
        description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    attribute_name: str = Field(
        default=...,
        description="""The attribute being captured in this annotation.""",
        json_schema_extra={
            "linkml_meta": {"alias": "attribute_name", "aliases": ["type", "name"], "domain_of": ["AttributeValue"]}
        },
    )
    attribute_cv_term_id: Optional[str] = Field(
        default=None,
        description="""If the attribute is a term from a controlled vocabulary, the ID of the term.""",
        json_schema_extra={"linkml_meta": {"alias": "attribute_cv_term_id", "domain_of": ["AttributeValue"]}},
    )
    raw_value: Optional[str] = Field(
        default=None,
        description="""Raw value from the source data. May or may not include units or other unstructured information.""",
        json_schema_extra={"linkml_meta": {"alias": "raw_value", "domain_of": ["AttributeValue", "Geolocation"]}},
    )


class QuantityValue(AttributeValue):
    """
    A simple quantity, e.g. 2cm. May be used to describe a range using the minimum_value and maximum_value fields.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"class_uri": "schema:QuantityValue", "from_schema": "http://kbase.github.io/cdm-schema/cdm_attr_value"}
    )

    maximum_value: Optional[float] = Field(
        default=None,
        description="""If the quantity describes a range, represents the upper bound of the range.""",
        json_schema_extra={"linkml_meta": {"alias": "maximum_value", "domain_of": ["QuantityValue"]}},
    )
    minimum_value: Optional[float] = Field(
        default=None,
        description="""If the quantity describes a range, represents the lower bound of the range.""",
        json_schema_extra={"linkml_meta": {"alias": "minimum_value", "domain_of": ["QuantityValue"]}},
    )
    value: Optional[float] = Field(
        default=None,
        description="""The numeric portion of the quantity.""",
        json_schema_extra={
            "linkml_meta": {"alias": "value", "domain_of": ["QuantityValue", "TextValue", "Statements"]}
        },
    )
    unit: Optional[str] = Field(
        default=None,
        description="""The unit of the quantity. Should be a term from UCUM.""",
        json_schema_extra={"linkml_meta": {"alias": "unit", "domain_of": ["QuantityValue"]}},
    )
    entity_id: str = Field(
        default=...,
        description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    attribute_name: str = Field(
        default=...,
        description="""The attribute being captured in this annotation.""",
        json_schema_extra={
            "linkml_meta": {"alias": "attribute_name", "aliases": ["type", "name"], "domain_of": ["AttributeValue"]}
        },
    )
    attribute_cv_term_id: Optional[str] = Field(
        default=None,
        description="""If the attribute is a term from a controlled vocabulary, the ID of the term.""",
        json_schema_extra={"linkml_meta": {"alias": "attribute_cv_term_id", "domain_of": ["AttributeValue"]}},
    )
    raw_value: Optional[str] = Field(
        default=None,
        description="""Raw value from the source data. May or may not include units or other unstructured information.""",
        json_schema_extra={"linkml_meta": {"alias": "raw_value", "domain_of": ["AttributeValue", "Geolocation"]}},
    )


class TextValue(AttributeValue):
    """
    A basic string value
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "http://kbase.github.io/cdm-schema/cdm_attr_value"})

    value: str = Field(
        default=...,
        description="""The value after undergoing normalisation or standardisation.""",
        json_schema_extra={
            "linkml_meta": {"alias": "value", "domain_of": ["QuantityValue", "TextValue", "Statements"]}
        },
    )
    value_cv_term_id: Optional[str] = Field(
        default=None,
        description="""If the term comes from the controlled vocabulary, the CURIE for the term. This will always be null if the text string is not from a controlled vocabulary.""",
        json_schema_extra={"linkml_meta": {"alias": "value_cv_term_id", "domain_of": ["TextValue"]}},
    )
    language: Optional[str] = Field(
        default=None,
        description="""Language of the text value.""",
        json_schema_extra={"linkml_meta": {"alias": "language", "domain_of": ["TextValue", "Statements"]}},
    )
    entity_id: str = Field(
        default=...,
        description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    attribute_name: str = Field(
        default=...,
        description="""The attribute being captured in this annotation.""",
        json_schema_extra={
            "linkml_meta": {"alias": "attribute_name", "aliases": ["type", "name"], "domain_of": ["AttributeValue"]}
        },
    )
    attribute_cv_term_id: Optional[str] = Field(
        default=None,
        description="""If the attribute is a term from a controlled vocabulary, the ID of the term.""",
        json_schema_extra={"linkml_meta": {"alias": "attribute_cv_term_id", "domain_of": ["AttributeValue"]}},
    )
    raw_value: Optional[str] = Field(
        default=None,
        description="""Raw value from the source data. May or may not include units or other unstructured information.""",
        json_schema_extra={"linkml_meta": {"alias": "raw_value", "domain_of": ["AttributeValue", "Geolocation"]}},
    )


class Measurement(QuantityValue):
    """
    A qualitative or quantitative observation of an attribute of an object or event against a standardized scale, to enable it to be compared with other objects or events.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_attr_value",
            "slot_usage": {
                "measurement_id": {"identifier": True, "name": "measurement_id"},
                "protocol_id": {
                    "description": "The ID of the protocol used to generate the measurement.",
                    "name": "protocol_id",
                },
            },
        }
    )

    measurement_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a measurement.""",
        json_schema_extra={
            "linkml_meta": {"alias": "measurement_id", "domain_of": ["Measurement", "Entity_X_Measurement"]}
        },
    )
    protocol_id: str = Field(
        default=...,
        description="""The ID of the protocol used to generate the measurement.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protocol_id",
                "domain_of": ["Cluster", "Feature", "Protocol", "Measurement", "Protocol_X_ProtocolParticipant"],
            }
        },
    )
    created_at: Optional[str] = Field(
        default=None,
        description="""Timestamp for the measurement.""",
        json_schema_extra={"linkml_meta": {"alias": "created_at", "domain_of": ["Event", "Experiment", "Measurement"]}},
    )
    quality: Optional[str] = Field(
        default=None,
        description="""The quality of the measurement, indicating the confidence that one can have in its correctness.""",
        json_schema_extra={
            "linkml_meta": {"alias": "quality", "aliases": ["confidence"], "domain_of": ["Measurement"]}
        },
    )
    maximum_value: Optional[float] = Field(
        default=None,
        description="""If the quantity describes a range, represents the upper bound of the range.""",
        json_schema_extra={"linkml_meta": {"alias": "maximum_value", "domain_of": ["QuantityValue"]}},
    )
    minimum_value: Optional[float] = Field(
        default=None,
        description="""If the quantity describes a range, represents the lower bound of the range.""",
        json_schema_extra={"linkml_meta": {"alias": "minimum_value", "domain_of": ["QuantityValue"]}},
    )
    value: Optional[float] = Field(
        default=None,
        description="""The numeric portion of the quantity.""",
        json_schema_extra={
            "linkml_meta": {"alias": "value", "domain_of": ["QuantityValue", "TextValue", "Statements"]}
        },
    )
    unit: Optional[str] = Field(
        default=None,
        description="""The unit of the quantity. Should be a term from UCUM.""",
        json_schema_extra={"linkml_meta": {"alias": "unit", "domain_of": ["QuantityValue"]}},
    )
    entity_id: str = Field(
        default=...,
        description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    attribute_name: str = Field(
        default=...,
        description="""The attribute being captured in this annotation.""",
        json_schema_extra={
            "linkml_meta": {"alias": "attribute_name", "aliases": ["type", "name"], "domain_of": ["AttributeValue"]}
        },
    )
    attribute_cv_term_id: Optional[str] = Field(
        default=None,
        description="""If the attribute is a term from a controlled vocabulary, the ID of the term.""",
        json_schema_extra={"linkml_meta": {"alias": "attribute_cv_term_id", "domain_of": ["AttributeValue"]}},
    )
    raw_value: Optional[str] = Field(
        default=None,
        description="""Raw value from the source data. May or may not include units or other unstructured information.""",
        json_schema_extra={"linkml_meta": {"alias": "raw_value", "domain_of": ["AttributeValue", "Geolocation"]}},
    )


class ProcessedMeasurement(Measurement):
    """
    A measurement that requires additional processing to generate a result.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({"from_schema": "http://kbase.github.io/cdm-schema/cdm_attr_value"})

    measurement_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a measurement.""",
        json_schema_extra={
            "linkml_meta": {"alias": "measurement_id", "domain_of": ["Measurement", "Entity_X_Measurement"]}
        },
    )
    protocol_id: str = Field(
        default=...,
        description="""The ID of the protocol used to generate the measurement.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protocol_id",
                "domain_of": ["Cluster", "Feature", "Protocol", "Measurement", "Protocol_X_ProtocolParticipant"],
            }
        },
    )
    created_at: Optional[str] = Field(
        default=None,
        description="""Timestamp for the measurement.""",
        json_schema_extra={"linkml_meta": {"alias": "created_at", "domain_of": ["Event", "Experiment", "Measurement"]}},
    )
    quality: Optional[str] = Field(
        default=None,
        description="""The quality of the measurement, indicating the confidence that one can have in its correctness.""",
        json_schema_extra={
            "linkml_meta": {"alias": "quality", "aliases": ["confidence"], "domain_of": ["Measurement"]}
        },
    )
    maximum_value: Optional[float] = Field(
        default=None,
        description="""If the quantity describes a range, represents the upper bound of the range.""",
        json_schema_extra={"linkml_meta": {"alias": "maximum_value", "domain_of": ["QuantityValue"]}},
    )
    minimum_value: Optional[float] = Field(
        default=None,
        description="""If the quantity describes a range, represents the lower bound of the range.""",
        json_schema_extra={"linkml_meta": {"alias": "minimum_value", "domain_of": ["QuantityValue"]}},
    )
    value: Optional[float] = Field(
        default=None,
        description="""The numeric portion of the quantity.""",
        json_schema_extra={
            "linkml_meta": {"alias": "value", "domain_of": ["QuantityValue", "TextValue", "Statements"]}
        },
    )
    unit: Optional[str] = Field(
        default=None,
        description="""The unit of the quantity. Should be a term from UCUM.""",
        json_schema_extra={"linkml_meta": {"alias": "unit", "domain_of": ["QuantityValue"]}},
    )
    entity_id: str = Field(
        default=...,
        description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    attribute_name: str = Field(
        default=...,
        description="""The attribute being captured in this annotation.""",
        json_schema_extra={
            "linkml_meta": {"alias": "attribute_name", "aliases": ["type", "name"], "domain_of": ["AttributeValue"]}
        },
    )
    attribute_cv_term_id: Optional[str] = Field(
        default=None,
        description="""If the attribute is a term from a controlled vocabulary, the ID of the term.""",
        json_schema_extra={"linkml_meta": {"alias": "attribute_cv_term_id", "domain_of": ["AttributeValue"]}},
    )
    raw_value: Optional[str] = Field(
        default=None,
        description="""Raw value from the source data. May or may not include units or other unstructured information.""",
        json_schema_extra={"linkml_meta": {"alias": "raw_value", "domain_of": ["AttributeValue", "Geolocation"]}},
    )


class Prefix(Table):
    """
    Maps CURIEs to URIs
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"class_uri": "sh:PrefixDeclaration", "from_schema": "http://kbase.github.io/cdm-schema/cdm_ontology"}
    )

    prefix: Optional[str] = Field(
        default=None,
        description="""A standardized prefix such as 'GO' or 'rdf' or 'FlyBase'""",
        json_schema_extra={"linkml_meta": {"alias": "prefix", "domain_of": ["Prefix"], "slot_uri": "sh:prefix"}},
    )
    base: Optional[str] = Field(
        default=None,
        description="""The base URI a prefix will expand to""",
        json_schema_extra={"linkml_meta": {"alias": "base", "domain_of": ["Prefix"], "slot_uri": "sh:namespace"}},
    )


class Statements(Table):
    """
    Represents an RDF triple
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "aliases": ["triple"],
            "class_uri": "rdf:Statement",
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_ontology",
        }
    )

    subject: Optional[str] = Field(
        default=None,
        description="""The subject of the statement""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "subject",
                "aliases": ["about", "source", "head", "subject_id"],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:subject",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )
    predicate: Optional[str] = Field(
        default=None,
        description="""The predicate of the statement""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "predicate",
                "aliases": ["relationship", "relationship type", "property", "predicate_id"],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:predicate",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )
    object: Optional[str] = Field(
        default=None,
        description="""Note the range of this slot is always a node. If the triple represents a literal, instead value will be populated""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "object",
                "aliases": ["target", "sink", "tail", "object_id"],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:object",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )
    value: Optional[str] = Field(
        default=None,
        description="""Note the range of this slot is always a string. Only used the triple represents a literal assertion""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "value",
                "close_mappings": ["rdf:object"],
                "domain_of": ["QuantityValue", "TextValue", "Statements"],
                "slot_uri": "rdf:object",
            }
        },
    )
    datatype: Optional[str] = Field(
        default=None,
        description="""the rdf datatype of the value, for example, xsd:string""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "datatype",
                "comments": ["only used when value is populated"],
                "domain_of": ["Statements"],
            }
        },
    )
    language: Optional[str] = Field(
        default=None,
        description="""the human language in which the value is encoded, e.g. 'en'""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "language",
                "comments": ["only used when value is populated"],
                "domain_of": ["TextValue", "Statements"],
                "todos": ["use an enum (rather than a string)"],
            }
        },
    )


class EntailedEdge(Table):
    """
    A relation graph edge that is inferred
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "comments": [
                "- It is common to populate this via a procedure external to the database, e.g balhoff/relation-graph"
            ],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_ontology",
            "see_also": ["https://github.com/balhoff/relation-graph"],
        }
    )

    subject: Optional[str] = Field(
        default=None,
        description="""The subject of the statement""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "subject",
                "aliases": ["about", "source", "head", "subject_id"],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:subject",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )
    predicate: Optional[str] = Field(
        default=None,
        description="""The predicate of the statement""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "predicate",
                "aliases": ["relationship", "relationship type", "property", "predicate_id"],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:predicate",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )
    object: Optional[str] = Field(
        default=None,
        description="""Note the range of this slot is always a node. If the triple represents a literal, instead value will be populated""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "object",
                "aliases": ["target", "sink", "tail", "object_id"],
                "domain_of": ["Association", "Statements", "EntailedEdge"],
                "slot_uri": "rdf:object",
                "todos": ["set range appropriately for ontology and association use"],
            }
        },
    )


class Geolocation(AttributeValue):
    """
    A normalized value for a location on the earth's surface
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "class_uri": "nmdc:GeolocationValue",
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_to_review",
            "mappings": ["schema:GeoCoordinates"],
        }
    )

    latitude: str = Field(
        default=..., json_schema_extra={"linkml_meta": {"alias": "latitude", "domain_of": ["Geolocation"]}}
    )
    longitude: str = Field(
        default=..., json_schema_extra={"linkml_meta": {"alias": "longitude", "domain_of": ["Geolocation"]}}
    )
    raw_value: Optional[str] = Field(
        default=None,
        description="""The raw value for a geolocation should follow {latitude} {longitude}""",
        json_schema_extra={"linkml_meta": {"alias": "raw_value", "domain_of": ["AttributeValue", "Geolocation"]}},
    )
    entity_id: str = Field(
        default=...,
        description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    attribute_name: str = Field(
        default=...,
        description="""The attribute being captured in this annotation.""",
        json_schema_extra={
            "linkml_meta": {"alias": "attribute_name", "aliases": ["type", "name"], "domain_of": ["AttributeValue"]}
        },
    )
    attribute_cv_term_id: Optional[str] = Field(
        default=None,
        description="""If the attribute is a term from a controlled vocabulary, the ID of the term.""",
        json_schema_extra={"linkml_meta": {"alias": "attribute_cv_term_id", "domain_of": ["AttributeValue"]}},
    )


class AssociationXPublication(Table):
    """
    Links associations to supporting literature.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {
                "association_id": {"multivalued": True, "name": "association_id"},
                "publication_id": {"multivalued": True, "name": "publication_id"},
            },
        }
    )

    association_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an association.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "association_id",
                "domain_of": ["Association", "Association_X_Publication", "Association_X_SupportingObject"],
            }
        },
    )
    publication_id: list[str] = Field(
        default=...,
        description="""Unique identifier for a publication - e.g. PMID, DOI, URL, etc.""",
        json_schema_extra={
            "linkml_meta": {"alias": "publication_id", "domain_of": ["Publication", "Association_X_Publication"]}
        },
    )


class AssociationXSupportingObject(Table):
    """
    Links associations to entities to capture supporting objects in an association. ay be a biological entity, such as a protein or feature, or a URL to a resource (e.g. a publication) that supports the association. Where possible, CDM identifiers should be used.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {
                "association_id": {"multivalued": True, "name": "association_id"},
                "entity_id": {"multivalued": True, "name": "entity_id"},
            },
        }
    )

    association_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an association.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "association_id",
                "domain_of": ["Association", "Association_X_Publication", "Association_X_SupportingObject"],
            }
        },
    )
    entity_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )


class ContigXContigCollection(Table):
    """
    Captures the relationship between a contig and a contig collection; equivalent to contig part-of contig collection.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"contig_id": {"multivalued": True, "name": "contig_id"}},
        }
    )

    contig_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_id",
                "domain_of": [
                    "Contig",
                    "Contig_X_ContigCollection",
                    "Contig_X_EncodedFeature",
                    "Contig_X_Feature",
                    "Contig_X_Protein",
                ],
            }
        },
    )
    contig_collection_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig collection.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_collection_id",
                "domain_of": [
                    "ContigCollection",
                    "Contig_X_ContigCollection",
                    "ContigCollection_X_EncodedFeature",
                    "ContigCollection_X_Feature",
                    "ContigCollection_X_Protein",
                ],
            }
        },
    )


class ContigXEncodedFeature(Table):
    """
    Captures the relationship between a contig and an encoded feature.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"encoded_feature_id": {"multivalued": True, "name": "encoded_feature_id"}},
        }
    )

    contig_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_id",
                "domain_of": [
                    "Contig",
                    "Contig_X_ContigCollection",
                    "Contig_X_EncodedFeature",
                    "Contig_X_Feature",
                    "Contig_X_Protein",
                ],
            }
        },
    )
    encoded_feature_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an encoded feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "encoded_feature_id",
                "domain_of": [
                    "EncodedFeature",
                    "Contig_X_EncodedFeature",
                    "ContigCollection_X_EncodedFeature",
                    "EncodedFeature_X_Feature",
                ],
            }
        },
    )


class ContigXFeature(Table):
    """
    Captures the relationship between a contig and a feature; equivalent to feature part-of contig.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"feature_id": {"multivalued": True, "name": "feature_id"}},
        }
    )

    contig_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_id",
                "domain_of": [
                    "Contig",
                    "Contig_X_ContigCollection",
                    "Contig_X_EncodedFeature",
                    "Contig_X_Feature",
                    "Contig_X_Protein",
                ],
            }
        },
    )
    feature_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "feature_id",
                "domain_of": [
                    "Feature",
                    "Contig_X_Feature",
                    "ContigCollection_X_Feature",
                    "EncodedFeature_X_Feature",
                    "Feature_X_Protein",
                ],
            }
        },
    )


class ContigXProtein(Table):
    """
    Captures the relationship between a contig and a protein; equivalent to protein is ribosomal translation of (http://purl.obolibrary.org/obo/RO_0002512) contig.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"protein_id": {"multivalued": True, "name": "protein_id"}},
        }
    )

    contig_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_id",
                "domain_of": [
                    "Contig",
                    "Contig_X_ContigCollection",
                    "Contig_X_EncodedFeature",
                    "Contig_X_Feature",
                    "Contig_X_Protein",
                ],
            }
        },
    )
    protein_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a protein.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protein_id",
                "domain_of": ["Protein", "Contig_X_Protein", "ContigCollection_X_Protein", "Feature_X_Protein"],
            }
        },
    )


class ContigCollectionXEncodedFeature(Table):
    """
    Captures the relationship between a contig collection and an encoded feature.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"encoded_feature_id": {"multivalued": True, "name": "encoded_feature_id"}},
        }
    )

    contig_collection_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig collection.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_collection_id",
                "domain_of": [
                    "ContigCollection",
                    "Contig_X_ContigCollection",
                    "ContigCollection_X_EncodedFeature",
                    "ContigCollection_X_Feature",
                    "ContigCollection_X_Protein",
                ],
            }
        },
    )
    encoded_feature_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an encoded feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "encoded_feature_id",
                "domain_of": [
                    "EncodedFeature",
                    "Contig_X_EncodedFeature",
                    "ContigCollection_X_EncodedFeature",
                    "EncodedFeature_X_Feature",
                ],
            }
        },
    )


class ContigCollectionXFeature(Table):
    """
    Captures the relationship between a contig collection and a feature; equivalent to feature part-of contig collection.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"feature_id": {"multivalued": True, "name": "feature_id"}},
        }
    )

    contig_collection_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig collection.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_collection_id",
                "domain_of": [
                    "ContigCollection",
                    "Contig_X_ContigCollection",
                    "ContigCollection_X_EncodedFeature",
                    "ContigCollection_X_Feature",
                    "ContigCollection_X_Protein",
                ],
            }
        },
    )
    feature_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "feature_id",
                "domain_of": [
                    "Feature",
                    "Contig_X_Feature",
                    "ContigCollection_X_Feature",
                    "EncodedFeature_X_Feature",
                    "Feature_X_Protein",
                ],
            }
        },
    )


class ContigCollectionXProtein(Table):
    """
    Captures the relationship between a contig collection and a protein; equivalent to protein is ribosomal translation of (http://purl.obolibrary.org/obo/RO_0002512) contig collection.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"protein_id": {"multivalued": True, "name": "protein_id"}},
        }
    )

    contig_collection_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contig collection.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contig_collection_id",
                "domain_of": [
                    "ContigCollection",
                    "Contig_X_ContigCollection",
                    "ContigCollection_X_EncodedFeature",
                    "ContigCollection_X_Feature",
                    "ContigCollection_X_Protein",
                ],
            }
        },
    )
    protein_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a protein.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protein_id",
                "domain_of": ["Protein", "Contig_X_Protein", "ContigCollection_X_Protein", "Feature_X_Protein"],
            }
        },
    )


class ContributorXRoleXExperiment(Table):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "http://kbase.github.io/cdm-schema/cdm_schema", "represents_relationship": True}
    )

    contributor_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contributor.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contributor_id",
                "domain_of": ["Contributor", "Contributor_X_Role_X_Experiment", "Contributor_X_Role_X_Project"],
            }
        },
    )
    experiment_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an experiment.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "experiment_id",
                "domain_of": [
                    "Experiment",
                    "Contributor_X_Role_X_Experiment",
                    "Experiment_X_Project",
                    "Experiment_X_Sample",
                ],
            }
        },
    )
    contributor_role: Optional[ContributorRole] = Field(
        default=None,
        description="""Role(s) played by the contributor when working on the experiment. If more than one role was played, additional rows should be added to represent each role.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contributor_role",
                "domain_of": ["Contributor_X_Role_X_Experiment", "Contributor_X_Role_X_Project"],
                "slot_uri": "schema:Role",
            }
        },
    )


class ContributorXRoleXProject(Table):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "http://kbase.github.io/cdm-schema/cdm_schema", "represents_relationship": True}
    )

    contributor_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a contributor.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contributor_id",
                "domain_of": ["Contributor", "Contributor_X_Role_X_Experiment", "Contributor_X_Role_X_Project"],
            }
        },
    )
    project_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a project.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "project_id",
                "domain_of": ["Project", "Contributor_X_Role_X_Project", "Experiment_X_Project"],
            }
        },
    )
    contributor_role: Optional[ContributorRole] = Field(
        default=None,
        description="""Role(s) played by the contributor when working on the experiment. If more than one role was played, additional rows should be added to represent each role.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "contributor_role",
                "domain_of": ["Contributor_X_Role_X_Experiment", "Contributor_X_Role_X_Project"],
                "slot_uri": "schema:Role",
            }
        },
    )


class EncodedFeatureXFeature(Table):
    """
    Captures the relationship between a feature and its transcription product.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "http://kbase.github.io/cdm-schema/cdm_schema", "represents_relationship": True}
    )

    encoded_feature_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an encoded feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "encoded_feature_id",
                "domain_of": [
                    "EncodedFeature",
                    "Contig_X_EncodedFeature",
                    "ContigCollection_X_EncodedFeature",
                    "EncodedFeature_X_Feature",
                ],
            }
        },
    )
    feature_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "feature_id",
                "domain_of": [
                    "Feature",
                    "Contig_X_Feature",
                    "ContigCollection_X_Feature",
                    "EncodedFeature_X_Feature",
                    "Feature_X_Protein",
                ],
            }
        },
    )


class EntityXMeasurement(Table):
    """
    Captures a measurement made on an entity.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {
                "entity_id": {"multivalued": True, "name": "entity_id"},
                "measurement_id": {"multivalued": True, "name": "measurement_id"},
            },
        }
    )

    entity_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an entity.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "entity_id",
                "domain_of": [
                    "ClusterMember",
                    "Sequence",
                    "Entity",
                    "Identifier",
                    "Name",
                    "AttributeValue",
                    "Association_X_SupportingObject",
                    "Entity_X_Measurement",
                ],
            }
        },
    )
    measurement_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a measurement.""",
        json_schema_extra={
            "linkml_meta": {"alias": "measurement_id", "domain_of": ["Measurement", "Entity_X_Measurement"]}
        },
    )


class ExperimentXProject(Table):
    """
    Captures the relationship between an experiment and the project that it is a part of.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"experiment_id": {"multivalued": True, "name": "experiment_id"}},
        }
    )

    experiment_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an experiment.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "experiment_id",
                "domain_of": [
                    "Experiment",
                    "Contributor_X_Role_X_Experiment",
                    "Experiment_X_Project",
                    "Experiment_X_Sample",
                ],
            }
        },
    )
    project_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a project.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "project_id",
                "domain_of": ["Project", "Contributor_X_Role_X_Project", "Experiment_X_Project"],
            }
        },
    )


class ExperimentXSample(Table):
    """
    Represents the participation of a sample in an experiment.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {
                "experiment_id": {"multivalued": True, "name": "experiment_id"},
                "sample_id": {"multivalued": True, "name": "sample_id"},
            },
        }
    )

    experiment_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for an experiment.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "experiment_id",
                "domain_of": [
                    "Experiment",
                    "Contributor_X_Role_X_Experiment",
                    "Experiment_X_Project",
                    "Experiment_X_Sample",
                ],
            }
        },
    )
    sample_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a sample.""",
        json_schema_extra={"linkml_meta": {"alias": "sample_id", "domain_of": ["Sample", "Experiment_X_Sample"]}},
    )


class FeatureXProtein(Table):
    """
    Captures the relationship between a feature and a protein; equivalent to feature encodes protein.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
            "slot_usage": {"protein_id": {"multivalued": True, "name": "protein_id"}},
        }
    )

    feature_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a feature.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "feature_id",
                "domain_of": [
                    "Feature",
                    "Contig_X_Feature",
                    "ContigCollection_X_Feature",
                    "EncodedFeature_X_Feature",
                    "Feature_X_Protein",
                ],
            }
        },
    )
    protein_id: list[str] = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a protein.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protein_id",
                "domain_of": ["Protein", "Contig_X_Protein", "ContigCollection_X_Protein", "Feature_X_Protein"],
            }
        },
    )


class ProtocolXProtocolParticipant(Table):
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {"from_schema": "http://kbase.github.io/cdm-schema/cdm_schema", "represents_relationship": True}
    )

    protocol_id: str = Field(
        default=...,
        description="""Internal (CDM) unique identifier for a protocol.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protocol_id",
                "domain_of": ["Cluster", "Feature", "Protocol", "Measurement", "Protocol_X_ProtocolParticipant"],
            }
        },
    )
    protocol_participant_id: str = Field(
        default=...,
        description="""The unique identifier for the protocol participant.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "protocol_participant_id",
                "domain_of": ["ProtocolParticipant", "Protocol_X_ProtocolParticipant"],
            }
        },
    )
    participant_type: Optional[str] = Field(
        default=None,
        description="""The type of participant in the protocol.""",
        json_schema_extra={
            "linkml_meta": {
                "alias": "participant_type",
                "domain_of": ["Protocol_X_ProtocolParticipant"],
                "examples": [{"value": "input"}, {"value": "output"}],
            }
        },
    )


class NamedEntity(Table):
    """
    Represents the link between an entity and its names.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "comments": [
                "Entity.entity_id <> Name.entity_id",
                "one entity can have multiple names, and one name can be associated with multiple entities.",
            ],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
        }
    )

    pass


class IdentifiedEntity(Table):
    """
    Represents the link between an entity and its identifiers.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "comments": [
                "Entity.entity_id <> Identifier.entity_id",
                "one entity can have multiple identifiers, and one identifier "
                "can be associated with multiple entities.",
            ],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
        }
    )

    pass


class AttributeValueEntity(Table):
    """
    Represents the link between an entity and its attribute values.
    """

    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta(
        {
            "comments": [
                "Entity.entity_id <> QuantityValue.entity_id",
                "Entity.entity_id <> TextValue.entity_id",
                "one entity can have multiple attribute values, and one "
                "attribute value can be associated with multiple entities.",
            ],
            "from_schema": "http://kbase.github.io/cdm-schema/cdm_schema",
            "represents_relationship": True,
        }
    )

    pass


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Table.model_rebuild()
Association.model_rebuild()
Cluster.model_rebuild()
ClusterMember.model_rebuild()
Contig.model_rebuild()
ContigCollection.model_rebuild()
Contributor.model_rebuild()
DataSource.model_rebuild()
EncodedFeature.model_rebuild()
GoldEnvironmentalContext.model_rebuild()
MixsEnvironmentalContext.model_rebuild()
Event.model_rebuild()
Experiment.model_rebuild()
Feature.model_rebuild()
Project.model_rebuild()
Protein.model_rebuild()
Protocol.model_rebuild()
ProtocolParticipant.model_rebuild()
Publication.model_rebuild()
Sample.model_rebuild()
Sequence.model_rebuild()
Entity.model_rebuild()
Identifier.model_rebuild()
Name.model_rebuild()
AttributeValue.model_rebuild()
QuantityValue.model_rebuild()
TextValue.model_rebuild()
Measurement.model_rebuild()
ProcessedMeasurement.model_rebuild()
Prefix.model_rebuild()
Statements.model_rebuild()
EntailedEdge.model_rebuild()
Geolocation.model_rebuild()
AssociationXPublication.model_rebuild()
AssociationXSupportingObject.model_rebuild()
ContigXContigCollection.model_rebuild()
ContigXEncodedFeature.model_rebuild()
ContigXFeature.model_rebuild()
ContigXProtein.model_rebuild()
ContigCollectionXEncodedFeature.model_rebuild()
ContigCollectionXFeature.model_rebuild()
ContigCollectionXProtein.model_rebuild()
ContributorXRoleXExperiment.model_rebuild()
ContributorXRoleXProject.model_rebuild()
EncodedFeatureXFeature.model_rebuild()
EntityXMeasurement.model_rebuild()
ExperimentXProject.model_rebuild()
ExperimentXSample.model_rebuild()
FeatureXProtein.model_rebuild()
ProtocolXProtocolParticipant.model_rebuild()
NamedEntity.model_rebuild()
IdentifiedEntity.model_rebuild()
AttributeValueEntity.model_rebuild()
