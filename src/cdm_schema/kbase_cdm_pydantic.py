from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "0.0.1"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'kb_cdm',
     'default_range': 'string',
     'description': 'Schema for KBase CDM',
     'id': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
     'imports': ['cdm_components', 'cdm_join_tables'],
     'name': 'cdm_schema',
     'prefixes': {'kb_cdm': {'prefix_prefix': 'kb_cdm',
                             'prefix_reference': 'http://kbase.github.io/cdm-schema/linkml/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'}},
     'source_file': 'src/linkml/cdm_schema.yaml'} )

class ClusterType(str, Enum):
    """
    The type of the entities in a cluster. Must be represented by a table in the CDM schema.
    """
    Protein = "Protein"
    Feature = "Feature"
    ContigCollection = "ContigCollection"


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
    Contributor = "Contributor"
    Project = "Project"
    Experiment = "Experiment"


class AttributeValueType(str, Enum):
    DateTimeValue = "DateTimeValue"
    """
    A date or date and time value.
    """
    QuantityValue = "QuantityValue"
    """
    A simple quantity, e.g. 2 cm.
    """
    QuantityRangeValue = "QuantityRangeValue"
    """
    A numerical range, e.g. 5-7 cm.
    """
    TextValue = "TextValue"
    """
    A quality, described using a text string.
    """
    ControlledTermValue = "ControlledTermValue"
    """
    A quality, described using a text string from a controlled vocabulary or enum.
    """
    ControlledVocabularyTermValue = "ControlledVocabularyTermValue"
    """
    A quality, described using a term from an ontology or schema with a stable persistent identifier.
    """
    Geolocation = "Geolocation"
    """
    A location, described using latitude and longitude.
    """


class ContributorRole(str, Enum):
    """
    The type of contribution made by a contributor.
    """
    contact_person = "contact_person"
    """
    Person with knowledge of how to access, troubleshoot, or otherwise field issues related to the resource. May also be "Point of Contact" in organisation that controls access to the resource, if that organisation is different from Publisher, Distributor, Data Manager.
    """
    data_collector = "data_collector"
    """
    Person/institution responsible for finding, gathering/collecting data under the guidelines of the author(s) or Principal Investigator (PI). May also use when crediting survey conductors, interviewers, event or condition observers, person responsible for monitoring key instrument data.
    """
    data_curator = "data_curator"
    """
    Person tasked with reviewing, enhancing, cleaning, or standardizing metadata and the associated data submitted for storage, use, and maintenance within a data centre or repository. While the "DataManager" is concerned with digital maintenance, the DataCurator's role encompasses quality assurance focused on content and metadata. This includes checking whether the submitted dataset is complete, with all files and components as described by submitter, whether the metadata is standardized to appropriate systems and schema, whether specialized metadata is needed to add value and ensure access across disciplines, and determining how the metadata might map to search engines, database products, and automated feeds.
    """
    data_manager = "data_manager"
    """
    Person (or organisation with a staff of data managers, such as a data centre) responsible for maintaining the finished resource. The work done by this person or organisation ensures that the resource is periodically "refreshed" in terms of software/hardware support, is kept available or is protected from unauthorized access, is stored in accordance with industry standards, and is handled in accordance with the records management requirements applicable to it.
    """
    distributor = "distributor"
    """
    Institution tasked with responsibility to generate/disseminate copies of the resource in either electronic or print form. Works stored in more than one archive/repository may credit each as a distributor.
    """
    editor = "editor"
    """
    A person who oversees the details related to the publication format of the resource. N.b. if the Editor is to be credited in place of multiple creators, the Editor's name may be supplied as Creator, with "(Ed.)" appended to the name.
    """
    hosting_institution = "hosting_institution"
    """
    Typically, the organisation allowing the resource to be available on the internet through the provision of its hardware/software/operating support. May also be used for an organisation that stores the data offline. Often a data centre (if that data centre is not the "publisher" of the resource).
    """
    producer = "producer"
    """
    Typically a person or organisation responsible for the artistry and form of a media product. In the data industry, this may be a company "producing" DVDs that package data for future dissemination by a distributor.
    """
    project_leader = "project_leader"
    """
    Person officially designated as head of project team or sub- project team instrumental in the work necessary to development of the resource. The Project Leader is not "removed" from the work that resulted in the resource; he or she remains intimately involved throughout the life of the particular project team.
    """
    project_manager = "project_manager"
    """
    Person officially designated as manager of a project. Project may consist of one or many project teams and sub-teams. The manager of a project normally has more administrative responsibility than actual work involvement.
    """
    project_member = "project_member"
    """
    Person on the membership list of a designated project/project team. This vocabulary may or may not indicate the quality, quantity, or substance of the person's involvement.
    """
    registration_agency = "registration_agency"
    """
    Institution/organisation officially appointed by a Registration Authority to handle specific tasks within a defined area of responsibility. DataCite is a Registration Agency for the International DOI Foundation (IDF). One of DataCite's tasks is to assign DOI prefixes to the allocating agents who then assign the full, specific character string to data clients, provide metadata back to the DataCite registry, etc.
    """
    registration_authority = "registration_authority"
    """
    A standards-setting body from which Registration Agencies obtain official recognition and guidance. The IDF serves as the Registration Authority for the International Standards Organisation (ISO) in the area/domain of Digital Object Identifiers.
    """
    related_person = "related_person"
    """
    A person without a specifically defined role in the development of the resource, but who is someone the author wishes to recognize. This person could be an author's intellectual mentor, a person providing intellectual leadership in the discipline or subject domain, etc.
    """
    researcher = "researcher"
    """
    A person involved in analyzing data or the results of an experiment or formal study. May indicate an intern or assistant to one of the authors who helped with research but who was not so "key" as to be listed as an author. Should be a person, not an institution. Note that a person involved in the gathering of data would fall under the contributorType "DataCollector." The researcher may find additional data online and correlate it to the data collected for the experiment or study, for example.
    """
    research_group = "research_group"
    """
    Typically refers to a group of individuals with a lab, department, or division; the group has a particular, defined focus of activity. May operate at a narrower level of scope; may or may not hold less administrative responsibility than a project team.
    """
    rights_holder = "rights_holder"
    """
    Person or institution owning or managing property rights, including intellectual property rights over the resource.
    """
    sponsor = "sponsor"
    """
    Person or organisation that issued a contract or under the auspices of which a work has been written, printed, published, developed, etc. Includes organisations that provide in-kind support, through donation, provision of people or a facility or instrumentation necessary for the development of the resource, etc.
    """
    supervisor = "supervisor"
    """
    Designated administrator over one or more groups/teams working to produce a resource or over one or more steps of a development process.
    """
    work_package_leader = "work_package_leader"
    """
    A Work Package is a recognized data product, not all of which is included in publication. The package, instead, may include notes, discarded documents, etc. The Work Package Leader is responsible for ensuring the comprehensive contents, versioning, and availability of the Work Package during the development of the resource.
    """
    other = "other"
    """
    Any person or institution making a significant contribution to the development and/or maintenance of the resource, but whose contribution does not "fit" other controlled vocabulary for contributorType. Could be a photographer, artist, or writer whose contribution helped to publicize the resource (as opposed to creating it), a reviewer of the resource, someone providing administrative services to the author (such as depositing updates into an online repository, analysing usage, etc.), or one of many other roles.
    """
    conceptualization = "conceptualization"
    """
    Ideas; formulation or evolution of overarching research goals and aims.
    """
    data_curation = "data_curation"
    """
    Management activities to annotate (produce metadata), scrub data and maintain research data (including software code, where it is necessary for interpreting the data itself) for initial use and later re-use.
    """
    formal_analysis = "formal_analysis"
    """
    Application of statistical, mathematical, computational, or other formal techniques to analyze or synthesize study data.
    """
    funding_acquisition = "funding_acquisition"
    """
    Acquisition of the financial support for the project leading to this publication.
    """
    investigation = "investigation"
    """
    Conducting a research and investigation process, specifically performing the experiments, or data/evidence collection.
    """
    methodology = "methodology"
    """
    Development or design of methodology; creation of models.
    """
    project_administration = "project_administration"
    """
    Management and coordination responsibility for the research activity planning and execution.
    """
    resources = "resources"
    """
    Provision of study materials, reagents, materials, patients, laboratory samples, animals, instrumentation, computing resources, or other analysis tools.
    """
    software = "software"
    """
    Programming, software development; designing computer programs; implementation of the computer code and supporting algorithms; testing of existing code components.
    """
    supervision = "supervision"
    """
    Oversight and leadership responsibility for the research activity planning and execution, including mentorship external to the core team.
    """
    validation = "validation"
    """
    Verification, whether as a part of the activity or separate, of the overall replication/reproducibility of results/experiments and other research outputs.
    """
    visualization = "visualization"
    """
    Preparation, creation and/or presentation of the published work, specifically visualization/data presentation.
    """
    writing_original_draft = "writing_original_draft"
    """
    Preparation, creation and/or presentation of the published work, specifically writing the initial draft (including substantive transformation).
    """
    writing_review_andSOLIDUSor_editing = "writing_review_editing"
    """
    Preparation, creation and/or presentation of the published work by those from the original research group, specifically critical review, commentary or revision -- including pre- or post-publication stages.
    """


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


class DescriptionType(str, Enum):
    """
    The type of text being represented.
    """
    abstract = "abstract"
    """
    A brief description of the resource and the context in which the resource was created.
    """
    description = "description"
    summary = "summary"


class EventType(str, Enum):
    """
    The type of date being represented.
    """
    accepted = "accepted"
    """
    The date that the publisher accepted the resource into their system. To indicate the start of an embargo period, use Submitted or Accepted, as appropriate.

    """
    available = "available"
    """
    The date the resource is made publicly available. To indicate the end of an embargo period, use Available.

    """
    copyrighted = "copyrighted"
    """
    The specific, documented date at which the resource receives a copyrighted status, if applicable.

    """
    collected = "collected"
    """
    The date or date range in which the resource content was collected. To indicate precise or particular timeframes in which research was conducted.

    """
    created = "created"
    """
    The date the resource itself was put together; this could refer to a timeframe in ancient history, be a date range or a single date for a final component, e.g., the finalized file with all of the data.

    """
    issued = "issued"
    """
    The date that the resource is published or distributed e.g. to a data centre

    """
    submitted = "submitted"
    """
    The date the creator submits the resource to the publisher. This could be different from Accepted if the publisher then applies a selection process. To indicate the start of an embargo period, use Submitted or Accepted, as appropriate.

    """
    updated = "updated"
    """
    The date of the last update to the resource, when the resource is being added to.

    """
    valid = "valid"
    """
    The date (or date range) during which the dataset or resource is accurate.

    """
    withdrawn = "withdrawn"
    """
    The date the resource is removed.

    """
    other = "other"


class RelationshipType(str, Enum):
    """
    The relationship between two entities. For example, when a PermanentID class is used to represent objects in the CreditMetadata field `related_identifiers`, the `relationship_type` field captures the relationship between the resource being registered (A) and this ID (B).
    """
    based_on_data = "based_on_data"
    cites = "cites"
    """
    Indicates that A includes B in a citation.

    """
    compiles = "compiles"
    """
    Indicates B is the result of a compile or creation event using A. Note: May be used for software and text, as a compiler can be a computer program or a person.

    """
    continues = "continues"
    """
    Indicates A is a continuation of the work B.

    """
    describes = "describes"
    """
    Indicates A describes B.

    """
    documents = "documents"
    """
    Indicates A is documentation about B; e.g. points to software documentation.

    """
    finances = "finances"
    has_comment = "has_comment"
    has_derivation = "has_derivation"
    has_expression = "has_expression"
    has_format = "has_format"
    has_manifestation = "has_manifestation"
    has_manuscript = "has_manuscript"
    has_metadata = "has_metadata"
    """
    Indicates resource A has additional metadata B.

    """
    has_part = "has_part"
    """
    Indicates A includes the part B.
    Primarily this relation is applied to container-contained type relationships.
    Note: May be used for individual software modules; note that code repository-to-version relationships should be modeled using IsVersionOf and HasVersion.

    """
    has_preprint = "has_preprint"
    has_related_material = "has_related_material"
    has_reply = "has_reply"
    has_review = "has_review"
    has_transformation = "has_transformation"
    has_version = "has_version"
    """
    Indicates A has a version (B).
    The registered resource such as a software package or code repository has a versioned instance (indicates A has the instance B) e.g. it may be used to relate an un-versioned code repository to one of its specific software versions.

    """
    is_based_on = "is_based_on"
    is_basis_for = "is_basis_for"
    is_cited_by = "is_cited_by"
    """
    Indicates that B includes A in a citation.

    """
    is_comment_on = "is_comment_on"
    is_compiled_by = "is_compiled_by"
    """
    Indicates B is used to compile or create A. Note: May be used for software and text, as a compiler can be a computer program or a person.

    """
    is_continued_by = "is_continued_by"
    """
    Indicates A is continued by the work B.

    """
    is_data_basis_for = "is_data_basis_for"
    is_derived_from = "is_derived_from"
    """
    Indicates B is a source upon which A is based.
    IsDerivedFrom should be used for a resource that is a derivative of an original resource.
    For example, `A isDerivedFrom B` could describe a dataset (A) derived from a larger dataset (B) where data values have been manipulated from their original state.

    """
    is_described_by = "is_described_by"
    """
    Indicates A is described by B.

    """
    is_documented_by = "is_documented_by"
    """
    Indicates B is documentation about/explaining A; e.g. points to software documentation.

    """
    is_expression_of = "is_expression_of"
    is_financed_by = "is_financed_by"
    is_format_of = "is_format_of"
    is_identical_to = "is_identical_to"
    """
    Indicates that A is identical to B, for use when there is a need to register two separate instances of the same resource.
    IsIdenticalTo should be used for a resource that is the same as the registered resource but is saved in another location, maybe another institution.

    """
    is_manifestation_of = "is_manifestation_of"
    is_manuscript_of = "is_manuscript_of"
    is_metadata_for = "is_metadata_for"
    """
    Indicates additional metadata A for a resource B.

    """
    is_new_version_of = "is_new_version_of"
    """
    Indicates A is a new edition of B, where the new edition has been modified or updated.

    """
    is_obsoleted_by = "is_obsoleted_by"
    """
    Indicates A is replaced by B.

    """
    is_original_form_of = "is_original_form_of"
    """
    Indicates A is the original form of B.
    May be used for different software operating systems or compiler formats, for example.

    """
    is_part_of = "is_part_of"
    """
    Indicates A is a portion of B; may be used for elements of a series.
    Primarily this relation is applied to container-contained type relationships.
    Note: May be used for individual software modules; note that code repository-to-version relationships should be modeled using IsVersionOf and HasVersion.

    """
    is_preprint_of = "is_preprint_of"
    is_previous_version_of = "is_previous_version_of"
    """
    Indicates A is a previous edition of B.

    """
    is_published_in = "is_published_in"
    """
    indicates A is published inside B, but is independent of other things published inside of B.

    """
    is_referenced_by = "is_referenced_by"
    """
    Indicates A is used as a source of information by B.

    """
    is_related_material = "is_related_material"
    is_replaced_by = "is_replaced_by"
    is_reply_to = "is_reply_to"
    is_required_by = "is_required_by"
    """
    Indicates A is required by B.
    Note: May be used to indicate software dependencies.

    """
    is_review_of = "is_review_of"
    is_reviewed_by = "is_reviewed_by"
    """
    Indicates that A is reviewed by B.

    """
    is_same_as = "is_same_as"
    is_source_of = "is_source_of"
    """
    Indicates A is a source upon which B is based.
    IsSourceOf is the original resource from which a derivative resource was created.
    For example, `A isSourceOf B` could describe a dataset (A) which acts as the source of a derived dataset (B) where the values have been manipulated.

    """
    is_supplement_to = "is_supplement_to"
    """
    Indicates that A is a supplement to B.

    """
    is_supplemented_by = "is_supplemented_by"
    """
    Indicates that B is a supplement to A.

    """
    is_transformation_of = "is_transformation_of"
    is_variant_form_of = "is_variant_form_of"
    """
    Indicates A is a variant or different form of B.
    Use for a different form of one thing.
    May be used for different software operating systems or compiler formats, for example.

    """
    is_version_of = "is_version_of"
    """
    Indicates A is a version of B.
    The registered resource is an instance of a target resource (indicates that A is an instance of B) e.g. it may be used to relate a specific version of a software package to its software code repository.

    """
    obsoletes = "obsoletes"
    """
    Indicates A replaces B.

    """
    references = "references"
    """
    Indicates B is used as a source of information for A.

    """
    replaces = "replaces"
    requires = "requires"
    """
    Indicates A requires B.
    Note: May be used to indicate software dependencies.

    """
    reviews = "reviews"
    """
    Indicates that A is a review of B.

    """
    unknown = "unknown"
    """
    The relationship between subject and object is unknown.
    """


class ResourceType(str, Enum):
    """
    The type of resource being represented.
    """
    dataset = "dataset"
    """
    A dataset.
    """


class TitleType(str, Enum):
    """
    The type of title being represented.
    """
    subtitle = "subtitle"
    """
    Any subtitle for the resource.
    """
    alternative_title = "alternative_title"
    """
    Other title(s) or names for the resource.
    """
    translated_title = "translated_title"
    """
    transformation of the title into another language.
    """
    other = "other"
    """
    Anything that doesn't fit into the above categories.
    """


class ProtocolParameterType(str, Enum):
    """
    An input, an operation parameter or switch, or an output for a protocol.
    """
    input = "input"
    """
    An input for an algorithmic protocol. Operational parameters or switches should also be captured here.
    """
    output = "output"
    """
    An output of an algorithmic protocol.
    """


class VariableType(str):
    """
    The type of the value of a variable. Should be a LinkML data type or one of the defined CDM data types.
    """
    pass


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
    Abstract class representing a table in the CDM schema.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_base'})

    pass


