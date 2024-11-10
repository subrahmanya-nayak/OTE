# Queries for Disease Use Cases
DISEASE_QUERIES = {
    # Fixed Use Cases
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
    "alopecia_clinical_compounds": """
    query {
        disease(efoId: "EFO_0000745") {
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
    # Dynamic Use Cases
    "approved_compounds": """
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
    "brain_protein_expression": """
    query ($efoId: String!) {
        disease(efoId: $efoId) {
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
    """
}
