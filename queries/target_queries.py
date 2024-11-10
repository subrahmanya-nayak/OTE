TARGET_QUERIES = {
    "jak2_preclinical_drugs": """
    query {
        target(ensemblId: "ENSG00000167552") {
            knownDrugs {
                rows {
                    drug {
                        name
                    }
                    phase
                    status
                }
            }
        }
    }
    """,
    "cancer_high_expression": """
    query ($ensemblId: String!) {
        target(ensemblId: $ensemblId) {
            associatedDiseases {
                rows {
                    disease {
                        name
                    }
                    score
                }
            }
        }
    }
    """,
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
    """
}