class Association(Table):
    """
    An association between an object--typically an entity such as a protein or a feature--and a classification system or ontology, such as the Gene Ontology, the Enzyme Classification, or TIGRFAMS domains.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['annotation',
                     'functional annotation',
                     'gene annotation',
                     'structural annotation',
                     'protein annotation'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_components',
         'slot_usage': {'association_id': {'identifier': True,
                                           'name': 'association_id'},
                        'object': {'comments': ['kb_cdm:Statement.subject'],
                                   'description': 'The object of an association. '
                                                  'Should be an ontology term or '
                                                  'database cross-reference.',
                                   'name': 'object',
                                   'range': 'local_curie',
                                   'required': True},
                        'predicate': {'description': 'The relationship between subject '
                                                     'and object in an association. '
                                                     'Should be a term from the '
                                                     'Relation Ontology.',
                                      'name': 'predicate',
                                      'pattern': '^RO:\\d+$',
                                      'range': 'local_curie',
                                      'required': True},
                        'subject': {'any_of': [{'range': 'cdm_feature_id'},
                                               {'range': 'cdm_encoded_feature_id'},
                                               {'range': 'cdm_protein_id'},
                                               {'range': 'cdm_contig_collection_id'}],
                                    'description': 'The subject of an association.',
                                    'name': 'subject',
                                    'range': 'Any',
                                    'required': True}}})

    association_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an association.""", json_schema_extra = { "linkml_meta": {'alias': 'association_id',
         'domain_of': ['Association', 'Association_x_SupportingObject']} })
    subject: str = Field(default=..., description="""The subject of an association.""", json_schema_extra = { "linkml_meta": {'alias': 'subject',
         'aliases': ['about', 'source', 'head', 'subject_id'],
         'any_of': [{'range': 'cdm_feature_id'},
                    {'range': 'cdm_encoded_feature_id'},
                    {'range': 'cdm_protein_id'},
                    {'range': 'cdm_contig_collection_id'}],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:subject',
         'todos': ['set range appropriately for ontology and association use']} })
    object: str = Field(default=..., description="""The object of an association. Should be an ontology term or database cross-reference.""", json_schema_extra = { "linkml_meta": {'alias': 'object',
         'aliases': ['target', 'sink', 'tail', 'object_id'],
         'comments': ['kb_cdm:Statement.subject'],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:object',
         'todos': ['set range appropriately for ontology and association use']} })
    predicate: str = Field(default=..., description="""The relationship between subject and object in an association. Should be a term from the Relation Ontology.""", json_schema_extra = { "linkml_meta": {'alias': 'predicate',
         'aliases': ['relationship', 'relationship type', 'property', 'predicate_id'],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:predicate',
         'todos': ['set range appropriately for ontology and association use']} })
    negated: Optional[bool] = Field(default=False, description="""If true, the relationship between the subject and object is negated. For example, consider an association where the subject is a protein ID, the object is the GO term for \"glucose biosynthesis\", and the predicate is \"involved in\". With the \"negated\" field set to false, the association is interpreted as \"<protein ID> is involved in glucose biosynthesis\". With the \"negated\" field set to true, the association is interpreted as \"<protein ID> is not involved in glucose biosynthesis\".""", json_schema_extra = { "linkml_meta": {'alias': 'negated', 'domain_of': ['Association'], 'ifabsent': 'false'} })
    evidence_type: Optional[str] = Field(default=None, description="""The type of evidence supporting the association. Should be a term from the Evidence and Conclusion Ontology (ECO). Specific pieces of evidence that support the association should be added as supporting objects, in the AssociationSupportingObject table.""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_type',
         'aliases': ['evidence code'],
         'domain_of': ['Association']} })
    primary_knowledge_source: Optional[str] = Field(default=None, description="""The knowledge source or contributor that created the association. Should be a CDM ID from the Contributor or DataSource table.""", json_schema_extra = { "linkml_meta": {'alias': 'primary_knowledge_source', 'domain_of': ['Association']} })
    aggregator_knowledge_source: Optional[str] = Field(default=None, description="""The knowledge source that aggregated the association. Should be a CDM ID from the Contributor or DataSource table.""", json_schema_extra = { "linkml_meta": {'alias': 'aggregator_knowledge_source', 'domain_of': ['Association']} })
    annotation_date: Optional[str] = Field(default=None, description="""The date when the annotation was made.""", json_schema_extra = { "linkml_meta": {'alias': 'annotation_date', 'domain_of': ['Association']} })
    comments: Optional[str] = Field(default=None, description="""Any comments about the association.""", json_schema_extra = { "linkml_meta": {'alias': 'comments', 'domain_of': ['Association', 'DataSourceNew']} })

    @field_validator('predicate')
    def pattern_predicate(cls, v):
        pattern=re.compile(r"^RO:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid predicate format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid predicate format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('evidence_type')
    def pattern_evidence_type(cls, v):
        pattern=re.compile(r"^ECO:\d+$")
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
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_components',
         'slot_usage': {'cluster_id': {'identifier': True, 'name': 'cluster_id'},
                        'name': {'description': 'Name of the cluster, if available.',
                                 'name': 'name'}}})

    cluster_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a cluster.
From the Entity table: entity_id where entity_type == 'Cluster'.
""", json_schema_extra = { "linkml_meta": {'alias': 'cluster_id', 'domain_of': ['Cluster', 'ClusterMember']} })
    description: Optional[str] = Field(default=None, description="""Brief textual definition or description.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    name: Optional[str] = Field(default=None, description="""Name of the cluster, if available.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'slot_uri': 'schema:name'} })
    entity_type: ClusterType = Field(default=..., description="""Type of entity being clustered.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_type',
         'domain_of': ['Cluster', 'Entity'],
         'todos': ['This should be an enum: Protein, Feature, strain/species/other?']} })
    protocol_id: Optional[str] = Field(default=None, description="""Protocol used to generate the cluster.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_id',
         'domain_of': ['Cluster',
                       'Experiment',
                       'OrderedProtocolStep',
                       'Protocol',
                       'ProtocolExecution',
                       'ProtocolVariable',
                       'Feature']} })


class ClusterMember(Table):
    """
    Relationship representing membership of a cluster. An optional score can be assigned to each cluster member.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_components'})

    cluster_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a cluster.
From the Entity table: entity_id where entity_type == 'Cluster'.
""", json_schema_extra = { "linkml_meta": {'alias': 'cluster_id', 'domain_of': ['Cluster', 'ClusterMember']} })
    entity_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an entity.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })
    is_representative: Optional[bool] = Field(default=False, description="""Whether or not this member is the representative for the cluster. If 'is_representative' is false, it is assumed that this is a cluster member.""", json_schema_extra = { "linkml_meta": {'alias': 'is_representative',
         'domain_of': ['ClusterMember'],
         'ifabsent': 'false'} })
    is_seed: Optional[bool] = Field(default=False, description="""Whether or not this is the seed for this cluster.""", json_schema_extra = { "linkml_meta": {'alias': 'is_seed', 'domain_of': ['ClusterMember'], 'ifabsent': 'false'} })
    score: Optional[float] = Field(default=None, description="""Output from the clustering protocol indicating how closely a member matches the representative.""", json_schema_extra = { "linkml_meta": {'alias': 'score', 'domain_of': ['ClusterMember']} })


class Event(Table):
    """
    Something that happened.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_components',
         'slot_usage': {'event_id': {'identifier': True, 'name': 'event_id'}}})

    event_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an event.""", json_schema_extra = { "linkml_meta": {'alias': 'event_id', 'domain_of': ['Event']} })
    created_at: Optional[str] = Field(default=None, description="""The time at which the event started or was created.""", json_schema_extra = { "linkml_meta": {'alias': 'created_at',
         'domain_of': ['Event', 'Experiment', 'MeasurementSet', 'ProtocolExecution']} })
    description: Optional[str] = Field(default=None, description="""Brief text description of what actually happened.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample'],
         'todos': ['Create controlled vocab for events?']} })
    name: Optional[str] = Field(default=None, description="""Name or title for the event.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable']} })
    location: Optional[str] = Field(default=None, description="""The location for this event. May be described in terms of coordinates.""", json_schema_extra = { "linkml_meta": {'alias': 'location', 'domain_of': ['Event']} })


class GoldEnvironmentalContext(Table):
    """
    Environmental context, described using JGI's five level system.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_components',
         'slot_usage': {'gold_environmental_context_id': {'identifier': True,
                                                          'name': 'gold_environmental_context_id'}}})

    gold_environmental_context_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a GOLD environmental context.""", json_schema_extra = { "linkml_meta": {'alias': 'gold_environmental_context_id',
         'domain_of': ['GoldEnvironmentalContext']} })
    ecosystem: Optional[str] = Field(default=None, description="""JGI GOLD descriptor representing the top level ecosystem categorization.""", json_schema_extra = { "linkml_meta": {'alias': 'ecosystem', 'domain_of': ['GoldEnvironmentalContext']} })
    ecosystem_category: Optional[str] = Field(default=None, description="""JGI GOLD descriptor representing the ecosystem category.""", json_schema_extra = { "linkml_meta": {'alias': 'ecosystem_category', 'domain_of': ['GoldEnvironmentalContext']} })
    ecosystem_subtype: Optional[str] = Field(default=None, description="""JGI GOLD descriptor representing the subtype of ecosystem. May be \"Unclassified\".""", json_schema_extra = { "linkml_meta": {'alias': 'ecosystem_subtype', 'domain_of': ['GoldEnvironmentalContext']} })
    ecosystem_type: Optional[str] = Field(default=None, description="""JGI GOLD descriptor representing the ecosystem type. May be \"Unclassified\".""", json_schema_extra = { "linkml_meta": {'alias': 'ecosystem_type', 'domain_of': ['GoldEnvironmentalContext']} })
    specific_ecosystem: Optional[str] = Field(default=None, description="""JGI GOLD descriptor representing the most specific level of ecosystem categorization. May be \"Unclassified\".""", json_schema_extra = { "linkml_meta": {'alias': 'specific_ecosystem', 'domain_of': ['GoldEnvironmentalContext']} })


class MixsEnvironmentalContext(Table):
    """
    Environmental context, described using the MiXS convention of broad and local environment, plus the medium.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_components',
         'slot_usage': {'mixs_environmental_context_id': {'identifier': True,
                                                          'name': 'mixs_environmental_context_id'}}})

    mixs_environmental_context_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a mixs environmental context.""", json_schema_extra = { "linkml_meta": {'alias': 'mixs_environmental_context_id',
         'domain_of': ['MixsEnvironmentalContext']} })
    env_broad_scale: Optional[str] = Field(default=None, title="broad-scale environmental context", description="""Report the major environmental system the sample or specimen came from. The system(s) identified should have a coarse spatial grain, to provide the general environmental context of where the sampling was done (e.g. in the desert or a rainforest). We recommend using subclasses of EnvO's biome class: http://purl.obolibrary.org/obo/ENVO_00000428. EnvO documentation about how to use the field: https://github.com/EnvironmentOntology/envo/wiki/Using-ENVO-with-MIxS""", json_schema_extra = { "linkml_meta": {'alias': 'env_broad_scale',
         'aliases': ['broad-scale environmental context'],
         'annotations': {'expected_value': {'tag': 'expected_value',
                                            'value': 'The major environment type(s) '
                                                     'where the sample was collected. '
                                                     'Recommend subclasses of biome '
                                                     '[ENVO:00000428]. Multiple terms '
                                                     'can be separated by one or more '
                                                     'pipes.'},
                         'tooltip': {'tag': 'tooltip',
                                     'value': 'The biome or major environmental system '
                                              'where the sample or specimen '
                                              'originated. Choose values from '
                                              "subclasses of the 'biome' class "
                                              '[ENVO:00000428] in the Environment '
                                              'Ontology (ENVO). For host-associated or '
                                              'plant-associated samples, use terms '
                                              'from the UBERON or Plant Ontology to '
                                              'describe the broad anatomical or '
                                              'morphological context'}},
         'domain_of': ['MixsEnvironmentalContext'],
         'examples': [{'value': 'oceanic epipelagic zone biome [ENVO:01000033] for '
                                'annotating a water sample from the photic zone in '
                                'middle of the Atlantic Ocean'}],
         'slot_uri': 'mixs:0000012',
         'string_serialization': '{termLabel} {[termID]}'} })
    env_local_scale: Optional[str] = Field(default=None, title="local environmental context", description="""Report the entity or entities which are in the sample or specimen's local vicinity and which you believe have significant causal influences on your sample or specimen. We recommend using EnvO terms which are of smaller spatial grain than your entry for env_broad_scale. Terms, such as anatomical sites, from other OBO Library ontologies which interoperate with EnvO (e.g. UBERON) are accepted in this field. EnvO documentation about how to use the field: https://github.com/EnvironmentOntology/envo/wiki/Using-ENVO-with-MIxS.""", json_schema_extra = { "linkml_meta": {'alias': 'env_local_scale',
         'aliases': ['local environmental context'],
         'annotations': {'expected_value': {'tag': 'expected_value',
                                            'value': 'Environmental entities having '
                                                     'causal influences upon the '
                                                     'entity at time of sampling.'},
                         'tooltip': {'tag': 'tooltip',
                                     'value': 'The specific environmental  entities or '
                                              'features near the sample or specimen '
                                              'that significantly influence its '
                                              'characteristics or composition. These '
                                              'entities are typically smaller in scale '
                                              'than the broad environmental context. '
                                              'Values for this field should be '
                                              'countable, material nouns and must be '
                                              'chosen from subclasses of BFO:0000040 '
                                              '(material entity) that appear in the '
                                              'Environment Ontology (ENVO). For '
                                              'host-associated or plant-associated '
                                              'samples, use terms from the UBERON or '
                                              'Plant Ontology to describe specific '
                                              'anatomical structures or plant parts.'}},
         'domain_of': ['MixsEnvironmentalContext'],
         'examples': [{'value': 'litter layer [ENVO:01000338]; Annotating a pooled '
                                'sample taken from various vegetation layers in a '
                                'forest consider: canopy [ENVO:00000047]|herb and fern '
                                'layer [ENVO:01000337]|litter layer '
                                '[ENVO:01000338]|understory [01000335]|shrub layer '
                                '[ENVO:01000336].'}],
         'slot_uri': 'mixs:0000013',
         'string_serialization': '{termLabel} {[termID]}'} })
    env_medium: Optional[str] = Field(default=None, title="environmental medium", description="""Report the environmental material(s) immediately surrounding the sample or specimen at the time of sampling. We recommend using subclasses of 'environmental material' (http://purl.obolibrary.org/obo/ENVO_00010483). EnvO documentation about how to use the field: https://github.com/EnvironmentOntology/envo/wiki/Using-ENVO-with-MIxS . Terms from other OBO ontologies are permissible as long as they reference mass/volume nouns (e.g. air, water, blood) and not discrete, countable entities (e.g. a tree, a leaf, a table top).""", json_schema_extra = { "linkml_meta": {'alias': 'env_medium',
         'aliases': ['environmental medium'],
         'annotations': {'expected_value': {'tag': 'expected_value',
                                            'value': 'The material displaced by the '
                                                     'entity at time of sampling. '
                                                     'Recommend subclasses of '
                                                     'environmental material '
                                                     '[ENVO:00010483].'},
                         'tooltip': {'tag': 'tooltip',
                                     'value': 'The predominant environmental material '
                                              'or substrate that directly surrounds or '
                                              'hosts the sample or specimen at the '
                                              'time of sampling. Choose values from '
                                              "subclasses of the 'environmental "
                                              "material' class [ENVO:00010483] in the "
                                              'Environment Ontology (ENVO). Values for '
                                              'this field should be measurable or mass '
                                              'material nouns, representing continuous '
                                              'environmental materials. For '
                                              'host-associated or plant-associated '
                                              'samples, use terms from the UBERON or '
                                              'Plant Ontology to indicate a tissue, '
                                              'organ, or plant structure'}},
         'domain_of': ['MixsEnvironmentalContext'],
         'examples': [{'value': 'soil [ENVO:00001998]; Annotating a fish swimming in '
                                'the upper 100 m of the Atlantic Ocean, consider: '
                                'ocean water [ENVO:00002151]. Example: Annotating a '
                                'duck on a pond consider: pond water '
                                '[ENVO:00002228]|air [ENVO_00002005]'}],
         'slot_uri': 'mixs:0000014',
         'string_serialization': '{termLabel} {[termID]}'} })


class LinkerTable(Table):
    """
    Tables for linking between tables.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_base'})

    pass


class Entity(Table):
    """
    An entity in the CDM.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_base',
         'slot_usage': {'entity_id': {'identifier': True, 'name': 'entity_id'}}})

    entity_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an entity.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })
    entity_type: EntityType = Field(default=..., description="""The class of the entity. Must be a valid CDM class.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_type', 'domain_of': ['Cluster', 'Entity']} })
    data_source_id: Optional[str] = Field(default=None, description="""The source from which the data came.""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_id',
         'domain_of': ['Entity',
                       'Contributor_x_DataSource',
                       'DataSource',
                       'DataSourceNew',
                       'DataSource_x_Description',
                       'DataSource_x_FundingReference',
                       'DataSource_x_License',
                       'DataSource_x_Title']} })
    data_source_entity_id: Optional[str] = Field(default=None, description="""The primary, ideally unique, ID of the entity at the data source.""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_entity_id', 'domain_of': ['Entity']} })
    data_source_created: str = Field(default=..., description="""Date/timestamp for when the entity was created or added to the data source.""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_created', 'domain_of': ['Entity']} })
    data_source_updated: Optional[str] = Field(default=None, description="""Date/timestamp for when the entity was updated in the data source.""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_updated', 'domain_of': ['Entity']} })
    created: str = Field(default=..., description="""Date/timestamp for when the entity was created or added to the CDM.""", json_schema_extra = { "linkml_meta": {'alias': 'created',
         'aliases': ['cdm_created', 'cdm_entity_created', 'entity_created'],
         'domain_of': ['Entity']} })
    updated: str = Field(default=..., description="""Date/timestamp for when the entity was updated in the CDM.""", json_schema_extra = { "linkml_meta": {'alias': 'updated',
         'aliases': ['cdm_updated', 'cdm_entity_updated', 'entity_updated'],
         'domain_of': ['Entity']} })


class Identifier(Table):
    """
    A string used as a resolvable (external) identifier for an entity. This should be a CURIE in the form `<database_prefix>:<local_identifier>`. [Bioregistry](https://bioregistry.io) is used as the canonical reference for CURIE database prefixes; please use the prefix exactly as written in the Bioregistry entry.

    If the string cannot be resolved to an URL, it should be added to the `Name` table instead.

    This table is used for capturing external IDs. The internal CDM identifier should be used in the *_id field (e.g. feature_id, protein_id, contig_collection_id).

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_base',
         'slot_usage': {'description': {'description': 'Brief description of the '
                                                       'identifier.',
                                        'name': 'description'}}})

    entity_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an entity.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })
    identifier: str = Field(default=..., description="""Fully-qualified URL or CURIE used as an identifier for an entity.""", json_schema_extra = { "linkml_meta": {'alias': 'identifier',
         'domain_of': ['Identifier'],
         'examples': [{'value': 'UniProt:Q8KCD6'}, {'value': 'EC:5.2.3.14'}],
         'slot_uri': 'schema:identifier'} })
    description: Optional[str] = Field(default=None, description="""Brief description of the identifier.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    source: Optional[str] = Field(default=None, description="""The source for a specific piece of information; should be a CDM internal ID of a source in the DataSource table.""", json_schema_extra = { "linkml_meta": {'alias': 'source', 'domain_of': ['Identifier', 'Name']} })
    relationship: Optional[str] = Field(default=None, description="""Relationship between this identifier and the entity in the `entity_id` field. If absent, it is assumed that the identifier represents the same entity in another data source.""", json_schema_extra = { "linkml_meta": {'alias': 'relationship', 'domain_of': ['Identifier']} })


class Name(Table):
    """
    A string used as the name or label for an entity. This may be a primary name, alternative name, synonym, acronym, or any other label used to refer to an entity.

    Identifiers that look like CURIEs or database references, but which cannot be resolved using [Bioregistry](https://bioregistry.io) or [identifiers.org](https://identifiers.org) should be added to the `Name` table.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_base',
         'slot_usage': {'description': {'description': 'Brief description of the name '
                                                       'and/or its relationship to the '
                                                       'entity.',
                                        'examples': [{'value': 'UniProt recommended '
                                                               'full name'}],
                                        'name': 'description'},
                        'name': {'description': 'The string used as a name.',
                                 'examples': [{'value': 'Heat-inducible transcription '
                                                        'repressor HrcA'},
                                              {'value': 'Uncharacterized protein '
                                                        '002R'}],
                                 'name': 'name',
                                 'required': True,
                                 'slot_uri': 'schema:name'}}})

    entity_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an entity.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })
    name: str = Field(default=..., description="""The string used as a name.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'examples': [{'value': 'Heat-inducible transcription repressor HrcA'},
                      {'value': 'Uncharacterized protein 002R'}],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Brief description of the name and/or its relationship to the entity.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample'],
         'examples': [{'value': 'UniProt recommended full name'}]} })
    source: Optional[str] = Field(default=None, description="""The source for a specific piece of information; should be a CDM internal ID of a source in the DataSource table.""", json_schema_extra = { "linkml_meta": {'alias': 'source', 'domain_of': ['Identifier', 'Name']} })


class EntityNames(LinkerTable):
    """
    Represents the link between an entity and its names.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['Entity.entity_id one:many Name.entity_id',
                      'one entity can have multiple names, and one name can be '
                      'associated with multiple entities.'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_base',
         'represents_relationship': True})

    pass


