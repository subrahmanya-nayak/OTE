DISEASE_QUERIES = {
    "breast_cancer_tissue_expression": """
    query {
        disease(efoId: "EFO_0000305") {
            associatedTargets {
                rows {
                    target {
                        expressions {
                            tissue {
                                label
                            }
                            protein {
                                level
                            }
                        }
                    }
                }
            }
        }
    }
    """,
    "clinical_compounds_by_id": """
    query ($efoId: String!) {
        disease(efoId: $efoId) {
            knownDrugs {
                rows {
                    drug {
                        name
                    }
                    phase
                }
            }
        }
    }
    """,
    "search_diseases": """
    query ($queryString: String!) {
        search(queryString: $queryString) {
            hits {
                id
                entity
                description
            }
        }
    }
    """
}
