# Queries for Target Use Cases
TARGET_QUERIES = {
    # Fixed Use Cases
    "jak2_preclinical_drugs": """
    query {
        target(ensemblId: "ENSG00000167552") {
            knownDrugs {
                rows {
                    drug {
                        name
                    }
                    phase
                    mechanismOfAction
                }
            }
        }
    }
    """,
    "jak2_high_expression_cancers": """
    query {
        target(ensemblId: "ENSG00000167552") {
            expressions {
                tissue {
                    label
                }
                rna {
                    zscore
                }
            }
        }
    }
    """,
    # Dynamic Use Cases
    "target_compounds": """
    query ($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
            knownDrugs {
                rows {
                    drug {
                        name
                    }
                    mechanismOfAction
                }
            }
        }
    }
    """,
    "cancer_high_expression": """
    query ($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
            expressions {
                tissue {
                    label
                }
                rna {
                    zscore
                }
            }
        }
    }
    """
}