class EntityIdentifiers(LinkerTable):
    """
    Represents the link between an entity and its identifiers.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['Entity.entity_id one:many Identifier.entity_id',
                      'one entity can have multiple identifiers, and one identifier '
                      'can be associated with multiple entities.'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_base',
         'represents_relationship': True})

    pass


class AttributeMixin(ConfiguredBaseModel):
    """
    The attribute in an attribute-value pair. One of `attribute_cv_id`, `attribute_cv_label`, and `attribute_string` is required.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'any_of': [{'slot_conditions': {'attribute_cv_id': {'name': 'attribute_cv_id',
                                                             'required': True}}},
                    {'slot_conditions': {'attribute_cv_label': {'name': 'attribute_cv_label',
                                                                'required': True}}},
                    {'slot_conditions': {'attribute_string': {'name': 'attribute_string',
                                                              'required': True}}}],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'mixin': True})

    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })


class EntityMixin(ConfiguredBaseModel):
    """
    A generic class for capturing attribute-value information about an entity in a structured form.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'mixin': True})

    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class UnitMixin(ConfiguredBaseModel):
    """
    The unit used in expressing a quantity value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'mixin': True})

    unit_cv_id: Optional[str] = Field(default=None, description="""The unit of the quantity, expressed as a CURIE from the Unit Ontology.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_cv_id',
         'aliases': ['unit term ID', 'unit PID'],
         'domain_of': ['UnitMixin']} })
    unit_cv_label: Optional[str] = Field(default=None, description="""The unit of a quantity, expressed as the term name of a term from the Unit Ontology or UCUM.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_cv_label',
         'aliases': ['unit term name'],
         'domain_of': ['UnitMixin']} })
    unit_string: Optional[str] = Field(default=None, description="""Links a QuantityValue to a unit. Units should be taken from the UCUM unit collection or the Unit Ontology. This field should only be used if the unit is not present in one of those sources.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_string',
         'aliases': ['scale'],
         'domain_of': ['UnitMixin'],
         'mappings': ['nmdc:unit', 'qud:unit', 'schema:unitCode', 'UO:0000000']} })


class AttributeValue(EntityMixin, AttributeMixin):
    """
    The value for any value of attribute for an entity. This object can hold both the un-normalized atomic value and the structured value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'aliases': ['EntityAttributeValue'],
         'class_uri': 'nmdc:AttributeValue',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'mixins': ['AttributeMixin', 'EntityMixin']})

    raw_value: Optional[str] = Field(default=None, description="""The value that was specified for an annotation in its raw form; e.g. \"2 cm\" or \"2-4 cm\"""", json_schema_extra = { "linkml_meta": {'alias': 'raw_value',
         'domain_of': ['AttributeValue'],
         'examples': [{'value': '2 cm'},
                      {'value': '2 to 5m'},
                      {'value': '37-39 degrees celcius'},
                      {'value': 'Regulation of glucose biosynthesis.'}],
         'mappings': ['nmdc:raw_value']} })
    type: Optional[AttributeValueType] = Field(default=None, description="""The type of value being represented - e.g. QuantityValue, TextValue, DateTimeValue, ControlledVocabularyTermValue, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence']} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class EntityAttributeValue(UnitMixin, EntityMixin, AttributeMixin):
    """
    Class comprising all possible entity-attribute-value slots.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'abstract': True,
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'mixins': ['AttributeMixin', 'EntityMixin', 'UnitMixin']})

    date_time: Optional[str] = Field(default=None, description="""A date or date and time, expressed in ISO 8601 format with timezone indicators where appropriate.  The date or date/time value, expressed in ISO 8601-compatible form. Dates should be expressed as YYYY-MM-DD; times should be expressed as HH:MM:SS with optional milliseconds and an indication of the timezone.""", json_schema_extra = { "linkml_meta": {'alias': 'date_time',
         'aliases': ['date', 'time', 'timestamp'],
         'domain_of': ['EntityAttributeValue', 'DateTimeValue'],
         'examples': [{'value': '2025-11-09'}, {'value': '2025-09-16T22:48:54Z'}]} })
    language: Optional[str] = Field(default=None, description="""the human language in which the value is encoded, e.g. 'en'""", json_schema_extra = { "linkml_meta": {'alias': 'language',
         'comments': ['only used when value is populated'],
         'domain_of': ['EntityAttributeValue',
                       'TextValue',
                       'ResourceDescription',
                       'ResourceTitle',
                       'Statement'],
         'todos': ['use an enum (rather than a string)']} })
    latitude: Optional[float] = Field(default=None, description="""The latitude portion of a geolocation.""", json_schema_extra = { "linkml_meta": {'alias': 'latitude', 'domain_of': ['EntityAttributeValue', 'Geolocation']} })
    longitude: Optional[float] = Field(default=None, description="""The longitude portion of a geolocation.""", json_schema_extra = { "linkml_meta": {'alias': 'longitude', 'domain_of': ['EntityAttributeValue', 'Geolocation']} })
    minimum_numeric_value: Optional[float] = Field(default=None, description="""The minimum value part, expressed as number, of the quantity value when the value covers a range.""", json_schema_extra = { "linkml_meta": {'alias': 'minimum_numeric_value',
         'domain_of': ['EntityAttributeValue', 'QuantityRangeValue'],
         'mappings': ['nmdc:minimum_numeric_value']} })
    maximum_numeric_value: Optional[float] = Field(default=None, description="""The maximum value part, expressed as number, of the quantity value when the value covers a range.""", json_schema_extra = { "linkml_meta": {'alias': 'maximum_numeric_value',
         'domain_of': ['EntityAttributeValue', 'QuantityRangeValue'],
         'mappings': ['nmdc:maximum_numeric_value']} })
    numeric_value: Optional[float] = Field(default=None, description="""The numerical part of a quantity value.""", json_schema_extra = { "linkml_meta": {'alias': 'numeric_value',
         'domain_of': ['EntityAttributeValue', 'QuantityValue'],
         'mappings': ['nmdc:numeric_value', 'qud:quantityValue', 'schema:value']} })
    text_value: Optional[str] = Field(default=None, description="""The value, as a text string. This field should only be used if the value is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'text_value',
         'aliases': ['value string', 'value text', 'string value'],
         'domain_of': ['EntityAttributeValue', 'TextValue']} })
    value_cv_id: Optional[str] = Field(default=None, description="""For values that are in a controlled vocabulary (CV), this attribute should capture the controlled vocabulary ID for the value.""", json_schema_extra = { "linkml_meta": {'alias': 'value_cv_id',
         'aliases': ['value term ID', 'value PID'],
         'domain_of': ['EntityAttributeValue', 'ControlledVocabularyTermValue']} })
    value_cv_label: Optional[str] = Field(default=None, description="""For values that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'value_cv_label',
         'aliases': ['value term name'],
         'domain_of': ['EntityAttributeValue',
                       'ControlledTermValue',
                       'ControlledVocabularyTermValue']} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })
    unit_cv_id: Optional[str] = Field(default=None, description="""The unit of the quantity, expressed as a CURIE from the Unit Ontology.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_cv_id',
         'aliases': ['unit term ID', 'unit PID'],
         'domain_of': ['UnitMixin']} })
    unit_cv_label: Optional[str] = Field(default=None, description="""The unit of a quantity, expressed as the term name of a term from the Unit Ontology or UCUM.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_cv_label',
         'aliases': ['unit term name'],
         'domain_of': ['UnitMixin']} })
    unit_string: Optional[str] = Field(default=None, description="""Links a QuantityValue to a unit. Units should be taken from the UCUM unit collection or the Unit Ontology. This field should only be used if the unit is not present in one of those sources.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_string',
         'aliases': ['scale'],
         'domain_of': ['UnitMixin'],
         'mappings': ['nmdc:unit', 'qud:unit', 'schema:unitCode', 'UO:0000000']} })


class QuantityValue(AttributeValue, UnitMixin):
    """
    A simple quantity, e.g. 2 cm.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:QuantityValue',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'mappings': ['schema:QuantityValue'],
         'mixins': ['UnitMixin'],
         'slot_usage': {'numeric_value': {'name': 'numeric_value', 'required': True},
                        'raw_value': {'description': 'Unnormalized atomic string '
                                                     'representation, suggested syntax '
                                                     '{number} {unit}',
                                      'name': 'raw_value'},
                        'type': {'ifabsent': 'AttributeValueType("QuantityValue")',
                                 'name': 'type'}}})

    numeric_value: float = Field(default=..., description="""The numerical part of a quantity value.""", json_schema_extra = { "linkml_meta": {'alias': 'numeric_value',
         'domain_of': ['EntityAttributeValue', 'QuantityValue'],
         'mappings': ['nmdc:numeric_value', 'qud:quantityValue', 'schema:value']} })
    unit_cv_id: Optional[str] = Field(default=None, description="""The unit of the quantity, expressed as a CURIE from the Unit Ontology.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_cv_id',
         'aliases': ['unit term ID', 'unit PID'],
         'domain_of': ['UnitMixin']} })
    unit_cv_label: Optional[str] = Field(default=None, description="""The unit of a quantity, expressed as the term name of a term from the Unit Ontology or UCUM.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_cv_label',
         'aliases': ['unit term name'],
         'domain_of': ['UnitMixin']} })
    unit_string: Optional[str] = Field(default=None, description="""Links a QuantityValue to a unit. Units should be taken from the UCUM unit collection or the Unit Ontology. This field should only be used if the unit is not present in one of those sources.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_string',
         'aliases': ['scale'],
         'domain_of': ['UnitMixin'],
         'mappings': ['nmdc:unit', 'qud:unit', 'schema:unitCode', 'UO:0000000']} })
    raw_value: Optional[str] = Field(default=None, description="""Unnormalized atomic string representation, suggested syntax {number} {unit}""", json_schema_extra = { "linkml_meta": {'alias': 'raw_value',
         'domain_of': ['AttributeValue'],
         'examples': [{'value': '2 cm'},
                      {'value': '2 to 5m'},
                      {'value': '37-39 degrees celcius'},
                      {'value': 'Regulation of glucose biosynthesis.'}],
         'mappings': ['nmdc:raw_value']} })
    type: Optional[AttributeValueType] = Field(default='QuantityValue', description="""The type of value being represented - e.g. QuantityValue, TextValue, DateTimeValue, ControlledVocabularyTermValue, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence'],
         'ifabsent': 'AttributeValueType("QuantityValue")'} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class QuantityRangeValue(AttributeValue, UnitMixin):
    """
    A numerical range, e.g. 5-7 cm.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'mappings': ['schema:QuantityRangeValue'],
         'mixins': ['UnitMixin'],
         'slot_usage': {'maximum_numeric_value': {'name': 'maximum_numeric_value',
                                                  'required': True},
                        'minimum_numeric_value': {'name': 'minimum_numeric_value',
                                                  'required': True},
                        'raw_value': {'description': 'Unnormalized atomic string '
                                                     'representation, suggested syntax '
                                                     '{minimum_number}-{maximum_number} '
                                                     '{unit}',
                                      'name': 'raw_value'},
                        'type': {'ifabsent': 'AttributeValueType("QuantityRangeValue")',
                                 'name': 'type'}}})

    maximum_numeric_value: float = Field(default=..., description="""The maximum value part, expressed as number, of the quantity value when the value covers a range.""", json_schema_extra = { "linkml_meta": {'alias': 'maximum_numeric_value',
         'domain_of': ['EntityAttributeValue', 'QuantityRangeValue'],
         'mappings': ['nmdc:maximum_numeric_value']} })
    minimum_numeric_value: float = Field(default=..., description="""The minimum value part, expressed as number, of the quantity value when the value covers a range.""", json_schema_extra = { "linkml_meta": {'alias': 'minimum_numeric_value',
         'domain_of': ['EntityAttributeValue', 'QuantityRangeValue'],
         'mappings': ['nmdc:minimum_numeric_value']} })
    unit_cv_id: Optional[str] = Field(default=None, description="""The unit of the quantity, expressed as a CURIE from the Unit Ontology.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_cv_id',
         'aliases': ['unit term ID', 'unit PID'],
         'domain_of': ['UnitMixin']} })
    unit_cv_label: Optional[str] = Field(default=None, description="""The unit of a quantity, expressed as the term name of a term from the Unit Ontology or UCUM.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_cv_label',
         'aliases': ['unit term name'],
         'domain_of': ['UnitMixin']} })
    unit_string: Optional[str] = Field(default=None, description="""Links a QuantityValue to a unit. Units should be taken from the UCUM unit collection or the Unit Ontology. This field should only be used if the unit is not present in one of those sources.""", json_schema_extra = { "linkml_meta": {'alias': 'unit_string',
         'aliases': ['scale'],
         'domain_of': ['UnitMixin'],
         'mappings': ['nmdc:unit', 'qud:unit', 'schema:unitCode', 'UO:0000000']} })
    raw_value: Optional[str] = Field(default=None, description="""Unnormalized atomic string representation, suggested syntax {minimum_number}-{maximum_number} {unit}""", json_schema_extra = { "linkml_meta": {'alias': 'raw_value',
         'domain_of': ['AttributeValue'],
         'examples': [{'value': '2 cm'},
                      {'value': '2 to 5m'},
                      {'value': '37-39 degrees celcius'},
                      {'value': 'Regulation of glucose biosynthesis.'}],
         'mappings': ['nmdc:raw_value']} })
    type: Optional[AttributeValueType] = Field(default='QuantityRangeValue', description="""The type of value being represented - e.g. QuantityValue, TextValue, DateTimeValue, ControlledVocabularyTermValue, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence'],
         'ifabsent': 'AttributeValueType("QuantityRangeValue")'} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class DateTimeValue(AttributeValue):
    """
    A date or date and time value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'nmdc:DateTimeValue',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'slot_usage': {'date_time': {'name': 'date_time', 'required': True},
                        'type': {'ifabsent': 'AttributeValueType("DateTimeValue")',
                                 'name': 'type'}}})

    date_time: str = Field(default=..., description="""A date or date and time, expressed in ISO 8601 format with timezone indicators where appropriate.  The date or date/time value, expressed in ISO 8601-compatible form. Dates should be expressed as YYYY-MM-DD; times should be expressed as HH:MM:SS with optional milliseconds and an indication of the timezone.""", json_schema_extra = { "linkml_meta": {'alias': 'date_time',
         'aliases': ['date', 'time', 'timestamp'],
         'domain_of': ['EntityAttributeValue', 'DateTimeValue'],
         'examples': [{'value': '2025-11-09'}, {'value': '2025-09-16T22:48:54Z'}]} })
    raw_value: Optional[str] = Field(default=None, description="""The value that was specified for an annotation in its raw form; e.g. \"2 cm\" or \"2-4 cm\"""", json_schema_extra = { "linkml_meta": {'alias': 'raw_value',
         'domain_of': ['AttributeValue'],
         'examples': [{'value': '2 cm'},
                      {'value': '2 to 5m'},
                      {'value': '37-39 degrees celcius'},
                      {'value': 'Regulation of glucose biosynthesis.'}],
         'mappings': ['nmdc:raw_value']} })
    type: Optional[AttributeValueType] = Field(default='DateTimeValue', description="""The type of value being represented - e.g. QuantityValue, TextValue, DateTimeValue, ControlledVocabularyTermValue, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence'],
         'ifabsent': 'AttributeValueType("DateTimeValue")'} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class Geolocation(AttributeValue):
    """
    A normalized value for a location on the earth's surface. Should be expressed in decimal degrees.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'nmdc:GeolocationValue',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'mappings': ['schema:GeoCoordinates'],
         'slot_usage': {'latitude': {'name': 'latitude', 'required': True},
                        'longitude': {'name': 'longitude', 'required': True},
                        'raw_value': {'description': 'The raw value for a geolocation; '
                                                     'should follow {latitude} '
                                                     '{longitude}.',
                                      'name': 'raw_value'}}})

    latitude: float = Field(default=..., description="""The latitude portion of a geolocation.""", json_schema_extra = { "linkml_meta": {'alias': 'latitude', 'domain_of': ['EntityAttributeValue', 'Geolocation']} })
    longitude: float = Field(default=..., description="""The longitude portion of a geolocation.""", json_schema_extra = { "linkml_meta": {'alias': 'longitude', 'domain_of': ['EntityAttributeValue', 'Geolocation']} })
    raw_value: Optional[str] = Field(default=None, description="""The raw value for a geolocation; should follow {latitude} {longitude}.""", json_schema_extra = { "linkml_meta": {'alias': 'raw_value',
         'domain_of': ['AttributeValue'],
         'examples': [{'value': '2 cm'},
                      {'value': '2 to 5m'},
                      {'value': '37-39 degrees celcius'},
                      {'value': 'Regulation of glucose biosynthesis.'}],
         'mappings': ['nmdc:raw_value']} })
    type: Optional[AttributeValueType] = Field(default=None, description="""The type of value being represented - e.g. QuantityValue, TextValue, DateTimeValue, ControlledVocabularyTermValue, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence']} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class ControlledTermValue(AttributeValue):
    """
    A quality, described using a text string from a controlled vocabulary or enum.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'nmdc:ControlledTermValue',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'slot_usage': {'type': {'ifabsent': 'AttributeValueType("ControlledTermValue")',
                                 'name': 'type'},
                        'value_cv_label': {'name': 'value_cv_label', 'required': True}}})

    value_cv_label: str = Field(default=..., description="""For values that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'value_cv_label',
         'aliases': ['value term name'],
         'domain_of': ['EntityAttributeValue',
                       'ControlledTermValue',
                       'ControlledVocabularyTermValue']} })
    raw_value: Optional[str] = Field(default=None, description="""The value that was specified for an annotation in its raw form; e.g. \"2 cm\" or \"2-4 cm\"""", json_schema_extra = { "linkml_meta": {'alias': 'raw_value',
         'domain_of': ['AttributeValue'],
         'examples': [{'value': '2 cm'},
                      {'value': '2 to 5m'},
                      {'value': '37-39 degrees celcius'},
                      {'value': 'Regulation of glucose biosynthesis.'}],
         'mappings': ['nmdc:raw_value']} })
    type: Optional[AttributeValueType] = Field(default='ControlledTermValue', description="""The type of value being represented - e.g. QuantityValue, TextValue, DateTimeValue, ControlledVocabularyTermValue, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence'],
         'ifabsent': 'AttributeValueType("ControlledTermValue")'} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class ControlledVocabularyTermValue(AttributeValue):
    """
    A quality, described using a term from an ontology or schema with a stable persistent identifier.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'any_of': [{'slot_conditions': {'value_cv_id': {'name': 'value_cv_id',
                                                         'required': True}}},
                    {'slot_conditions': {'value_cv_label': {'name': 'value_cv_label',
                                                            'required': True}}}],
         'class_uri': 'nmdc:ControlledIdentifiedTermValue',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'slot_usage': {'type': {'ifabsent': 'AttributeValueType("ControlledVocabularyTermValue")',
                                 'name': 'type'}}})

    value_cv_label: Optional[str] = Field(default=None, description="""For values that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'value_cv_label',
         'aliases': ['value term name'],
         'domain_of': ['EntityAttributeValue',
                       'ControlledTermValue',
                       'ControlledVocabularyTermValue']} })
    value_cv_id: Optional[str] = Field(default=None, description="""For values that are in a controlled vocabulary (CV), this attribute should capture the controlled vocabulary ID for the value.""", json_schema_extra = { "linkml_meta": {'alias': 'value_cv_id',
         'aliases': ['value term ID', 'value PID'],
         'domain_of': ['EntityAttributeValue', 'ControlledVocabularyTermValue']} })
    raw_value: Optional[str] = Field(default=None, description="""The value that was specified for an annotation in its raw form; e.g. \"2 cm\" or \"2-4 cm\"""", json_schema_extra = { "linkml_meta": {'alias': 'raw_value',
         'domain_of': ['AttributeValue'],
         'examples': [{'value': '2 cm'},
                      {'value': '2 to 5m'},
                      {'value': '37-39 degrees celcius'},
                      {'value': 'Regulation of glucose biosynthesis.'}],
         'mappings': ['nmdc:raw_value']} })
    type: Optional[AttributeValueType] = Field(default='ControlledVocabularyTermValue', description="""The type of value being represented - e.g. QuantityValue, TextValue, DateTimeValue, ControlledVocabularyTermValue, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence'],
         'ifabsent': 'AttributeValueType("ControlledVocabularyTermValue")'} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class TextValue(AttributeValue):
    """
    A basic string value.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'nmdc:TextValue',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_attr_value',
         'slot_usage': {'text_value': {'description': 'The text value after undergoing '
                                                      'normalisation or '
                                                      'standardisation.',
                                       'name': 'text_value',
                                       'required': True},
                        'type': {'ifabsent': 'AttributeValueType("TextValue")',
                                 'name': 'type'}}})

    text_value: str = Field(default=..., description="""The text value after undergoing normalisation or standardisation.""", json_schema_extra = { "linkml_meta": {'alias': 'text_value',
         'aliases': ['value string', 'value text', 'string value'],
         'domain_of': ['EntityAttributeValue', 'TextValue']} })
    language: Optional[str] = Field(default=None, description="""Language of the text value.""", json_schema_extra = { "linkml_meta": {'alias': 'language',
         'domain_of': ['EntityAttributeValue',
                       'TextValue',
                       'ResourceDescription',
                       'ResourceTitle',
                       'Statement']} })
    raw_value: Optional[str] = Field(default=None, description="""The value that was specified for an annotation in its raw form; e.g. \"2 cm\" or \"2-4 cm\"""", json_schema_extra = { "linkml_meta": {'alias': 'raw_value',
         'domain_of': ['AttributeValue'],
         'examples': [{'value': '2 cm'},
                      {'value': '2 to 5m'},
                      {'value': '37-39 degrees celcius'},
                      {'value': 'Regulation of glucose biosynthesis.'}],
         'mappings': ['nmdc:raw_value']} })
    type: Optional[AttributeValueType] = Field(default='TextValue', description="""The type of value being represented - e.g. QuantityValue, TextValue, DateTimeValue, ControlledVocabularyTermValue, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence'],
         'ifabsent': 'AttributeValueType("TextValue")'} })
    attribute_cv_id: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term ID from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_id',
         'aliases': ['attribute term ID', 'attribute PID'],
         'domain_of': ['AttributeMixin']} })
    attribute_cv_label: Optional[str] = Field(default=None, description="""The attribute being represented. For attributes that are in a controlled vocabulary, ontology, or enumeration, this attribute should capture the term from the controlled vocabulary.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_cv_label',
         'aliases': ['attribute term name'],
         'domain_of': ['AttributeMixin']} })
    attribute_string: Optional[str] = Field(default=None, description="""The attribute being represented, as a text string. This field should only be used if the attribute is not represented in a controlled vocabulary, ontology, or enumeration.""", json_schema_extra = { "linkml_meta": {'alias': 'attribute_string',
         'aliases': ['attribute', 'tag'],
         'domain_of': ['AttributeMixin']} })
    entity_id: str = Field(default=..., description="""The database entity (sample, feature, protein, etc.) to which the attribute-value annotation refers.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class Contributor(Table):
    """
    Represents a contributor to a resource.

    Contributors must have a 'contributor_type', either 'Person' or 'Organization', and one of the 'name' fields: either 'given_name' and 'family_name' (for a person), or 'name' (for an organization or a person).

    The 'contributor_role' field takes values from the DataCite and CRediT contributor roles vocabularies. For more information on these resources and choosing appropriate roles, please see the following links:

    DataCite contributor roles: https://support.datacite.org/docs/datacite-metadata-schema-v44-recommended-and-optional-properties#7a-contributortype

    CRediT contributor role taxonomy: https://credit.niso.org

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'any_of': [{'slot_conditions': {'family_name': {'name': 'family_name',
                                                         'required': True},
                                         'given_name': {'name': 'given_name',
                                                        'required': True}}},
                    {'slot_conditions': {'name': {'name': 'name', 'required': True}}}],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'slot_usage': {'contributor_id': {'identifier': True,
                                           'name': 'contributor_id'}}})

    contributor_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contributor.
