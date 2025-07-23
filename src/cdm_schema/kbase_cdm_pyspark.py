"""Automated conversion of cdm_schema to PySpark."""

from pyspark.sql.types import BooleanType, DateType, FloatType, IntegerType, StringType, StructField, StructType

schema = {
    "Association": StructType(
        [
            StructField("association_id", StringType(), nullable=False),
            StructField("subject", StringType(), nullable=False),
            StructField("object", StringType(), nullable=False),
            StructField("predicate", StringType(), nullable=True),
            StructField("negated", BooleanType(), nullable=True),
            StructField("evidence_type", StringType(), nullable=True),
            StructField("primary_knowledge_source", StringType(), nullable=True),
            StructField("aggregator_knowledge_source", StringType(), nullable=True),
            StructField("annotation_date", DateType(), nullable=True),
            StructField("comments", StringType(), nullable=True),
        ]
    ),
    "Cluster": StructType(
        [
            StructField("cluster_id", StringType(), nullable=False),
            StructField("description", StringType(), nullable=True),
            StructField("name", StringType(), nullable=True),
            StructField("entity_type", StringType(), nullable=False),
            StructField("protocol_id", StringType(), nullable=True),
        ]
    ),
    "ClusterMember": StructType(
        [
            StructField("cluster_id", StringType(), nullable=False),
            StructField("entity_id", StringType(), nullable=False),
            StructField("is_representative", BooleanType(), nullable=True),
            StructField("is_seed", BooleanType(), nullable=True),
            StructField("score", FloatType(), nullable=True),
        ]
    ),
    "Contig": StructType(
        [
            StructField("contig_id", StringType(), nullable=False),
            StructField("hash", StringType(), nullable=True),
            StructField("gc_content", FloatType(), nullable=True),
            StructField("length", IntegerType(), nullable=True),
        ]
    ),
    "ContigCollection": StructType(
        [
            StructField("contig_collection_id", StringType(), nullable=False),
            StructField("hash", StringType(), nullable=True),
            StructField("asm_score", FloatType(), nullable=True),
            StructField("checkm2_completeness", FloatType(), nullable=True),
            StructField("checkm2_contamination", FloatType(), nullable=True),
            StructField("contig_bp", IntegerType(), nullable=True),
            StructField("contig_collection_type", StringType(), nullable=True),
            StructField("ctg_L50", IntegerType(), nullable=True),
            StructField("ctg_L90", IntegerType(), nullable=True),
            StructField("ctg_N50", IntegerType(), nullable=True),
            StructField("ctg_N90", IntegerType(), nullable=True),
            StructField("ctg_logsum", FloatType(), nullable=True),
            StructField("ctg_max", IntegerType(), nullable=True),
            StructField("ctg_powsum", FloatType(), nullable=True),
            StructField("gap_pct", FloatType(), nullable=True),
            StructField("gc_avg", FloatType(), nullable=True),
            StructField("gc_std", FloatType(), nullable=True),
            StructField("n_contigs", IntegerType(), nullable=True),
            StructField("n_scaffolds", IntegerType(), nullable=True),
            StructField("scaf_L50", IntegerType(), nullable=True),
            StructField("scaf_L90", IntegerType(), nullable=True),
            StructField("scaf_N50", IntegerType(), nullable=True),
            StructField("scaf_N90", IntegerType(), nullable=True),
            StructField("scaf_bp", IntegerType(), nullable=True),
            StructField("scaf_l_gt50k", IntegerType(), nullable=True),
            StructField("scaf_logsum", FloatType(), nullable=True),
            StructField("scaf_max", IntegerType(), nullable=True),
            StructField("scaf_n_gt50K", IntegerType(), nullable=True),
            StructField("scaf_pct_gt50K", FloatType(), nullable=True),
            StructField("scaf_powsum", FloatType(), nullable=True),
        ]
    ),
    "Contributor": StructType(
        [
            StructField("contributor_id", StringType(), nullable=False),
            StructField("contributor_type", StringType(), nullable=True),
            StructField("name", StringType(), nullable=True),
            StructField("given_name", StringType(), nullable=True),
            StructField("family_name", StringType(), nullable=True),
        ]
    ),
    "DataSource": StructType(
        [
            StructField("data_source_id", StringType(), nullable=False),
            StructField("name", StringType(), nullable=True),
            StructField("comments", StringType(), nullable=True),
            StructField("date_accessed", DateType(), nullable=True),
            StructField("url", StringType(), nullable=True),
            StructField("version", StringType(), nullable=True),
        ]
    ),
    "EncodedFeature": StructType(
        [
            StructField("encoded_feature_id", StringType(), nullable=False),
            StructField("hash", StringType(), nullable=True),
            StructField("has_stop_codon", BooleanType(), nullable=True),
            StructField("type", StringType(), nullable=True),
        ]
    ),
    "GoldEnvironmentalContext": StructType(
        [
            StructField("gold_environmental_context_id", StringType(), nullable=False),
            StructField("ecosystem", StringType(), nullable=True),
            StructField("ecosystem_category", StringType(), nullable=True),
            StructField("ecosystem_subtype", StringType(), nullable=True),
            StructField("ecosystem_type", StringType(), nullable=True),
            StructField("specific_ecosystem", StringType(), nullable=True),
        ]
    ),
    "MixsEnvironmentalContext": StructType(
        [
            StructField("mixs_environmental_context_id", StringType(), nullable=False),
            StructField("env_broad_scale", StringType(), nullable=True),
            StructField("env_local_scale", StringType(), nullable=True),
            StructField("env_medium", StringType(), nullable=True),
        ]
    ),
    "Event": StructType(
        [
            StructField("event_id", StringType(), nullable=False),
            StructField("created_at", DateType(), nullable=True),
            StructField("description", StringType(), nullable=True),
            StructField("name", StringType(), nullable=True),
            StructField("location", StringType(), nullable=True),
        ]
    ),
    "Experiment": StructType(
        [
            StructField("experiment_id", StringType(), nullable=False),
            StructField("created_at", DateType(), nullable=True),
            StructField("description", StringType(), nullable=True),
            StructField("name", StringType(), nullable=True),
        ]
    ),
    "Feature": StructType(
        [
            StructField("feature_id", StringType(), nullable=False),
            StructField("hash", StringType(), nullable=True),
            StructField("cds_phase", StringType(), nullable=True),
            StructField("e_value", FloatType(), nullable=True),
            StructField("end", IntegerType(), nullable=True),
            StructField("p_value", FloatType(), nullable=True),
            StructField("start", IntegerType(), nullable=True),
            StructField("strand", StringType(), nullable=True),
            StructField("source_database", StringType(), nullable=True),
            StructField("protocol_id", StringType(), nullable=True),
            StructField("type", StringType(), nullable=True),
        ]
    ),
    "Project": StructType(
        [
            StructField("project_id", StringType(), nullable=False),
            StructField("description", StringType(), nullable=True),
        ]
    ),
    "Protein": StructType(
        [
            StructField("protein_id", StringType(), nullable=False),
            StructField("hash", StringType(), nullable=True),
            StructField("description", StringType(), nullable=True),
            StructField("evidence_for_existence", StringType(), nullable=True),
            StructField("length", IntegerType(), nullable=True),
            StructField("sequence", StringType(), nullable=True),
        ]
    ),
    "Protocol": StructType(
        [
            StructField("protocol_id", StringType(), nullable=False),
            StructField("doi", StringType(), nullable=True),
            StructField("description", StringType(), nullable=True),
            StructField("version", StringType(), nullable=True),
            StructField("url", StringType(), nullable=True),
        ]
    ),
    "ProtocolParticipant": StructType(
        [
            StructField("protocol_participant_id", StringType(), nullable=False),
        ]
    ),
    "Publication": StructType(
        [
            StructField("publication_id", StringType(), nullable=False),
        ]
    ),
    "Sample": StructType(
        [
            StructField("sample_id", StringType(), nullable=False),
            StructField("description", StringType(), nullable=True),
            StructField("type", StringType(), nullable=True),
        ]
    ),
    "Sequence": StructType(
        [
            StructField("sequence_id", StringType(), nullable=False),
            StructField("entity_id", StringType(), nullable=False),
            StructField("type", StringType(), nullable=True),
            StructField("length", IntegerType(), nullable=True),
            StructField("checksum", StringType(), nullable=True),
        ]
    ),
    "Entity": StructType(
        [
            StructField("entity_id", StringType(), nullable=False),
            StructField("data_source_id", StringType(), nullable=False),
            StructField("entity_type", StringType(), nullable=False),
            StructField("data_source_entity_id", StringType(), nullable=True),
            StructField("data_source_created", DateType(), nullable=False),
            StructField("data_source_updated", DateType(), nullable=True),
            StructField("created", DateType(), nullable=False),
            StructField("updated", DateType(), nullable=False),
        ]
    ),
    "Identifier": StructType(
        [
            StructField("entity_id", StringType(), nullable=False),
            StructField("identifier", StringType(), nullable=False),
            StructField("description", StringType(), nullable=True),
            StructField("source", StringType(), nullable=True),
            StructField("relationship", StringType(), nullable=True),
        ]
    ),
    "Name": StructType(
        [
            StructField("entity_id", StringType(), nullable=False),
            StructField("name", StringType(), nullable=False),
            StructField("description", StringType(), nullable=True),
            StructField("source", StringType(), nullable=True),
        ]
    ),
    "QuantityValue": StructType(
        [
            StructField("maximum_value", FloatType(), nullable=True),
            StructField("minimum_value", FloatType(), nullable=True),
            StructField("value", FloatType(), nullable=True),
            StructField("unit", StringType(), nullable=True),
            StructField("entity_id", StringType(), nullable=False),
            StructField("attribute_name", StringType(), nullable=False),
            StructField("attribute_cv_term_id", StringType(), nullable=True),
            StructField("raw_value", StringType(), nullable=True),
        ]
    ),
    "TextValue": StructType(
        [
            StructField("value", StringType(), nullable=False),
            StructField("value_cv_term_id", StringType(), nullable=True),
            StructField("language", StringType(), nullable=True),
            StructField("entity_id", StringType(), nullable=False),
            StructField("attribute_name", StringType(), nullable=False),
            StructField("attribute_cv_term_id", StringType(), nullable=True),
            StructField("raw_value", StringType(), nullable=True),
        ]
    ),
    "Measurement": StructType(
        [
            StructField("measurement_id", StringType(), nullable=False),
            StructField("protocol_id", StringType(), nullable=False),
            StructField("created_at", DateType(), nullable=True),
            StructField("quality", StringType(), nullable=True),
            StructField("maximum_value", FloatType(), nullable=True),
            StructField("minimum_value", FloatType(), nullable=True),
            StructField("value", FloatType(), nullable=True),
            StructField("unit", StringType(), nullable=True),
            StructField("entity_id", StringType(), nullable=False),
            StructField("attribute_name", StringType(), nullable=False),
            StructField("attribute_cv_term_id", StringType(), nullable=True),
            StructField("raw_value", StringType(), nullable=True),
        ]
    ),
    "ProcessedMeasurement": StructType(
        [
            StructField("measurement_id", StringType(), nullable=False),
            StructField("protocol_id", StringType(), nullable=False),
            StructField("created_at", DateType(), nullable=True),
            StructField("quality", StringType(), nullable=True),
            StructField("maximum_value", FloatType(), nullable=True),
            StructField("minimum_value", FloatType(), nullable=True),
            StructField("value", FloatType(), nullable=True),
            StructField("unit", StringType(), nullable=True),
            StructField("entity_id", StringType(), nullable=False),
            StructField("attribute_name", StringType(), nullable=False),
            StructField("attribute_cv_term_id", StringType(), nullable=True),
            StructField("raw_value", StringType(), nullable=True),
        ]
    ),
    "Prefix": StructType(
        [
            StructField("prefix", StringType(), nullable=True),
            StructField("base", StringType(), nullable=True),
        ]
    ),
    "Statements": StructType(
        [
            StructField("subject", StringType(), nullable=True),
            StructField("predicate", StringType(), nullable=True),
            StructField("object", StringType(), nullable=True),
            StructField("value", StringType(), nullable=True),
            StructField("datatype", StringType(), nullable=True),
            StructField("language", StringType(), nullable=True),
        ]
    ),
    "EntailedEdge": StructType(
        [
            StructField("subject", StringType(), nullable=True),
            StructField("predicate", StringType(), nullable=True),
            StructField("object", StringType(), nullable=True),
        ]
    ),
    "Geolocation": StructType(
        [
            StructField("latitude", StringType(), nullable=False),
            StructField("longitude", StringType(), nullable=False),
            StructField("raw_value", StringType(), nullable=True),
            StructField("entity_id", StringType(), nullable=False),
            StructField("attribute_name", StringType(), nullable=False),
            StructField("attribute_cv_term_id", StringType(), nullable=True),
        ]
    ),
    "Association_X_Publication": StructType(
        [
            StructField("association_id", StringType(), nullable=False),
            StructField("publication_id", StringType(), nullable=False),
        ]
    ),
    "Association_X_SupportingObject": StructType(
        [
            StructField("association_id", StringType(), nullable=False),
            StructField("entity_id", StringType(), nullable=False),
        ]
    ),
    "Contig_X_ContigCollection": StructType(
        [
            StructField("contig_id", StringType(), nullable=False),
            StructField("contig_collection_id", StringType(), nullable=False),
        ]
    ),
    "Contig_X_EncodedFeature": StructType(
        [
            StructField("contig_id", StringType(), nullable=False),
            StructField("encoded_feature_id", StringType(), nullable=False),
        ]
    ),
    "Contig_X_Feature": StructType(
        [
            StructField("contig_id", StringType(), nullable=False),
            StructField("feature_id", StringType(), nullable=False),
        ]
    ),
    "Contig_X_Protein": StructType(
        [
            StructField("contig_id", StringType(), nullable=False),
            StructField("protein_id", StringType(), nullable=False),
        ]
    ),
    "ContigCollection_X_EncodedFeature": StructType(
        [
            StructField("contig_collection_id", StringType(), nullable=False),
            StructField("encoded_feature_id", StringType(), nullable=False),
        ]
    ),
    "ContigCollection_X_Feature": StructType(
        [
            StructField("contig_collection_id", StringType(), nullable=False),
            StructField("feature_id", StringType(), nullable=False),
        ]
    ),
    "ContigCollection_X_Protein": StructType(
        [
            StructField("contig_collection_id", StringType(), nullable=False),
            StructField("protein_id", StringType(), nullable=False),
        ]
    ),
    "Contributor_X_Role_X_Experiment": StructType(
        [
            StructField("contributor_id", StringType(), nullable=False),
            StructField("experiment_id", StringType(), nullable=False),
            StructField("contributor_role", StringType(), nullable=True),
        ]
    ),
    "Contributor_X_Role_X_Project": StructType(
        [
            StructField("contributor_id", StringType(), nullable=False),
            StructField("project_id", StringType(), nullable=False),
            StructField("contributor_role", StringType(), nullable=True),
        ]
    ),
    "EncodedFeature_X_Feature": StructType(
        [
            StructField("encoded_feature_id", StringType(), nullable=False),
            StructField("feature_id", StringType(), nullable=False),
        ]
    ),
    "Entity_X_Measurement": StructType(
        [
            StructField("entity_id", StringType(), nullable=False),
            StructField("measurement_id", StringType(), nullable=False),
        ]
    ),
    "Experiment_X_Project": StructType(
        [
            StructField("experiment_id", StringType(), nullable=False),
            StructField("project_id", StringType(), nullable=False),
        ]
    ),
    "Experiment_X_Sample": StructType(
        [
            StructField("experiment_id", StringType(), nullable=False),
            StructField("sample_id", StringType(), nullable=False),
        ]
    ),
    "Feature_X_Protein": StructType(
        [
            StructField("feature_id", StringType(), nullable=False),
            StructField("protein_id", StringType(), nullable=False),
        ]
    ),
    "Protocol_X_ProtocolParticipant": StructType(
        [
            StructField("protocol_id", StringType(), nullable=False),
            StructField("protocol_participant_id", StringType(), nullable=False),
            StructField("participant_type", StringType(), nullable=True),
        ]
    ),
}
