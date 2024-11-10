DRUG_QUERIES = {
    # Search Query to Get ChEMBL ID from Drug Name
    "search_drug": """
    query ($query: String!) {
        search(queryString: $query, entityNames: ["drug"]) {
            hits {
                id
                name
                description
            }
        }
    }
    """,
    # Fixed Use Case: Imatinib Phase 2
    "imatinib_phase_2": """
    query {
        drug(chemblId: "CHEMBL941") {
            indications {
                rows {
                    disease {
                        name
                    }
                    maxPhaseForIndication
                }
            }
        }
    }
    """,
    # Fixed Use Case: Rituximab Approved
    "rituximab_approved": """
    query {
        drug(chemblId: "CHEMBL1201589") {
            indications {
                rows {
                    disease {
                        name
                    }
                    maxPhaseForIndication
                }
            }
        }
    }
    """,
    # Dynamic Use Case: Phase 2 Diseases for Any Drug
    "diseases_phase_2": """
    query ($chemblId: String!) {
        drug(chemblId: $chemblId) {
            indications {
                rows {
                    disease {
                        name
                    }
                    maxPhaseForIndication
                }
            }
        }
    }
    """,
    # Dynamic Use Case: Adverse Events for Any Drug
    "adverse_events": """
    query ($chemblId: String!) {
        drug(chemblId: $chemblId) {
            adverseEvents {
                rows {
                    name
                    count
                }
            }
        }
    }
    """
}