From the Entity table: entity_id where entity_type == 'Contributor'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_id',
         'domain_of': ['Contributor',
                       'ContributorAffiliation',
                       'Contributor_x_DataSource',
                       'Contributor_x_Role_x_Project']} })
    contributor_type: Optional[ContributorType] = Field(default=None, description="""Must be either 'Person' or 'Organization'.""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_type',
         'domain_of': ['Contributor'],
         'exact_mappings': ['DataCite:attributes.contributors.name_type',
                            'DataCite:attributes.creators.name_type'],
         'examples': [{'value': 'Person'}, {'value': 'Organization'}],
         'slot_uri': 'schema:@type'} })
    name: Optional[str] = Field(default=None, description="""Contributor name. For organizations, this should be the full (unabbreviated) name; can also be used for a person if the given name/family name format is not applicable.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'close_mappings': ['OSTI.ARTICLE:author', 'OSTI.ARTICLE:contributor'],
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'exact_mappings': ['JGI:organisms.pi.name', 'ORCID:name'],
         'examples': [{'value': 'National Institute of Mental Health'},
                      {'value': 'Madonna'},
                      {'value': 'Ransome the Clown'}],
         'related_mappings': ['DataCite:attributes.creators.name',
                              'DataCite:attributes.contributors.name'],
         'slot_uri': 'schema:name'} })
    given_name: Optional[str] = Field(default=None, description="""The given name(s) of the contributor.""", json_schema_extra = { "linkml_meta": {'alias': 'given_name',
         'domain_of': ['Contributor'],
         'examples': [{'value': 'Marionetta Cecille de la'},
                      {'value': 'Helena'},
                      {'value': 'Hubert George'}],
         'related_mappings': ['DataCite:attributes.contributors.givenName',
                              'DataCite:attributes.creators.givenName']} })
    family_name: Optional[str] = Field(default=None, description="""The family name(s) of the contributor.""", json_schema_extra = { "linkml_meta": {'alias': 'family_name',
         'domain_of': ['Contributor'],
         'examples': [{'value': 'Carte-Postale'},
                      {'value': 'Bonham Carter'},
                      {'value': 'Wells'}],
         'related_mappings': ['DataCite:attributes.contributors.familyName',
                              'DataCite:attributes.creators.familyName']} })


class ContributorAffiliation(LinkerTable):
    """
    Captures relationships between contributors where one contributor is part of another contributor, e.g. a member of a group or a group that is part of a larger organization.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'schema:affiliation',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'represents_relationship': True,
         'slot_usage': {'contributor_id': {'multivalued': True,
                                           'name': 'contributor_id'}}})

    contributor_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for a contributor.
From the Entity table: entity_id where entity_type == 'Contributor'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_id',
         'domain_of': ['Contributor',
                       'ContributorAffiliation',
                       'Contributor_x_DataSource',
                       'Contributor_x_Role_x_Project']} })
    affiliation_id: Optional[list[str]] = Field(default=None, description="""The ID of the organization to which a contributor belongs. Should be the ID of another contributor.""", json_schema_extra = { "linkml_meta": {'alias': 'affiliation_id',
         'aliases': ['affiliation_contributor_id'],
         'domain_of': ['ContributorAffiliation']} })


class ContributorXDataSource(LinkerTable):
    """
    Captures the people and/or organizations involved in producing a dataset; ideally the contributor_role field will capture how the contributor was involved.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'narrow_mappings': ['DataCite:attributes.contributors',
                             'DataCite:attributes.creators',
                             'ORCID:contributors',
                             'OSTI.ARTICLE:contributors',
                             'OSTI.ARTICLE:authors',
                             'JGI:organisms.pi'],
         'slot_usage': {'contributor_role': {'name': 'contributor_role',
                                             'required': False}}})

    contributor_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contributor.
From the Entity table: entity_id where entity_type == 'Contributor'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_id',
         'domain_of': ['Contributor',
                       'ContributorAffiliation',
                       'Contributor_x_DataSource',
                       'Contributor_x_Role_x_Project']} })
    data_source_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a data source.
From the Entity table: entity_id where entity_type == 'DataSource'.
""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_id',
         'domain_of': ['Entity',
                       'Contributor_x_DataSource',
                       'DataSource',
                       'DataSourceNew',
                       'DataSource_x_Description',
                       'DataSource_x_FundingReference',
                       'DataSource_x_License',
                       'DataSource_x_Title']} })
    contributor_role: Optional[ContributorRole] = Field(default=None, description="""Role(s) played by the contributor when working on the experiment. If more than one role was played, additional rows should be added to represent each role.""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_role',
         'domain_of': ['Contributor_x_DataSource', 'Contributor_x_Role_x_Project'],
         'slot_uri': 'schema:Role'} })


class ContributorXRoleXProject(Table):
    """
    Describes the participation of a contributor in a project; ideally the contributor_role field will capture how the contributor was involved.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'slot_usage': {'contributor_role': {'name': 'contributor_role',
                                             'required': False}}})

    contributor_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contributor.
From the Entity table: entity_id where entity_type == 'Contributor'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_id',
         'domain_of': ['Contributor',
                       'ContributorAffiliation',
                       'Contributor_x_DataSource',
                       'Contributor_x_Role_x_Project']} })
    project_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a project.
From the Entity table: entity_id where entity_type == 'Project'.
""", json_schema_extra = { "linkml_meta": {'alias': 'project_id',
         'domain_of': ['Contributor_x_Role_x_Project', 'Project']} })
    contributor_role: Optional[ContributorRole] = Field(default=None, description="""Role(s) played by the contributor when working on the experiment. If more than one role was played, additional rows should be added to represent each role.""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_role',
         'domain_of': ['Contributor_x_DataSource', 'Contributor_x_Role_x_Project'],
         'slot_uri': 'schema:Role'} })


class DataSource(Table):
    """
    The source for a resource, dataset, association, etc.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit'})

    data_source_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a data source.
From the Entity table: entity_id where entity_type == 'DataSource'.
""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_id',
         'domain_of': ['Entity',
                       'Contributor_x_DataSource',
                       'DataSource',
                       'DataSourceNew',
                       'DataSource_x_Description',
                       'DataSource_x_FundingReference',
                       'DataSource_x_License',
                       'DataSource_x_Title']} })
    name: Optional[str] = Field(default=None, description="""A string used as a name or title.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'slot_uri': 'schema:name'} })


class DataSourceNew(Table):
    """
    The source dataset from which data within the CDM was extracted. This might be an API query; a set of files downloaded from a website or uploaded by a user; a database dump; etc. A given data source should have either version information (e.g. a release number, like those used by UniProt or RefSeq) or an access date to allow the original raw data dump to be recapitulated.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'any_of': [{'slot_conditions': {'date_updated': {'name': 'date_updated',
                                                          'required': True}}},
                    {'slot_conditions': {'version': {'name': 'version',
                                                     'required': True}}}],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'slot_usage': {'data_source_id': {'identifier': True,
                                           'name': 'data_source_id'},
                        'name': {'description': 'The name of the data source.',
                                 'examples': [{'value': 'UniProt'},
                                              {'value': 'NMDC Runtime API'},
                                              {'value': 'NCBI RefSeq'}],
                                 'name': 'name'}}})

    data_source_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a data source.
From the Entity table: entity_id where entity_type == 'DataSource'.
""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_id',
         'domain_of': ['Entity',
                       'Contributor_x_DataSource',
                       'DataSource',
                       'DataSourceNew',
                       'DataSource_x_Description',
                       'DataSource_x_FundingReference',
                       'DataSource_x_License',
                       'DataSource_x_Title']} })
    name: Optional[str] = Field(default=None, description="""The name of the data source.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'examples': [{'value': 'UniProt'},
                      {'value': 'NMDC Runtime API'},
                      {'value': 'NCBI RefSeq'}],
         'slot_uri': 'schema:name'} })
    comments: Optional[str] = Field(default=None, description="""Freeform text providing extra information.""", json_schema_extra = { "linkml_meta": {'alias': 'comments',
         'domain_of': ['Association', 'DataSourceNew'],
         'examples': [{'value': 'This comment adds a lot of extra value!'}],
         'slot_uri': 'schema:comment'} })
    date_accessed: str = Field(default=..., description="""The date when the data was downloaded from the data source.""", json_schema_extra = { "linkml_meta": {'alias': 'date_accessed', 'domain_of': ['DataSourceNew']} })
    date_published: Optional[str] = Field(default=None, description="""The date when the data source was originally made public.""", json_schema_extra = { "linkml_meta": {'alias': 'date_published',
         'aliases': ['date_created'],
         'domain_of': ['DataSourceNew']} })
    date_updated: Optional[str] = Field(default=None, description="""The date when the data source was last updated.""", json_schema_extra = { "linkml_meta": {'alias': 'date_updated', 'domain_of': ['DataSourceNew']} })
    license: Optional[str] = Field(default=None, description="""Usage license for the resource. Use one of the SPDX license identifiers or provide a link to the license text if no SPDX ID is available.
""", json_schema_extra = { "linkml_meta": {'alias': 'license',
         'domain_of': ['DataSourceNew'],
         'exact_mappings': ['biolink:license'],
         'related_mappings': ['DataCite:attributes.rights_list'],
         'slot_uri': 'schema:license'} })
    publisher: Optional[str] = Field(default=None, description="""The publisher of the resource. For a dataset, this is the repository where it is stored.""", json_schema_extra = { "linkml_meta": {'alias': 'publisher',
         'domain_of': ['DataSourceNew'],
         'narrow_mappings': ['ORCID:url', 'OSTI.ARTICLE:site_url'],
         'slot_uri': 'schema:provider'} })
    resource_type: ResourceType = Field(default=..., description="""The broad type of the source data for this object. 'dataset' is currently the only valid value supported by this schema.""", json_schema_extra = { "linkml_meta": {'alias': 'resource_type',
         'domain_of': ['DataSourceNew'],
         'exact_mappings': ['OSTI.ARTICLE:product_type',
                            'OSTI.ARTICLE:workType',
                            'DataCite:attributes.types.schema_org'],
         'examples': [{'value': 'dataset'}],
         'narrow_mappings': ['OSTI.ARTICLE:dataset_type'],
         'slot_uri': 'schema:@type'} })
    url: Optional[str] = Field(default=None, description="""The URL from which the data was loaded.""", json_schema_extra = { "linkml_meta": {'alias': 'url', 'domain_of': ['DataSourceNew', 'License', 'Protocol']} })
    version: Optional[str] = Field(default=None, description="""The version of the resource. This must be an absolute version, not a relative version like 'latest'.""", json_schema_extra = { "linkml_meta": {'alias': 'version',
         'domain_of': ['DataSourceNew', 'Protocol'],
         'exact_mappings': ['DataCite:attributes.version'],
         'examples': [{'value': '5'},
                      {'value': '1.2.1'},
                      {'value': '20220405'},
                      {'value': 'v1.5.3'}],
         'slot_uri': 'schema:version'} })


class DataSourceXDescription(LinkerTable):
    """
    Links a data source to a description (e.g. the abstract or a free text description).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit'})

    data_source_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a data source.
From the Entity table: entity_id where entity_type == 'DataSource'.
""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_id',
         'domain_of': ['Entity',
                       'Contributor_x_DataSource',
                       'DataSource',
                       'DataSourceNew',
                       'DataSource_x_Description',
                       'DataSource_x_FundingReference',
                       'DataSource_x_License',
                       'DataSource_x_Title']} })
    resource_description_id: str = Field(default=..., description="""Unique identifier for a description for a resource.""", json_schema_extra = { "linkml_meta": {'alias': 'resource_description_id',
         'domain_of': ['DataSource_x_Description', 'ResourceDescription']} })


class DataSourceXFundingReference(LinkerTable):
    """
    Links a data source to a funding reference.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit'})

    data_source_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a data source.
From the Entity table: entity_id where entity_type == 'DataSource'.
""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_id',
         'domain_of': ['Entity',
                       'Contributor_x_DataSource',
                       'DataSource',
                       'DataSourceNew',
                       'DataSource_x_Description',
                       'DataSource_x_FundingReference',
                       'DataSource_x_License',
                       'DataSource_x_Title']} })
    funding_reference_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a specific source of funding -- e.g. a grant or award.
From the Entity table: entity_id where entity_type == 'FundingReference'.
""", json_schema_extra = { "linkml_meta": {'alias': 'funding_reference_id',
         'domain_of': ['DataSource_x_FundingReference', 'FundingReference']} })


class DataSourceXLicense(LinkerTable):
    """
    Links a data source to a license.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit'})

    data_source_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a data source.
From the Entity table: entity_id where entity_type == 'DataSource'.
""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_id',
         'domain_of': ['Entity',
                       'Contributor_x_DataSource',
                       'DataSource',
                       'DataSourceNew',
                       'DataSource_x_Description',
                       'DataSource_x_FundingReference',
                       'DataSource_x_License',
                       'DataSource_x_Title']} })
    license_id: str = Field(default=..., description="""Unique identifier for a license.
""", json_schema_extra = { "linkml_meta": {'alias': 'license_id', 'domain_of': ['DataSource_x_License', 'License']} })


