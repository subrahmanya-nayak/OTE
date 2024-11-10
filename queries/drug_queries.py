DRUG_QUERIES = {
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
    """,
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
    """
}