class DataSourceXTitle(LinkerTable):
    """
    Links a data source to a title.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit'})

    data_source_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a data source.
From the Entity table: entity_id where entity_type == 'DataSource'.
""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_id',
         'domain_of': ['Entity',
                       'Contributor_x_DataSource',
                       'DataSource',
                       'DataSourceNew',
                       'DataSource_x_Description',
                       'DataSource_x_FundingReference',
                       'DataSource_x_License',
                       'DataSource_x_Title']} })
    resource_title_id: str = Field(default=..., description="""Unique identifier for a title for a resource.""", json_schema_extra = { "linkml_meta": {'alias': 'resource_title_id',
         'domain_of': ['DataSource_x_Title', 'ResourceTitle']} })


class FundingReference(Table):
    """
    Represents a funding source for a resource, including the funding body and the grant awarded.

    One (or more) of the fields `grant_id`, `grant_url`, or `funder.organization_name` is required; others are optional.

    Recommended resources for organization identifiers include:
      - Research Organization Registry, http://ror.org
      - International Standard Name Identifier, https://isni.org
      - Crossref Funder Registry, https://www.crossref.org/services/funder-registry/ (to be subsumed into ROR)

    Some organizations may have a digital object identifier (DOI).

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'any_of': [{'slot_conditions': {'grant_id': {'name': 'grant_id',
                                                      'required': True}}},
                    {'slot_conditions': {'grant_url': {'name': 'grant_url',
                                                       'required': True}}},
                    {'slot_conditions': {'funder': {'name': 'funder',
                                                    'required': True}}}],
         'class_uri': 'schema:MonetaryGrant',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'slot_usage': {'funding_reference_id': {'identifier': True,
                                                 'name': 'funding_reference_id'}}})

    funding_reference_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a specific source of funding -- e.g. a grant or award.
From the Entity table: entity_id where entity_type == 'FundingReference'.
""", json_schema_extra = { "linkml_meta": {'alias': 'funding_reference_id',
         'domain_of': ['DataSource_x_FundingReference', 'FundingReference']} })
    funder: Optional[str] = Field(default=None, description="""The funder for the grant or award.""", json_schema_extra = { "linkml_meta": {'alias': 'funder',
         'domain_of': ['FundingReference'],
         'slot_uri': 'schema:funder'} })
    grant_id: Optional[str] = Field(default=None, description="""Code for the grant, assigned by the funder.""", json_schema_extra = { "linkml_meta": {'alias': 'grant_id',
         'domain_of': ['FundingReference'],
         'examples': [{'value': '1296'},
                      {'value': 'CBET-0756451'},
                      {'value': 'DOI:10.46936/10.25585/60000745'}],
         'slot_uri': 'schema:identifier'} })
    grant_title: Optional[str] = Field(default=None, description="""Title for the grant.""", json_schema_extra = { "linkml_meta": {'alias': 'grant_title',
         'domain_of': ['FundingReference'],
         'examples': [{'value': 'Metagenomic analysis of the rhizosphere of three '
                                'biofuel crops at the KBS intensive site'}],
         'slot_uri': 'schema:name'} })
    grant_url: Optional[str] = Field(default=None, description="""URL for the grant.""", json_schema_extra = { "linkml_meta": {'alias': 'grant_url',
         'domain_of': ['FundingReference'],
         'examples': [{'value': 'https://genome.jgi.doe.gov/portal/Metanaintenssite/Metanaintenssite.info.html'}],
         'slot_uri': 'schema:url'} })

    @field_validator('grant_url')
    def pattern_grant_url(cls, v):
        pattern=re.compile(r"^[a-zA-Z0-9.-_]+:\S")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid grant_url format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid grant_url format: {v}"
            raise ValueError(err_msg)
        return v


class License(Table):
    """
    License information for the resource.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'any_of': [{'slot_conditions': {'id': {'name': 'id', 'required': True}}},
                    {'slot_conditions': {'url': {'name': 'url', 'required': True}}}],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'slot_usage': {'license_id': {'identifier': True, 'name': 'license_id'}}})

    license_id: str = Field(default=..., description="""Unique identifier for a license.
""", json_schema_extra = { "linkml_meta": {'alias': 'license_id', 'domain_of': ['DataSource_x_License', 'License']} })
    id: Optional[str] = Field(default=None, description="""CURIE for the license.""", json_schema_extra = { "linkml_meta": {'alias': 'id', 'domain_of': ['License']} })
    name: Optional[str] = Field(default=None, description="""String representing the license, from the SPDX license identifiers at https://spdx.org/licenses/.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'examples': [{'value': 'CC-BY-NC-ND-4.0'}, {'value': 'Apache-2.0'}]} })
    url: Optional[str] = Field(default=None, description="""URL for the license.""", json_schema_extra = { "linkml_meta": {'alias': 'url',
         'domain_of': ['DataSourceNew', 'License', 'Protocol'],
         'examples': [{'value': 'https://jgi.doe.gov/user-programs/pmo-overview/policies/'}]} })


class Project(Table):
    """
    Administrative unit for collecting data related to a certain topic, location, data type, grant funding, and so on.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['proposal',
                     'research proposal',
                     'research study',
                     'investigation',
                     'project',
                     'study',
                     'umbrella project',
                     'research initiative'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'slot_usage': {'project_id': {'identifier': True, 'name': 'project_id'}}})

    project_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a project.
From the Entity table: entity_id where entity_type == 'Project'.
""", json_schema_extra = { "linkml_meta": {'alias': 'project_id',
         'domain_of': ['Contributor_x_Role_x_Project', 'Project']} })
    description: Optional[str] = Field(default=None, description="""Brief text description of the project.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })


class Publication(Table):
    """
    A publication (e.g. journal article).
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit',
         'slot_usage': {'publication_id': {'identifier': True,
                                           'name': 'publication_id'}}})

    publication_id: str = Field(default=..., description="""Unique identifier for a publication - e.g. PMID, DOI, URL, etc.""", json_schema_extra = { "linkml_meta": {'alias': 'publication_id', 'domain_of': ['Publication']} })


class ResourceDescription(Table):
    """
    Textual information about the resource being represented.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit'})

    resource_description_id: str = Field(default=..., description="""Unique identifier for a description for a resource.""", json_schema_extra = { "linkml_meta": {'alias': 'resource_description_id',
         'domain_of': ['DataSource_x_Description', 'ResourceDescription']} })
    description_text: str = Field(default=..., description="""The text content of the informational element.""", json_schema_extra = { "linkml_meta": {'alias': 'description_text',
         'domain_of': ['ResourceDescription'],
         'examples': [{'value': 'This is the most interesting dataset ever to earn a '
                                'DOI.'}]} })
    description_type: Optional[DescriptionType] = Field(default=None, description="""The type of text being represented.""", json_schema_extra = { "linkml_meta": {'alias': 'description_type',
         'domain_of': ['ResourceDescription'],
         'examples': [{'value': 'abstract'},
                      {'value': 'description'},
                      {'value': 'summary'}]} })
    language: Optional[str] = Field(default=None, description="""The language in which the description is written, using the appropriate IETF BCP-47 notation.""", json_schema_extra = { "linkml_meta": {'alias': 'language',
         'domain_of': ['EntityAttributeValue',
                       'TextValue',
                       'ResourceDescription',
                       'ResourceTitle',
                       'Statement'],
         'examples': [{'value': 'ru-Cyrl'}, {'value': 'fr'}]} })


class ResourceTitle(Table):
    """
    Represents the title or name of a resource, the type of that title, and the language used (if appropriate).

    The `title` field is required; `title_type` is only necessary if the text is not the primary title.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_credit'})

    resource_title_id: str = Field(default=..., description="""Unique identifier for a title for a resource.""", json_schema_extra = { "linkml_meta": {'alias': 'resource_title_id',
         'domain_of': ['DataSource_x_Title', 'ResourceTitle']} })
    language: Optional[str] = Field(default=None, description="""The language in which the title is written, using the appropriate IETF BCP-47 notation.""", json_schema_extra = { "linkml_meta": {'alias': 'language',
         'domain_of': ['EntityAttributeValue',
                       'TextValue',
                       'ResourceDescription',
                       'ResourceTitle',
                       'Statement'],
         'examples': [{'value': 'ru-Cyrl'}, {'value': 'fr'}]} })
    title: str = Field(default=..., description="""A string used as a title for a resource.""", json_schema_extra = { "linkml_meta": {'alias': 'title',
         'domain_of': ['ResourceTitle'],
         'examples': [{'value': 'Amaranthus hypochondriacus genome'},
                      {'value': 'Геном амаранта ипохондрического'}],
         'slot_uri': 'schema:name'} })
    title_type: Optional[TitleType] = Field(default=None, description="""A descriptor for the title for cases where the contents of the `title` field is not the primary name or title.""", json_schema_extra = { "linkml_meta": {'alias': 'title_type',
         'domain_of': ['ResourceTitle'],
         'examples': [{'value': 'subtitle'},
                      {'value': 'alternative_title'},
                      {'value': 'translated_title'},
                      {'value': 'other'}]} })


class Prefix(Table):
    """
    Maps CURIEs to URIs
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'class_uri': 'sh:PrefixDeclaration',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_ontology'})

    prefix: Optional[str] = Field(default=None, description="""A standardized prefix such as 'GO' or 'rdf' or 'FlyBase'.""", json_schema_extra = { "linkml_meta": {'alias': 'prefix', 'domain_of': ['Prefix'], 'slot_uri': 'sh:prefix'} })
    base: Optional[str] = Field(default=None, description="""The base URI a prefix will expand to.""", json_schema_extra = { "linkml_meta": {'alias': 'base', 'domain_of': ['Prefix'], 'slot_uri': 'sh:namespace'} })


class Statement(Table):
    """
    Represents an RDF triple, a statement in the form \"_subject_ _predicate_ _object_\" or \"_subject_ _predicate_ _value_\".

    See [Semantic SQL](https://incatools.github.io/semantic-sql/) for more information on the contents of this table and how it is populated.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['triple'],
         'class_uri': 'rdf:Statement',
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_ontology',
         'slot_usage': {'object': {'name': 'object', 'range': 'local_curie'},
                        'predicate': {'name': 'predicate', 'range': 'local_curie'},
                        'subject': {'name': 'subject', 'range': 'local_curie'}}})

    subject: Optional[str] = Field(default=None, description="""The subject of the statement""", json_schema_extra = { "linkml_meta": {'alias': 'subject',
         'aliases': ['about', 'source', 'head', 'subject_id'],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:subject',
         'todos': ['set range appropriately for ontology and association use']} })
    predicate: Optional[str] = Field(default=None, description="""The predicate of the statement""", json_schema_extra = { "linkml_meta": {'alias': 'predicate',
         'aliases': ['relationship', 'relationship type', 'property', 'predicate_id'],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:predicate',
         'todos': ['set range appropriately for ontology and association use']} })
    object: Optional[str] = Field(default=None, description="""Note the range of this slot is always a node. If the triple represents a literal, the \"value\" field will be populated instead.""", json_schema_extra = { "linkml_meta": {'alias': 'object',
         'aliases': ['target', 'sink', 'tail', 'object_id'],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:object',
         'todos': ['set range appropriately for ontology and association use']} })
    value: Optional[str] = Field(default=None, description="""Note the range of this slot is always a string. Only used if the triple represents a literal assertion""", json_schema_extra = { "linkml_meta": {'alias': 'value',
         'close_mappings': ['rdf:object'],
         'domain_of': ['Statement',
                       'ExperimentCondition',
                       'Measurement',
                       'ProtocolInput',
                       'ProtocolOutput'],
         'slot_uri': 'rdf:object'} })
    datatype: Optional[str] = Field(default=None, description="""the rdf datatype of the value, for example, xsd:string or xsd:float.""", json_schema_extra = { "linkml_meta": {'alias': 'datatype',
         'comments': ['only used when value is populated'],
         'domain_of': ['Statement']} })
    language: Optional[str] = Field(default=None, description="""the human language in which the value is encoded, e.g. 'en'""", json_schema_extra = { "linkml_meta": {'alias': 'language',
         'comments': ['only used when value is populated'],
         'domain_of': ['EntityAttributeValue',
                       'TextValue',
                       'ResourceDescription',
                       'ResourceTitle',
                       'Statement'],
         'todos': ['use an enum (rather than a string)']} })


class EntailedEdge(Table):
    """
    A relation graph edge that is inferred. This table contains links between the nodes that appear as subjects in the [Statement](Statement) table. The graph contains all possible links between nodes and is created using a reasoner such as [relation-graph](https://github.com/balhoff/relation-graph) to materialise inferrred links.

    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['- It is common to populate this via a procedure external to the '
                      'database, e.g balhoff/relation-graph'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_ontology',
         'see_also': ['https://github.com/balhoff/relation-graph'],
         'slot_usage': {'object': {'name': 'object', 'range': 'local_curie'},
                        'predicate': {'name': 'predicate', 'range': 'local_curie'},
                        'subject': {'name': 'subject', 'range': 'local_curie'}}})

    subject: Optional[str] = Field(default=None, description="""The subject of the statement""", json_schema_extra = { "linkml_meta": {'alias': 'subject',
         'aliases': ['about', 'source', 'head', 'subject_id'],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:subject',
         'todos': ['set range appropriately for ontology and association use']} })
    predicate: Optional[str] = Field(default=None, description="""The predicate of the statement""", json_schema_extra = { "linkml_meta": {'alias': 'predicate',
         'aliases': ['relationship', 'relationship type', 'property', 'predicate_id'],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:predicate',
         'todos': ['set range appropriately for ontology and association use']} })
    object: Optional[str] = Field(default=None, description="""Note the range of this slot is always a node. If the triple represents a literal, the \"value\" field will be populated instead.""", json_schema_extra = { "linkml_meta": {'alias': 'object',
         'aliases': ['target', 'sink', 'tail', 'object_id'],
         'domain_of': ['Association', 'Statement', 'EntailedEdge'],
         'slot_uri': 'rdf:object',
         'todos': ['set range appropriately for ontology and association use']} })


class Experiment(Table):
    """
    A discrete scientific procedure undertaken to make a discovery, test a hypothesis, or demonstrate a known fact. The protocol_id links to the workflow followed to perform the experiment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'description': {'description': 'Brief explanation of what was '
                                                       'done.',
                                        'name': 'description'},
                        'experiment_id': {'identifier': True, 'name': 'experiment_id'},
                        'name': {'description': 'Name or title of the experiment.',
                                 'name': 'name'}}})

    experiment_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an experiment.""", json_schema_extra = { "linkml_meta": {'alias': 'experiment_id',
         'domain_of': ['Experiment', 'ExperimentCondition'],
         'slot_uri': 'CDM:experiment_id'} })
    protocol_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a protocol.
From the Entity table: entity_id where entity_type == 'Protocol'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_id',
         'domain_of': ['Cluster',
                       'Experiment',
                       'OrderedProtocolStep',
                       'Protocol',
                       'ProtocolExecution',
                       'ProtocolVariable',
                       'Feature'],
         'slot_uri': 'CDM:protocol_id'} })
    name: Optional[str] = Field(default=None, description="""Name or title of the experiment.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Brief explanation of what was done.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    created_at: Optional[str] = Field(default=None, description="""The start time of the experiment.""", json_schema_extra = { "linkml_meta": {'alias': 'created_at',
         'domain_of': ['Event', 'Experiment', 'MeasurementSet', 'ProtocolExecution']} })


class ExperimentCondition(Table):
    """
    A measurement, reagent, or description of one aspect of the environment used in an experiment; examples include temperature; aerobic or anaerobic conditions; presence of a chemical in the environment. Used to describe the context, conditions, or set-up of an experiment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['condition',
                     'environment condition',
                     'environmental condition',
                     'experiment condition',
                     'experimental condition',
                     'environment context',
                     'environmental context',
                     'experiment context',
                     'experimental context'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'experiment_condition_id': {'identifier': True,
                                                    'name': 'experiment_condition_id'}}})

    experiment_condition_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an experiment condition.""", json_schema_extra = { "linkml_meta": {'alias': 'experiment_condition_id',
         'domain_of': ['ExperimentCondition', 'ExperimentConditionSet'],
         'slot_uri': 'CDM:experiment_condition_id'} })
    experiment_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an experiment.""", json_schema_extra = { "linkml_meta": {'alias': 'experiment_id',
         'domain_of': ['Experiment', 'ExperimentCondition'],
         'slot_uri': 'CDM:experiment_id'} })
    variable_id: str = Field(default=..., description="""Internal CDM unique identifier for a variable.""", json_schema_extra = { "linkml_meta": {'alias': 'variable_id',
         'domain_of': ['ExperimentCondition',
                       'MeasurementSet',
                       'ProtocolVariable',
                       'Variable',
                       'VariableValue'],
         'slot_uri': 'CDM:variable_id'} })
    value: Optional[str] = Field(default=None, description="""A value; units should not be included.""", json_schema_extra = { "linkml_meta": {'alias': 'value',
         'domain_of': ['Statement',
                       'ExperimentCondition',
                       'Measurement',
                       'ProtocolInput',
                       'ProtocolOutput']} })


class ExperimentConditionSet(Table):
    """
    A unique combination of experimental conditions and entities that are used in a specific experiment. One experiment condition set is expected to comprise of multiple ExperimentConditions.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['environment conditions',
                     'environmental conditions',
                     'experiment conditions',
                     'experimental conditions'],
         'comments': ['Grouping table to collate unique sets of '
                      '`experiment_condition_id`s.'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol'})

    experiment_condition_set_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a set of experimental conditions.""", json_schema_extra = { "linkml_meta": {'alias': 'experiment_condition_set_id',
         'domain_of': ['ExperimentConditionSet', 'Measurement'],
         'slot_uri': 'CDM:experiment_condition_set_id'} })
    experiment_condition_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an experiment condition.""", json_schema_extra = { "linkml_meta": {'alias': 'experiment_condition_id',
         'domain_of': ['ExperimentCondition', 'ExperimentConditionSet'],
         'slot_uri': 'CDM:experiment_condition_id'} })


class Measurement(Table):
    """
    The value of a specified variable_id under the specified conditions.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['computed measurement',
                     'matrix entry',
                     'observation',
                     'result',
                     'results'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'measurement_id': {'identifier': True,
                                           'name': 'measurement_id'}}})

    measurement_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a measurement.""", json_schema_extra = { "linkml_meta": {'alias': 'measurement_id',
         'domain_of': ['Measurement'],
         'slot_uri': 'CDM:measurement_id'} })
    measurement_set_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a specified variable in a specified experiment.""", json_schema_extra = { "linkml_meta": {'alias': 'measurement_set_id',
         'domain_of': ['Measurement', 'MeasurementSet'],
         'slot_uri': 'CDM:measurement_set_id'} })
    experiment_condition_set_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a set of experimental conditions.""", json_schema_extra = { "linkml_meta": {'alias': 'experiment_condition_set_id',
         'domain_of': ['ExperimentConditionSet', 'Measurement'],
         'slot_uri': 'CDM:experiment_condition_set_id'} })
    value: Optional[str] = Field(default=None, description="""The value for a given measurement set (a specified variable in a specified experiment) in the environmental conditions specified by experiment_condition_set_id.""", json_schema_extra = { "linkml_meta": {'alias': 'value',
         'domain_of': ['Statement',
                       'ExperimentCondition',
                       'Measurement',
                       'ProtocolInput',
                       'ProtocolOutput']} })


class MeasurementSet(Table):
    """
    Grouping table to collate a set of protocol outputs by variable, quality, and timestamp.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['experiment variable measurement set'],
         'comments': ['Grouping table to collate a set of protocol outputs by '
                      'variable, quality, and timestamp.'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'measurement_set_id': {'identifier': True,
                                               'name': 'measurement_set_id'}}})

    measurement_set_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a specified variable in a specified experiment.""", json_schema_extra = { "linkml_meta": {'alias': 'measurement_set_id',
         'domain_of': ['Measurement', 'MeasurementSet'],
         'slot_uri': 'CDM:measurement_set_id'} })
    variable_id: str = Field(default=..., description="""Internal CDM unique identifier for a variable.""", json_schema_extra = { "linkml_meta": {'alias': 'variable_id',
         'domain_of': ['ExperimentCondition',
                       'MeasurementSet',
                       'ProtocolVariable',
                       'Variable',
                       'VariableValue'],
         'slot_uri': 'CDM:variable_id'} })
    quality: Optional[str] = Field(default=None, description="""A quality score for measurement.""", json_schema_extra = { "linkml_meta": {'alias': 'quality', 'domain_of': ['MeasurementSet']} })
    created_at: Optional[str] = Field(default=None, description="""Timestamp for the measurement.""", json_schema_extra = { "linkml_meta": {'alias': 'created_at',
         'aliases': ['timestamp'],
         'domain_of': ['Event', 'Experiment', 'MeasurementSet', 'ProtocolExecution']} })


class OrderedProtocolStep(Table):
    """
    A list of the steps in a protocol; the step_index indicates the order in which they should be executed.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol'})

    protocol_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a protocol.
From the Entity table: entity_id where entity_type == 'Protocol'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_id',
         'domain_of': ['Cluster',
                       'Experiment',
                       'OrderedProtocolStep',
                       'Protocol',
                       'ProtocolExecution',
                       'ProtocolVariable',
                       'Feature'],
         'slot_uri': 'CDM:protocol_id'} })
    protocol_step_id: str = Field(default=..., description="""Internal CDM unique identifier for a step in a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_step_id',
         'domain_of': ['OrderedProtocolStep', 'ProtocolStep'],
         'slot_uri': 'CDM:protocol_step_id'} })
    step_index: int = Field(default=..., description="""The number of the step in an ordered progression.""", json_schema_extra = { "linkml_meta": {'alias': 'step_index', 'domain_of': ['OrderedProtocolStep']} })


class Parameter(Table):
    """
    A parameter in a protocol. Currently specific to computational protocols.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'parameter_id': {'aliases': ['protocol_parameter_id'],
                                         'identifier': True,
                                         'name': 'parameter_id'}}})

    parameter_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a parameter of a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'parameter_id',
         'aliases': ['protocol_parameter_id'],
         'domain_of': ['Parameter', 'ProtocolInput'],
         'slot_uri': 'CDM:parameter_id'} })
    name: Optional[str] = Field(default=None, description="""A string used as a name or title.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Brief textual definition or description.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    value_type: Optional[str] = Field(default=None, description="""The type(s) of the value.""", json_schema_extra = { "linkml_meta": {'alias': 'value_type',
         'domain_of': ['Parameter', 'Variable', 'VariableValue'],
         'examples': [{'value': 'boolean'},
                      {'value': 'SomeSpecifiedEnum'},
                      {'value': 'integer'}]} })
    required: Optional[bool] = Field(default=None, description="""Whether or not this parameter must be supplied.""", json_schema_extra = { "linkml_meta": {'alias': 'required', 'domain_of': ['Parameter']} })
    cardinality: Optional[str] = Field(default=None, description="""The cardinality of the parameter.""", json_schema_extra = { "linkml_meta": {'alias': 'cardinality',
         'domain_of': ['Parameter'],
         'examples': [{'value': '0 .. 1'}, {'value': '1 .. n'}, {'value': '0 .. 4'}]} })
    default: Optional[str] = Field(default=None, description="""The default value for the parameter if a value is not supplied.""", json_schema_extra = { "linkml_meta": {'alias': 'default',
         'domain_of': ['Parameter'],
         'examples': [{'value': 'false'}, {'value': '42'}]} })
    parameter_type: Optional[ProtocolParameterType] = Field(default=None, description="""Whether the parameter applies to the protocol input or output.""", json_schema_extra = { "linkml_meta": {'alias': 'parameter_type',
         'domain_of': ['Parameter'],
         'examples': [{'value': 'input'}, {'value': 'output'}]} })


class Protocol(Table):
    """
    A defined method or set of methods.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'protocol_id': {'identifier': True, 'name': 'protocol_id'}}})

    protocol_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a protocol.
From the Entity table: entity_id where entity_type == 'Protocol'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_id',
         'domain_of': ['Cluster',
                       'Experiment',
                       'OrderedProtocolStep',
                       'Protocol',
                       'ProtocolExecution',
                       'ProtocolVariable',
                       'Feature'],
         'slot_uri': 'CDM:protocol_id'} })
    name: Optional[str] = Field(default=None, description="""A string used as a name or title.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Brief text description of the protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    doi: Optional[str] = Field(default=None, description="""The DOI for a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'doi', 'domain_of': ['Protocol']} })
    url: Optional[str] = Field(default=None, description="""The URL for a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'url', 'domain_of': ['DataSourceNew', 'License', 'Protocol']} })
    version: Optional[str] = Field(default=None, description="""The version of the protocol that has been used.""", json_schema_extra = { "linkml_meta": {'alias': 'version', 'domain_of': ['DataSourceNew', 'Protocol']} })


class ProtocolExecution(Table):
    """
    An instance of executing a protocol. Used for
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'protocol_execution_id': {'identifier': True,
                                                  'name': 'protocol_execution_id'}}})

    protocol_execution_id: str = Field(default=..., description="""Internal CDM unique identifier for an execution of a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_execution_id',
         'domain_of': ['ProtocolExecution', 'ProtocolInput'],
         'slot_uri': 'CDM:protocol_execution_id'} })
    protocol_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a protocol.
From the Entity table: entity_id where entity_type == 'Protocol'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_id',
         'domain_of': ['Cluster',
                       'Experiment',
                       'OrderedProtocolStep',
                       'Protocol',
                       'ProtocolExecution',
                       'ProtocolVariable',
                       'Feature'],
         'slot_uri': 'CDM:protocol_id'} })
    name: Optional[str] = Field(default=None, description="""A string used as a name or title.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Brief textual definition or description.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    created_at: Optional[str] = Field(default=None, description="""when the protocol was executed""", json_schema_extra = { "linkml_meta": {'alias': 'created_at',
         'aliases': ['timestamp'],
         'domain_of': ['Event', 'Experiment', 'MeasurementSet', 'ProtocolExecution']} })


class ProtocolInput(Table):
    """
    An input parameter for a protocol.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'protocol_input_id': {'identifier': True,
                                              'name': 'protocol_input_id'}}})

    parameter_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a parameter of a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'parameter_id',
         'domain_of': ['Parameter', 'ProtocolInput'],
         'slot_uri': 'CDM:parameter_id'} })
    protocol_input_id: str = Field(default=..., description="""Internal CDM unique identifier for the value of an input parameter for a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_input_id',
         'domain_of': ['ProtocolInput', 'ProtocolInputSet'],
         'slot_uri': 'CDM:protocol_input_id'} })
    protocol_execution_id: str = Field(default=..., description="""Internal CDM unique identifier for an execution of a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_execution_id',
         'domain_of': ['ProtocolExecution', 'ProtocolInput'],
         'slot_uri': 'CDM:protocol_execution_id'} })
    value: str = Field(default=..., description="""The value for a parameter of a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'value',
         'domain_of': ['Statement',
                       'ExperimentCondition',
                       'Measurement',
                       'ProtocolInput',
                       'ProtocolOutput']} })


class ProtocolInputSet(Table):
    """
    A set of input parameters for a protocol.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'protocol_input_set_id': {'identifier': True,
                                                  'name': 'protocol_input_set_id'}}})

    protocol_input_id: str = Field(default=..., description="""Internal CDM unique identifier for the value of an input parameter for a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_input_id',
         'domain_of': ['ProtocolInput', 'ProtocolInputSet'],
         'slot_uri': 'CDM:protocol_input_id'} })
    protocol_input_set_id: str = Field(default=..., description="""Internal CDM unique identifier for a set of input parameter values for a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_input_set_id',
         'domain_of': ['ProtocolInputSet', 'ProtocolOutput'],
         'slot_uri': 'CDM:protocol_input_set_id'} })


class ProtocolOutput(Table):
    """
    The output of a protocol.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'protocol_output_id': {'identifier': True,
                                               'name': 'protocol_output_id'}}})

    protocol_output_id: str = Field(default=..., description="""Internal CDM unique identifier for the value of an output of a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_output_id',
         'domain_of': ['ProtocolOutput'],
         'slot_uri': 'CDM:protocol_output_id'} })
    protocol_input_set_id: str = Field(default=..., description="""Internal CDM unique identifier for a set of input parameter values for a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_input_set_id',
         'domain_of': ['ProtocolInputSet', 'ProtocolOutput'],
         'slot_uri': 'CDM:protocol_input_set_id'} })
    value: str = Field(default=..., description="""An output from a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'value',
         'domain_of': ['Statement',
                       'ExperimentCondition',
                       'Measurement',
                       'ProtocolInput',
                       'ProtocolOutput']} })


class ProtocolStep(Table):
    """
    A step in a protocol.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'protocol_step_id': {'identifier': True,
                                             'name': 'protocol_step_id'}}})

    protocol_step_id: str = Field(default=..., description="""Internal CDM unique identifier for a step in a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_step_id',
         'domain_of': ['OrderedProtocolStep', 'ProtocolStep'],
         'slot_uri': 'CDM:protocol_step_id'} })
    step: Optional[str] = Field(default=None, description="""Text description of a step in a protocol.""", json_schema_extra = { "linkml_meta": {'alias': 'step',
         'any_of': [{'range': 'string'}, {'range': 'cdm_protocol_id'}],
         'domain_of': ['ProtocolStep']} })


class ProtocolVariable(LinkerTable):
    """
    A variable that may or may not be set as part of an experiment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol'})

    protocol_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a protocol.
From the Entity table: entity_id where entity_type == 'Protocol'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_id',
         'domain_of': ['Cluster',
                       'Experiment',
                       'OrderedProtocolStep',
                       'Protocol',
                       'ProtocolExecution',
                       'ProtocolVariable',
                       'Feature'],
         'slot_uri': 'CDM:protocol_id'} })
    variable_id: str = Field(default=..., description="""Internal CDM unique identifier for a variable.""", json_schema_extra = { "linkml_meta": {'alias': 'variable_id',
         'domain_of': ['ExperimentCondition',
                       'MeasurementSet',
                       'ProtocolVariable',
                       'Variable',
                       'VariableValue'],
         'slot_uri': 'CDM:variable_id'} })


class Variable(Table):
    """
    A variable (input, output, environmental, etc.) that can be set or measured as part of a protocol.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'variable_id': {'identifier': True, 'name': 'variable_id'}}})

    variable_id: str = Field(default=..., description="""Internal CDM unique identifier for a variable.""", json_schema_extra = { "linkml_meta": {'alias': 'variable_id',
         'domain_of': ['ExperimentCondition',
                       'MeasurementSet',
                       'ProtocolVariable',
                       'Variable',
                       'VariableValue'],
         'slot_uri': 'CDM:variable_id'} })
    name: Optional[str] = Field(default=None, description="""A string used as a name or title.""", json_schema_extra = { "linkml_meta": {'alias': 'name',
         'domain_of': ['Cluster',
                       'Event',
                       'Name',
                       'Contributor',
                       'DataSource',
                       'DataSourceNew',
                       'License',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable'],
         'slot_uri': 'schema:name'} })
    description: Optional[str] = Field(default=None, description="""Brief textual definition or description.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    name_cv_id: Optional[str] = Field(default=None, description="""If the `name` is from a controlled vocabulary (CV), the curie of the controlled vocabulary term.""", json_schema_extra = { "linkml_meta": {'alias': 'name_cv_id', 'domain_of': ['Variable']} })
    unit: Optional[str] = Field(default=None, description="""The units used to measure the value of the variable, if applicable. Units should be expressed using the Unit Ontology or a term from UCUM.""", json_schema_extra = { "linkml_meta": {'alias': 'unit', 'domain_of': ['Variable']} })
    value_type: VariableType = Field(default=..., description="""The type of the value of a variable. Should be a LinkML data type or one of the defined CDM data types.""", json_schema_extra = { "linkml_meta": {'alias': 'value_type', 'domain_of': ['Parameter', 'Variable', 'VariableValue']} })


class VariableValue(Table):
    """
    The possible types for the value of a variable. Should be a LinkML data type or one of the defined CDM data types.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_protocol',
         'slot_usage': {'variable_value_id': {'identifier': True,
                                              'name': 'variable_value_id'}}})

    variable_value_id: str = Field(default=..., description="""Internal CDM unique identifier for a variable value.""", json_schema_extra = { "linkml_meta": {'alias': 'variable_value_id',
         'domain_of': ['VariableValue'],
         'slot_uri': 'CDM:variable_value_id'} })
    variable_id: str = Field(default=..., description="""Internal CDM unique identifier for a variable.""", json_schema_extra = { "linkml_meta": {'alias': 'variable_id',
         'domain_of': ['ExperimentCondition',
                       'MeasurementSet',
                       'ProtocolVariable',
                       'Variable',
                       'VariableValue'],
         'slot_uri': 'CDM:variable_id'} })
    value_type: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'alias': 'value_type', 'domain_of': ['Parameter', 'Variable', 'VariableValue']} })


class Contig(Table):
    """
    A contig (derived from the word \"contiguous\") is a set of DNA segments or sequences that overlap in a way that provides a contiguous representation of a genomic region. A contig should not contain any gaps.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_bioentity',
         'slot_usage': {'contig_id': {'identifier': True, 'name': 'contig_id'}}})

    contig_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig.
From the Entity table: entity_id where entity_type == 'Contig'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_id',
         'domain_of': ['Contig',
                       'Contig_x_ContigCollection',
                       'Contig_x_EncodedFeature',
                       'Contig_x_Feature',
                       'Contig_x_Protein']} })
    hash: Optional[str] = Field(default=None, description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""", json_schema_extra = { "linkml_meta": {'alias': 'hash',
         'domain_of': ['Contig',
                       'ContigCollection',
                       'EncodedFeature',
                       'Feature',
                       'Protein']} })
    gc_content: Optional[float] = Field(default=None, description="""GC content of the contig, expressed as a percentage.""", json_schema_extra = { "linkml_meta": {'alias': 'gc_content', 'domain_of': ['Contig']} })
    length: Optional[int] = Field(default=None, description="""Length of the contig in bp.""", json_schema_extra = { "linkml_meta": {'alias': 'length', 'domain_of': ['Contig', 'Protein', 'Sequence']} })


class ContigCollection(Table):
    """
    A set of individual, overlapping contigs that represent the complete sequenced genome of an organism.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'aliases': ['genome',
                     'biological subject',
                     'assembly',
                     'contig collection',
                     'contig set'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_bioentity',
         'slot_usage': {'contig_collection_id': {'identifier': True,
                                                 'name': 'contig_collection_id'}}})

    contig_collection_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig collection.
From the Entity table: entity_id where entity_type == 'ContigCollection'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_id',
         'domain_of': ['ContigCollection',
                       'Contig_x_ContigCollection',
                       'ContigCollection_x_EncodedFeature',
                       'ContigCollection_x_Feature',
                       'ContigCollection_x_Protein']} })
    hash: Optional[str] = Field(default=None, description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""", json_schema_extra = { "linkml_meta": {'alias': 'hash',
         'domain_of': ['Contig',
                       'ContigCollection',
                       'EncodedFeature',
                       'Feature',
                       'Protein']} })
    asm_score: Optional[float] = Field(default=None, description="""A composite score for comparing contig collection quality.""", json_schema_extra = { "linkml_meta": {'alias': 'asm_score', 'domain_of': ['ContigCollection']} })
    checkm_completeness: Optional[float] = Field(default=None, description="""Estimate of the completeness of a contig collection (MAG or genome), estimated by CheckM tool. Ensure that percentage values are converted to floats.""", json_schema_extra = { "linkml_meta": {'alias': 'checkm_completeness', 'domain_of': ['ContigCollection']} })
    checkm_contamination: Optional[float] = Field(default=None, description="""Estimate of the contamination of a contig collection (MAG or genome), estimated by CheckM tool. Ensure that percentage values are converted to floats.""", json_schema_extra = { "linkml_meta": {'alias': 'checkm_contamination', 'domain_of': ['ContigCollection']} })
    checkm_version: Optional[str] = Field(default=None, description="""Version of the CheckM tool used.""", json_schema_extra = { "linkml_meta": {'alias': 'checkm_version', 'domain_of': ['ContigCollection']} })
    contig_bp: Optional[int] = Field(default=None, description="""Total size in bp of all contigs""", json_schema_extra = { "linkml_meta": {'alias': 'contig_bp',
         'aliases': ['sequence length', 'total sequence length'],
         'domain_of': ['ContigCollection']} })
    contig_collection_type: Optional[ContigCollectionType] = Field(default=None, description="""The type of contig collection.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_type', 'domain_of': ['ContigCollection']} })
    contig_l50: Optional[int] = Field(default=None, description="""Given a set of contigs, the L50 is defined as the sequence length of the shortest contig at 50% of the total contig collection length""", json_schema_extra = { "linkml_meta": {'alias': 'contig_l50',
         'aliases': ['ctg_L50', 'contig_L50'],
         'domain_of': ['ContigCollection']} })
    contig_l90: Optional[int] = Field(default=None, description="""The L90 statistic is less than or equal to the L50 statistic; it is the length for which the collection of all contigs of that length or longer contains at least 90% of the sum of the lengths of all contigs""", json_schema_extra = { "linkml_meta": {'alias': 'contig_l90',
         'aliases': ['ctg_L90', 'contig_L90'],
         'domain_of': ['ContigCollection']} })
    contig_n50: Optional[int] = Field(default=None, description="""Given a set of contigs, each with its own length, the N50 count is defined as the smallest number_of_contigs whose length sum makes up half of contig collection size""", json_schema_extra = { "linkml_meta": {'alias': 'contig_n50',
         'aliases': ['ctg_N50', 'contig_N50'],
         'domain_of': ['ContigCollection']} })
    contig_n90: Optional[int] = Field(default=None, description="""Given a set of contigs, each with its own length, the N90 count is defined as the smallest number of contigs whose length sum makes up 90% of contig collection size""", json_schema_extra = { "linkml_meta": {'alias': 'contig_n90',
         'aliases': ['ctg_N90', 'contig_N90'],
         'domain_of': ['ContigCollection']} })
    contig_logsum: Optional[float] = Field(default=None, description="""The sum of the (length*log(length)) of all contigs, times some constant.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_logsum',
         'aliases': ['ctg_logsum'],
         'domain_of': ['ContigCollection']} })
    contig_max: Optional[int] = Field(default=None, description="""Maximum contig length""", json_schema_extra = { "linkml_meta": {'alias': 'contig_max',
         'aliases': ['ctg_max'],
         'domain_of': ['ContigCollection']} })
    contig_powersum: Optional[float] = Field(default=None, description="""Powersum of all contigs is the same as logsum except that it uses the sum of (length*(length^P)) for some power P (default P=0.25)""", json_schema_extra = { "linkml_meta": {'alias': 'contig_powersum',
         'aliases': ['ctg_powersum', 'ctg_powsum', 'contig_powsum'],
         'domain_of': ['ContigCollection']} })
    gap_percent: Optional[float] = Field(default=None, description="""The gap size percentage of all scaffolds""", json_schema_extra = { "linkml_meta": {'alias': 'gap_percent',
         'aliases': ['gap_pct'],
         'domain_of': ['ContigCollection']} })
    gc_average: Optional[float] = Field(default=None, description="""The average GC content of the contig collection, expressed as a percentage""", json_schema_extra = { "linkml_meta": {'alias': 'gc_average',
         'aliases': ['gc_avg'],
         'domain_of': ['ContigCollection']} })
    gc_std: Optional[float] = Field(default=None, description="""The standard deviation of GC content across the contig collection""", json_schema_extra = { "linkml_meta": {'alias': 'gc_std', 'aliases': ['gc_stdev'], 'domain_of': ['ContigCollection']} })
    gtdb_taxon_id: Optional[str] = Field(default=None, description="""The GTDB taxon ID for this contig collection.""", json_schema_extra = { "linkml_meta": {'alias': 'gtdb_taxon_id', 'domain_of': ['ContigCollection']} })
    n_chromosomes: Optional[int] = Field(default=None, description="""Total number of chromosomes""", json_schema_extra = { "linkml_meta": {'alias': 'n_chromosomes', 'domain_of': ['ContigCollection']} })
    n_contigs: Optional[int] = Field(default=None, description="""Total number of contigs""", json_schema_extra = { "linkml_meta": {'alias': 'n_contigs', 'domain_of': ['ContigCollection']} })
    n_scaffolds: Optional[int] = Field(default=None, description="""Total number of scaffolds""", json_schema_extra = { "linkml_meta": {'alias': 'n_scaffolds', 'domain_of': ['ContigCollection']} })
    ncbi_taxon_id: Optional[str] = Field(default=None, description="""The NCBI taxon ID for this contig collection.""", json_schema_extra = { "linkml_meta": {'alias': 'ncbi_taxon_id', 'domain_of': ['ContigCollection']} })
    scaffold_l50: Optional[int] = Field(default=None, description="""Given a set of scaffolds, the L50 is defined as the sequence length of the shortest scaffold at 50% of the total contig collection length""", json_schema_extra = { "linkml_meta": {'alias': 'scaffold_l50',
         'aliases': ['scaf_L50', 'scaffold_L50'],
         'domain_of': ['ContigCollection']} })
    scaffold_l90: Optional[int] = Field(default=None, description="""The L90 statistic is less than or equal to the L50 statistic; it is the length for which the collection of all scaffolds of that length or longer contains at least 90% of the sum of the lengths of all scaffolds.""", json_schema_extra = { "linkml_meta": {'alias': 'scaffold_l90',
         'aliases': ['scaf_L90', 'scaffold_L90'],
         'domain_of': ['ContigCollection']} })
    scaffold_n50: Optional[int] = Field(default=None, description="""Given a set of scaffolds, each with its own length, the N50 count is defined as the smallest number of scaffolds whose length sum makes up half of contig collection size""", json_schema_extra = { "linkml_meta": {'alias': 'scaffold_n50',
         'aliases': ['scaf_N50', 'scaffold_N50'],
         'domain_of': ['ContigCollection']} })
    scaffold_n90: Optional[int] = Field(default=None, description="""Given a set of scaffolds, each with its own length, the N90 count is defined as the smallest number of scaffolds whose length sum makes up 90% of contig collection size""", json_schema_extra = { "linkml_meta": {'alias': 'scaffold_n90',
         'aliases': ['scaf_N90', 'scaffold_N90'],
         'domain_of': ['ContigCollection']} })
    scaffold_bp: Optional[int] = Field(default=None, description="""Total size in bp of all scaffolds""", json_schema_extra = { "linkml_meta": {'alias': 'scaffold_bp',
         'aliases': ['scaf_bp'],
         'domain_of': ['ContigCollection']} })
    scaffold_logsum: Optional[float] = Field(default=None, description="""The sum of the (length*log(length)) of all scaffolds, times some constant. Increase the contiguity, the score will increase""", json_schema_extra = { "linkml_meta": {'alias': 'scaffold_logsum',
         'aliases': ['scaf_logsum'],
         'domain_of': ['ContigCollection']} })
    scaffold_maximum_length: Optional[int] = Field(default=None, description="""Maximum scaffold length""", json_schema_extra = { "linkml_meta": {'alias': 'scaffold_maximum_length',
         'aliases': ['scaf_max', 'scaffold_max'],
         'domain_of': ['ContigCollection']} })
    scaffold_powersum: Optional[float] = Field(default=None, description="""Powersum of all scaffolds is the same as logsum except that it uses the sum of (length*(length^P)) for some power P (default P=0.25).""", json_schema_extra = { "linkml_meta": {'alias': 'scaffold_powersum',
         'aliases': ['scaf_powsum', 'scaffold_powsum'],
         'domain_of': ['ContigCollection']} })
    scaffolds_n_over_50K: Optional[int] = Field(default=None, description="""The number of scaffolds longer than 50,000 base pairs.""", json_schema_extra = { "linkml_meta": {'alias': 'scaffolds_n_over_50K',
         'aliases': ['scaf_n_gt50K', 'scaffold_n_gt50K'],
         'domain_of': ['ContigCollection']} })
    scaffolds_percent_over_50K: Optional[float] = Field(default=None, description="""The percentage of the total assembly length represented by scaffolds longer than 50,000 base pairs""", json_schema_extra = { "linkml_meta": {'alias': 'scaffolds_percent_over_50K',
         'aliases': ['scaf_pct_gt50K', 'scaffold_pct_gt50K'],
         'domain_of': ['ContigCollection']} })
    scaffolds_total_length_over_50k: Optional[int] = Field(default=None, description="""The total length of scaffolds longer than 50,000 base pairs""", json_schema_extra = { "linkml_meta": {'alias': 'scaffolds_total_length_over_50k',
         'aliases': ['scaf_l_gt50k', 'scaffold_l_gt50k'],
         'domain_of': ['ContigCollection']} })


class EncodedFeature(Table):
    """
    An entity generated from a feature, such as a transcript.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_bioentity',
         'slot_usage': {'encoded_feature_id': {'identifier': True,
                                               'name': 'encoded_feature_id'}}})

    encoded_feature_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an encoded feature.
From the Entity table: entity_id where entity_type == 'EncodedFeature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'encoded_feature_id',
         'domain_of': ['EncodedFeature',
                       'Contig_x_EncodedFeature',
                       'ContigCollection_x_EncodedFeature',
                       'EncodedFeature_x_Feature',
                       'EncodedFeature_x_Protein']} })
    hash: Optional[str] = Field(default=None, description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""", json_schema_extra = { "linkml_meta": {'alias': 'hash',
         'domain_of': ['Contig',
                       'ContigCollection',
                       'EncodedFeature',
                       'Feature',
                       'Protein']} })
    has_stop_codon: Optional[bool] = Field(default=None, description="""Captures whether or not the sequence includes stop coordinates.""", json_schema_extra = { "linkml_meta": {'alias': 'has_stop_codon', 'domain_of': ['EncodedFeature']} })
    type: Optional[str] = Field(default=None, description="""The type of the entity. Should be a term from the sequence ontology.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence']} })

    @field_validator('type')
    def pattern_type(cls, v):
        pattern=re.compile(r"^SO:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid type format: {v}"
            raise ValueError(err_msg)
        return v


class Feature(Table):
    """
    A feature localized to an interval along a contig.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'comments': ['corresponds to an entry in GFF3'],
         'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_bioentity',
         'see_also': ['https://github.com/The-Sequence-Ontology/Specifications/blob/master/gff3.md'],
         'slot_usage': {'feature_id': {'identifier': True, 'name': 'feature_id'}}})

    feature_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a feature.
From the Entity table: entity_id where entity_type == 'Feature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'feature_id',
         'domain_of': ['Feature',
                       'Contig_x_Feature',
                       'ContigCollection_x_Feature',
                       'EncodedFeature_x_Feature',
                       'Feature_x_Protein']} })
    hash: Optional[str] = Field(default=None, description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""", json_schema_extra = { "linkml_meta": {'alias': 'hash',
         'domain_of': ['Contig',
                       'ContigCollection',
                       'EncodedFeature',
                       'Feature',
                       'Protein']} })
    cds_phase: Optional[CdsPhaseType] = Field(default=None, description="""For features of type CDS, the phase indicates where the next codon begins relative to the 5' end (where the 5' end of the CDS is relative to the strand of the CDS feature) of the current CDS feature. cds_phase is required if the feature type is CDS.""", json_schema_extra = { "linkml_meta": {'alias': 'cds_phase', 'domain_of': ['Feature']} })
    e_value: Optional[float] = Field(default=None, description="""The 'score' of the feature. The semantics of this field are ill-defined. E-values should be used for sequence similarity features.""", json_schema_extra = { "linkml_meta": {'alias': 'e_value', 'domain_of': ['Feature']} })
    end: Optional[int] = Field(default=None, description="""The start and end coordinates of the feature are given in positive 1-based int coordinates, relative to the landmark given in column one. Start is always less than or equal to end. For features that cross the origin of a circular feature (e.g. most bacterial genomes, plasmids, and some viral genomes), the requirement for start to be less than or equal to end is satisfied by making end = the position of the end + the length of the landmark feature. For zero-length features, such as insertion sites, start equals end and the implied site is to the right of the indicated base in the direction of the landmark.""", json_schema_extra = { "linkml_meta": {'alias': 'end', 'domain_of': ['Feature']} })
    p_value: Optional[float] = Field(default=None, description="""The 'score' of the feature. The semantics of this field are ill-defined. P-values should be used for ab initio gene prediction features.""", json_schema_extra = { "linkml_meta": {'alias': 'p_value', 'domain_of': ['Feature']} })
    start: Optional[int] = Field(default=None, description="""The start and end coordinates of the feature are given in positive 1-based int coordinates, relative to the landmark given in column one. Start is always less than or equal to end. For features that cross the origin of a circular feature (e.g. most bacterial genomes, plasmids, and some viral genomes), the requirement for start to be less than or equal to end is satisfied by making end = the position of the end + the length of the landmark feature. For zero-length features, such as insertion sites, start equals end and the implied site is to the right of the indicated base in the direction of the landmark.""", json_schema_extra = { "linkml_meta": {'alias': 'start', 'domain_of': ['Feature']} })
    strand: Optional[StrandType] = Field(default=None, description="""The strand of the feature.""", json_schema_extra = { "linkml_meta": {'alias': 'strand', 'domain_of': ['Feature']} })
    source_database: Optional[str] = Field(default=None, description="""ID of the data source from which this entity came.""", json_schema_extra = { "linkml_meta": {'alias': 'source_database', 'domain_of': ['Feature']} })
    protocol_id: Optional[str] = Field(default=None, description="""ID of the protocol used to generate the feature.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_id',
         'aliases': ['generated by'],
         'domain_of': ['Cluster',
                       'Experiment',
                       'OrderedProtocolStep',
                       'Protocol',
                       'ProtocolExecution',
                       'ProtocolVariable',
                       'Feature']} })
    type: Optional[str] = Field(default=None, description="""The type of the feature; constrained to be a Sequence Ontology accession (i.e. SO:000nnnn). Must be sequence_feature (SO:0000110) or an is_a child of it.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'aliases': ['feature type'],
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence']} })

    @field_validator('type')
    def pattern_type(cls, v):
        pattern=re.compile(r"^SO:\d+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid type format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid type format: {v}"
            raise ValueError(err_msg)
        return v


class Protein(Table):
    """
    Proteins are large, complex molecules made up of one or more long, folded chains of amino acids, whose sequences are determined by the DNA sequence of the protein-encoding gene.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_bioentity',
         'slot_usage': {'protein_id': {'identifier': True, 'name': 'protein_id'}}})

    protein_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a protein.
From the Entity table: entity_id where entity_type == 'Protein'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protein_id',
         'domain_of': ['Protein',
                       'Contig_x_Protein',
                       'ContigCollection_x_Protein',
                       'EncodedFeature_x_Protein',
                       'Feature_x_Protein']} })
    hash: Optional[str] = Field(default=None, description="""A hash value generated from one or more object attributes that serves to ensure the entity is unique.""", json_schema_extra = { "linkml_meta": {'alias': 'hash',
         'domain_of': ['Contig',
                       'ContigCollection',
                       'EncodedFeature',
                       'Feature',
                       'Protein']} })
    description: Optional[str] = Field(default=None, description="""Brief text description of the entity.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    evidence_for_existence: Optional[ProteinEvidenceForExistence] = Field(default=None, description="""The evidence that this protein exists. For example, the protein may have been isolated from a cell, or it may be predicted based on sequence features.""", json_schema_extra = { "linkml_meta": {'alias': 'evidence_for_existence', 'domain_of': ['Protein']} })
    length: Optional[int] = Field(default=None, description="""The length of the protein.""", json_schema_extra = { "linkml_meta": {'alias': 'length', 'domain_of': ['Contig', 'Protein', 'Sequence']} })
    sequence: Optional[str] = Field(default=None, description="""The protein amino acid sequence.""", json_schema_extra = { "linkml_meta": {'alias': 'sequence', 'domain_of': ['Protein']} })


class Sample(Table):
    """
    A material entity that can be characterised by an experiment.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_bioentity',
         'slot_usage': {'sample_id': {'identifier': True, 'name': 'sample_id'}}})

    sample_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a sample.
From the Entity table: entity_id where entity_type == 'Sample'.
""", json_schema_extra = { "linkml_meta": {'alias': 'sample_id', 'domain_of': ['Sample']} })
    description: Optional[str] = Field(default=None, description="""Brief textual description of the sample.""", json_schema_extra = { "linkml_meta": {'alias': 'description',
         'domain_of': ['Cluster',
                       'Event',
                       'Identifier',
                       'Name',
                       'Project',
                       'Experiment',
                       'Parameter',
                       'Protocol',
                       'ProtocolExecution',
                       'Variable',
                       'Protein',
                       'Sample']} })
    type: Optional[str] = Field(default=None, description="""The type of entity that the sample is. Vocab TBD.""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence']} })


class Sequence(Table):
    """
    A sequence of nucleotides or amino acids.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_bioentity',
         'slot_usage': {'entity_id': {'description': 'The entity to which this '
                                                     'sequence belongs.',
                                      'name': 'entity_id'}}})

    sequence_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a sequence.
From the Entity table: entity_id where entity_type == 'Sequence'.
""", json_schema_extra = { "linkml_meta": {'alias': 'sequence_id', 'domain_of': ['Sequence']} })
    entity_id: str = Field(default=..., description="""The entity to which this sequence belongs.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })
    type: Optional[SequenceType] = Field(default=None, description="""The type of the sequence, either \"Nucleotide\" or \"Amino Acid\".""", json_schema_extra = { "linkml_meta": {'alias': 'type',
         'domain_of': ['AttributeValue',
                       'EncodedFeature',
                       'Feature',
                       'Sample',
                       'Sequence']} })
    length: Optional[int] = Field(default=None, description="""The length of the sequence in base pairs (for nucleotide sequences) or amino acids (for amino acid sequences).""", json_schema_extra = { "linkml_meta": {'alias': 'length', 'domain_of': ['Contig', 'Protein', 'Sequence']} })
    checksum: Optional[str] = Field(default=None, description="""The checksum of the sequence, used to verify its integrity.""", json_schema_extra = { "linkml_meta": {'alias': 'checksum', 'domain_of': ['Sequence']} })


class AssociationXSupportingObject(LinkerTable):
    """
    Links associations to entities to capture supporting objects in an association. May be a biological entity, such as a protein or feature, or a URL to a resource (e.g. a publication) that supports the association. Where possible, CDM identifiers should be used.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'association_id': {'multivalued': True,
                                           'name': 'association_id'},
                        'entity_id': {'multivalued': True, 'name': 'entity_id'}}})

    association_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for an association.""", json_schema_extra = { "linkml_meta": {'alias': 'association_id',
         'domain_of': ['Association', 'Association_x_SupportingObject']} })
    entity_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for an entity.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_id',
         'domain_of': ['ClusterMember',
                       'Entity',
                       'Identifier',
                       'Name',
                       'EntityMixin',
                       'Sequence',
                       'Association_x_SupportingObject']} })


class ContigXContigCollection(LinkerTable):
    """
    Captures the relationship between a contig and a contig collection; equivalent to contig part-of contig collection.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'contig_id': {'multivalued': True, 'name': 'contig_id'}}})

    contig_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for a contig.
From the Entity table: entity_id where entity_type == 'Contig'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_id',
         'domain_of': ['Contig',
                       'Contig_x_ContigCollection',
                       'Contig_x_EncodedFeature',
                       'Contig_x_Feature',
                       'Contig_x_Protein']} })
    contig_collection_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig collection.
From the Entity table: entity_id where entity_type == 'ContigCollection'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_id',
         'domain_of': ['ContigCollection',
                       'Contig_x_ContigCollection',
                       'ContigCollection_x_EncodedFeature',
                       'ContigCollection_x_Feature',
                       'ContigCollection_x_Protein']} })


class ContigXEncodedFeature(LinkerTable):
    """
    Captures the relationship between a contig and an encoded feature.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'encoded_feature_id': {'multivalued': True,
                                               'name': 'encoded_feature_id'}}})

    contig_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig.
From the Entity table: entity_id where entity_type == 'Contig'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_id',
         'domain_of': ['Contig',
                       'Contig_x_ContigCollection',
                       'Contig_x_EncodedFeature',
                       'Contig_x_Feature',
                       'Contig_x_Protein']} })
    encoded_feature_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for an encoded feature.
From the Entity table: entity_id where entity_type == 'EncodedFeature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'encoded_feature_id',
         'domain_of': ['EncodedFeature',
                       'Contig_x_EncodedFeature',
                       'ContigCollection_x_EncodedFeature',
                       'EncodedFeature_x_Feature',
                       'EncodedFeature_x_Protein']} })


class ContigXFeature(LinkerTable):
    """
    Captures the relationship between a contig and a feature; equivalent to feature part-of contig.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'feature_id': {'multivalued': True, 'name': 'feature_id'}}})

    contig_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig.
From the Entity table: entity_id where entity_type == 'Contig'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_id',
         'domain_of': ['Contig',
                       'Contig_x_ContigCollection',
                       'Contig_x_EncodedFeature',
                       'Contig_x_Feature',
                       'Contig_x_Protein']} })
    feature_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for a feature.
From the Entity table: entity_id where entity_type == 'Feature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'feature_id',
         'domain_of': ['Feature',
                       'Contig_x_Feature',
                       'ContigCollection_x_Feature',
                       'EncodedFeature_x_Feature',
                       'Feature_x_Protein']} })


class ContigXProtein(LinkerTable):
    """
    Captures the relationship between a contig and a protein; equivalent to protein is ribosomal translation of (http://purl.obolibrary.org/obo/RO_0002512) contig.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'protein_id': {'multivalued': True, 'name': 'protein_id'}}})

    contig_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig.
From the Entity table: entity_id where entity_type == 'Contig'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_id',
         'domain_of': ['Contig',
                       'Contig_x_ContigCollection',
                       'Contig_x_EncodedFeature',
                       'Contig_x_Feature',
                       'Contig_x_Protein']} })
    protein_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for a protein.
From the Entity table: entity_id where entity_type == 'Protein'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protein_id',
         'domain_of': ['Protein',
                       'Contig_x_Protein',
                       'ContigCollection_x_Protein',
                       'EncodedFeature_x_Protein',
                       'Feature_x_Protein']} })


class ContigCollectionXEncodedFeature(LinkerTable):
    """
    Captures the relationship between a contig collection and an encoded feature.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'encoded_feature_id': {'multivalued': True,
                                               'name': 'encoded_feature_id'}}})

    contig_collection_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig collection.
From the Entity table: entity_id where entity_type == 'ContigCollection'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_id',
         'domain_of': ['ContigCollection',
                       'Contig_x_ContigCollection',
                       'ContigCollection_x_EncodedFeature',
                       'ContigCollection_x_Feature',
                       'ContigCollection_x_Protein']} })
    encoded_feature_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for an encoded feature.
From the Entity table: entity_id where entity_type == 'EncodedFeature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'encoded_feature_id',
         'domain_of': ['EncodedFeature',
                       'Contig_x_EncodedFeature',
                       'ContigCollection_x_EncodedFeature',
                       'EncodedFeature_x_Feature',
                       'EncodedFeature_x_Protein']} })


class ContigCollectionXFeature(LinkerTable):
    """
    Captures the relationship between a contig collection and a feature; equivalent to feature part-of contig collection.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'feature_id': {'multivalued': True, 'name': 'feature_id'}}})

    contig_collection_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig collection.
From the Entity table: entity_id where entity_type == 'ContigCollection'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_id',
         'domain_of': ['ContigCollection',
                       'Contig_x_ContigCollection',
                       'ContigCollection_x_EncodedFeature',
                       'ContigCollection_x_Feature',
                       'ContigCollection_x_Protein']} })
    feature_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for a feature.
From the Entity table: entity_id where entity_type == 'Feature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'feature_id',
         'domain_of': ['Feature',
                       'Contig_x_Feature',
                       'ContigCollection_x_Feature',
                       'EncodedFeature_x_Feature',
                       'Feature_x_Protein']} })


class ContigCollectionXProtein(LinkerTable):
    """
    Captures the relationship between a contig collection and a protein; equivalent to protein is ribosomal translation of (http://purl.obolibrary.org/obo/RO_0002512) contig collection.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'protein_id': {'multivalued': True, 'name': 'protein_id'}}})

    contig_collection_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a contig collection.
From the Entity table: entity_id where entity_type == 'ContigCollection'.
""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_id',
         'domain_of': ['ContigCollection',
                       'Contig_x_ContigCollection',
                       'ContigCollection_x_EncodedFeature',
                       'ContigCollection_x_Feature',
                       'ContigCollection_x_Protein']} })
    protein_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for a protein.
From the Entity table: entity_id where entity_type == 'Protein'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protein_id',
         'domain_of': ['Protein',
                       'Contig_x_Protein',
                       'ContigCollection_x_Protein',
                       'EncodedFeature_x_Protein',
                       'Feature_x_Protein']} })


class EncodedFeatureXFeature(LinkerTable):
    """
    Captures the relationship between a feature and its transcription product.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True})

    encoded_feature_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an encoded feature.
From the Entity table: entity_id where entity_type == 'EncodedFeature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'encoded_feature_id',
         'domain_of': ['EncodedFeature',
                       'Contig_x_EncodedFeature',
                       'ContigCollection_x_EncodedFeature',
                       'EncodedFeature_x_Feature',
                       'EncodedFeature_x_Protein']} })
    feature_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a feature.
From the Entity table: entity_id where entity_type == 'Feature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'feature_id',
         'domain_of': ['Feature',
                       'Contig_x_Feature',
                       'ContigCollection_x_Feature',
                       'EncodedFeature_x_Feature',
                       'Feature_x_Protein']} })


class EncodedFeatureXProtein(LinkerTable):
    """
    Captures the relationship between an encoded feature (RNA of some sort) and a protein.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True})

    encoded_feature_id: str = Field(default=..., description="""Internal (CDM) unique identifier for an encoded feature.
From the Entity table: entity_id where entity_type == 'EncodedFeature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'encoded_feature_id',
         'domain_of': ['EncodedFeature',
                       'Contig_x_EncodedFeature',
                       'ContigCollection_x_EncodedFeature',
                       'EncodedFeature_x_Feature',
                       'EncodedFeature_x_Protein']} })
    protein_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a protein.
From the Entity table: entity_id where entity_type == 'Protein'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protein_id',
         'domain_of': ['Protein',
                       'Contig_x_Protein',
                       'ContigCollection_x_Protein',
                       'EncodedFeature_x_Protein',
                       'Feature_x_Protein']} })


class FeatureXProtein(LinkerTable):
    """
    Captures the relationship between a feature and a protein; equivalent to feature encodes protein.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'represents_relationship': True,
         'slot_usage': {'protein_id': {'multivalued': True, 'name': 'protein_id'}}})

    feature_id: str = Field(default=..., description="""Internal (CDM) unique identifier for a feature.
From the Entity table: entity_id where entity_type == 'Feature'.
""", json_schema_extra = { "linkml_meta": {'alias': 'feature_id',
         'domain_of': ['Feature',
                       'Contig_x_Feature',
                       'ContigCollection_x_Feature',
                       'EncodedFeature_x_Feature',
                       'Feature_x_Protein']} })
    protein_id: list[str] = Field(default=..., description="""Internal (CDM) unique identifier for a protein.
From the Entity table: entity_id where entity_type == 'Protein'.
""", json_schema_extra = { "linkml_meta": {'alias': 'protein_id',
         'domain_of': ['Protein',
                       'Contig_x_Protein',
                       'ContigCollection_x_Protein',
                       'EncodedFeature_x_Protein',
                       'Feature_x_Protein']} })


class Schema(ConfiguredBaseModel):
    """
    The root class for the CDM schema.
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'http://kbase.github.io/cdm-schema/linkml/cdm_schema',
         'tree_root': True})

    entities: Optional[list[str]] = Field(default=None, description="""All entities in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'entities', 'domain_of': ['Schema']} })
    names: Optional[list[Name]] = Field(default=None, description="""All names in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'names', 'domain_of': ['Schema']} })
    identifiers: Optional[list[Identifier]] = Field(default=None, description="""All identifiers in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'identifiers', 'domain_of': ['Schema']} })
    entity_names: Optional[list[EntityNames]] = Field(default=None, description="""All name x entity records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_names', 'domain_of': ['Schema']} })
    entity_identifiers: Optional[list[EntityIdentifiers]] = Field(default=None, description="""All identifier x entity records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_identifiers', 'domain_of': ['Schema']} })
    entity_attribute_values: Optional[list[EntityAttributeValue]] = Field(default=None, description="""All entity attribute values in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'entity_attribute_values', 'domain_of': ['Schema']} })
    associations: Optional[list[str]] = Field(default=None, description="""All associations in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'associations', 'domain_of': ['Schema']} })
    clusters: Optional[list[str]] = Field(default=None, description="""All clusters in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'clusters', 'domain_of': ['Schema']} })
    cluster_members: Optional[list[ClusterMember]] = Field(default=None, description="""All cluster members in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'cluster_members', 'domain_of': ['Schema']} })
    events: Optional[list[str]] = Field(default=None, description="""All events in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'events', 'domain_of': ['Schema']} })
    gold_environmental_contexts: Optional[list[str]] = Field(default=None, description="""All GOLD environmental contexts in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'gold_environmental_contexts', 'domain_of': ['Schema']} })
    mixs_environmental_contexts: Optional[list[str]] = Field(default=None, description="""All MIxS environmental contexts in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'mixs_environmental_contexts', 'domain_of': ['Schema']} })
    contributors: Optional[list[str]] = Field(default=None, description="""All contributors in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contributors', 'domain_of': ['Schema']} })
    contributor_affiliations: Optional[list[ContributorAffiliation]] = Field(default=None, description="""All contributor affiliations in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_affiliations', 'domain_of': ['Schema']} })
    contributor_x_role_x_project: Optional[list[ContributorXRoleXProject]] = Field(default=None, description="""All contributor x role x project records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contributor_x_role_x_project', 'domain_of': ['Schema']} })
    data_sources: Optional[list[str]] = Field(default=None, description="""All data sources in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'data_sources', 'domain_of': ['Schema']} })
    data_source_x_descriptions: Optional[list[DataSourceXDescription]] = Field(default=None, description="""All data source descriptions in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_x_descriptions', 'domain_of': ['Schema']} })
    data_source_x_funding_references: Optional[list[DataSourceXFundingReference]] = Field(default=None, description="""All data source x funding reference records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_x_funding_references', 'domain_of': ['Schema']} })
    data_source_x_licenses: Optional[list[DataSourceXLicense]] = Field(default=None, description="""All data source x license records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_x_licenses', 'domain_of': ['Schema']} })
    data_source_x_titles: Optional[list[DataSourceXTitle]] = Field(default=None, description="""All data source x title records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'data_source_x_titles', 'domain_of': ['Schema']} })
    funding_references: Optional[list[str]] = Field(default=None, description="""All funding references in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'funding_references', 'domain_of': ['Schema']} })
    licenses: Optional[list[str]] = Field(default=None, description="""All licenses in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'licenses', 'domain_of': ['Schema']} })
    projects: Optional[list[str]] = Field(default=None, description="""All projects in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'projects', 'domain_of': ['Schema']} })
    publications: Optional[list[str]] = Field(default=None, description="""All publications in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'publications', 'domain_of': ['Schema']} })
    resource_descriptions: Optional[list[ResourceDescription]] = Field(default=None, description="""All resource descriptions in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'resource_descriptions', 'domain_of': ['Schema']} })
    resource_titles: Optional[list[ResourceTitle]] = Field(default=None, description="""All resource titles in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'resource_titles', 'domain_of': ['Schema']} })
    prefixes: Optional[list[Prefix]] = Field(default=None, description="""The prefix mappings for the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'prefixes', 'domain_of': ['Schema']} })
    statements: Optional[list[Statement]] = Field(default=None, description="""All statements in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'statements', 'domain_of': ['Schema']} })
    entailed_edges: Optional[list[EntailedEdge]] = Field(default=None, description="""All entailed edges in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'entailed_edges', 'domain_of': ['Schema']} })
    contigs: Optional[list[str]] = Field(default=None, description="""All contigs in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contigs', 'domain_of': ['Schema']} })
    contig_collections: Optional[list[str]] = Field(default=None, description="""All contig collections in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collections', 'domain_of': ['Schema']} })
    encoded_features: Optional[list[str]] = Field(default=None, description="""All encoded features in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'encoded_features', 'domain_of': ['Schema']} })
    features: Optional[list[str]] = Field(default=None, description="""All features in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'features', 'domain_of': ['Schema']} })
    proteins: Optional[list[str]] = Field(default=None, description="""All proteins in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'proteins', 'domain_of': ['Schema']} })
    samples: Optional[list[str]] = Field(default=None, description="""All samples in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'samples', 'domain_of': ['Schema']} })
    sequences: Optional[list[Sequence]] = Field(default=None, description="""All sequences in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'sequences', 'domain_of': ['Schema']} })
    experiments: Optional[list[str]] = Field(default=None, description="""All experiments in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'experiments', 'domain_of': ['Schema']} })
    experiment_conditions: Optional[list[str]] = Field(default=None, description="""All experiment conditions in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'experiment_conditions', 'domain_of': ['Schema']} })
    experiment_condition_sets: Optional[list[ExperimentConditionSet]] = Field(default=None, description="""All experiment condition sets in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'experiment_condition_sets', 'domain_of': ['Schema']} })
    measurements: Optional[list[str]] = Field(default=None, description="""All measurements in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'measurements', 'domain_of': ['Schema']} })
    measurement_sets: Optional[list[str]] = Field(default=None, description="""All measurement sets in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'measurement_sets', 'domain_of': ['Schema']} })
    ordered_protocol_steps: Optional[list[OrderedProtocolStep]] = Field(default=None, description="""All ordered protocol steps in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'ordered_protocol_steps', 'domain_of': ['Schema']} })
    parameters: Optional[list[str]] = Field(default=None, description="""All parameters in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'parameters', 'domain_of': ['Schema']} })
    protocols: Optional[list[str]] = Field(default=None, description="""All protocols in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'protocols', 'domain_of': ['Schema']} })
    protocol_executions: Optional[list[str]] = Field(default=None, description="""All protocol executions in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_executions', 'domain_of': ['Schema']} })
    protocol_inputs: Optional[list[str]] = Field(default=None, description="""All protocol inputs in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_inputs', 'domain_of': ['Schema']} })
    protocol_input_sets: Optional[list[str]] = Field(default=None, description="""All protocol input sets in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_input_sets', 'domain_of': ['Schema']} })
    protocol_outputs: Optional[list[str]] = Field(default=None, description="""All protocol outputs in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_outputs', 'domain_of': ['Schema']} })
    protocol_steps: Optional[list[str]] = Field(default=None, description="""All protocol steps in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_steps', 'domain_of': ['Schema']} })
    protocol_variables: Optional[list[ProtocolVariable]] = Field(default=None, description="""All protocol variables in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'protocol_variables', 'domain_of': ['Schema']} })
    variables: Optional[list[str]] = Field(default=None, description="""All variables in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'variables', 'domain_of': ['Schema']} })
    variable_values: Optional[list[str]] = Field(default=None, description="""All variable values in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'variable_values', 'domain_of': ['Schema']} })
    association_x_supporting_objects: Optional[list[AssociationXSupportingObject]] = Field(default=None, description="""All association x supporting object records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'association_x_supporting_objects', 'domain_of': ['Schema']} })
    contig_x_contig_collections: Optional[list[ContigXContigCollection]] = Field(default=None, description="""All contig x contig collection records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_x_contig_collections', 'domain_of': ['Schema']} })
    contig_x_encoded_features: Optional[list[ContigXEncodedFeature]] = Field(default=None, description="""All contig x encoded feature records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_x_encoded_features', 'domain_of': ['Schema']} })
    contig_x_features: Optional[list[ContigXFeature]] = Field(default=None, description="""All contig x feature records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_x_features', 'domain_of': ['Schema']} })
    contig_x_proteins: Optional[list[ContigXProtein]] = Field(default=None, description="""All contig x protein records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_x_proteins', 'domain_of': ['Schema']} })
    contig_collection_x_encoded_features: Optional[list[ContigCollectionXEncodedFeature]] = Field(default=None, description="""All contig collection x encoded feature records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_x_encoded_features', 'domain_of': ['Schema']} })
    contig_collection_x_features: Optional[list[ContigCollectionXFeature]] = Field(default=None, description="""All contig collection x feature records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_x_features', 'domain_of': ['Schema']} })
    contig_collection_x_proteins: Optional[list[ContigCollectionXProtein]] = Field(default=None, description="""All contig collection x protein records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'contig_collection_x_proteins', 'domain_of': ['Schema']} })
    encoded_feature_x_features: Optional[list[EncodedFeatureXFeature]] = Field(default=None, description="""All encoded feature x feature records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'encoded_feature_x_features', 'domain_of': ['Schema']} })
    encoded_feature_x_proteins: Optional[list[EncodedFeatureXProtein]] = Field(default=None, description="""All encoded feature x protein records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'encoded_feature_x_proteins', 'domain_of': ['Schema']} })
    feature_x_proteins: Optional[list[FeatureXProtein]] = Field(default=None, description="""All feature x protein records in the schema.""", json_schema_extra = { "linkml_meta": {'alias': 'feature_x_proteins', 'domain_of': ['Schema']} })


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Table.model_rebuild()
Association.model_rebuild()
Cluster.model_rebuild()
ClusterMember.model_rebuild()
Event.model_rebuild()
GoldEnvironmentalContext.model_rebuild()
MixsEnvironmentalContext.model_rebuild()
LinkerTable.model_rebuild()
Entity.model_rebuild()
Identifier.model_rebuild()
Name.model_rebuild()
EntityNames.model_rebuild()
EntityIdentifiers.model_rebuild()
AttributeMixin.model_rebuild()
EntityMixin.model_rebuild()
UnitMixin.model_rebuild()
AttributeValue.model_rebuild()
EntityAttributeValue.model_rebuild()
QuantityValue.model_rebuild()
QuantityRangeValue.model_rebuild()
DateTimeValue.model_rebuild()
Geolocation.model_rebuild()
ControlledTermValue.model_rebuild()
ControlledVocabularyTermValue.model_rebuild()
TextValue.model_rebuild()
Contributor.model_rebuild()
ContributorAffiliation.model_rebuild()
ContributorXDataSource.model_rebuild()
ContributorXRoleXProject.model_rebuild()
DataSource.model_rebuild()
DataSourceNew.model_rebuild()
DataSourceXDescription.model_rebuild()
DataSourceXFundingReference.model_rebuild()
DataSourceXLicense.model_rebuild()
DataSourceXTitle.model_rebuild()
FundingReference.model_rebuild()
License.model_rebuild()
Project.model_rebuild()
Publication.model_rebuild()
ResourceDescription.model_rebuild()
ResourceTitle.model_rebuild()
Prefix.model_rebuild()
Statement.model_rebuild()
EntailedEdge.model_rebuild()
Experiment.model_rebuild()
ExperimentCondition.model_rebuild()
ExperimentConditionSet.model_rebuild()
Measurement.model_rebuild()
MeasurementSet.model_rebuild()
OrderedProtocolStep.model_rebuild()
Parameter.model_rebuild()
Protocol.model_rebuild()
ProtocolExecution.model_rebuild()
ProtocolInput.model_rebuild()
ProtocolInputSet.model_rebuild()
ProtocolOutput.model_rebuild()
ProtocolStep.model_rebuild()
ProtocolVariable.model_rebuild()
Variable.model_rebuild()
VariableValue.model_rebuild()
Contig.model_rebuild()
ContigCollection.model_rebuild()
EncodedFeature.model_rebuild()
Feature.model_rebuild()
Protein.model_rebuild()
Sample.model_rebuild()
Sequence.model_rebuild()
AssociationXSupportingObject.model_rebuild()
ContigXContigCollection.model_rebuild()
ContigXEncodedFeature.model_rebuild()
ContigXFeature.model_rebuild()
ContigXProtein.model_rebuild()
ContigCollectionXEncodedFeature.model_rebuild()
ContigCollectionXFeature.model_rebuild()
ContigCollectionXProtein.model_rebuild()
EncodedFeatureXFeature.model_rebuild()
EncodedFeatureXProtein.model_rebuild()
FeatureXProtein.model_rebuild()
Schema.model_rebuild()

