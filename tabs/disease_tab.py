import streamlit as st
from utils import query_opentargets, display_results
from queries.disease_queries import DISEASE_QUERIES

def display():
    with st.container():
        st.markdown(
            """
            <div style="background-color: #e7f4e4; padding: 10px; border-radius: 5px;">
                <h2 style="color: #4a8e4a; text-align: center;">🩺 Disease Use Cases</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Fixed and Dynamic Use Case Selection
        mode = st.radio(
            "Select Mode:",
            ["Fixed Use Cases", "Dynamic Use Cases"],
            key="disease_mode",
            help="Choose between pre-configured and dynamic use cases.",
        )

        query_display = None  # Store the query for later display

        try:
            if mode == "Fixed Use Cases":
                use_case = st.selectbox(
                    "Select a Fixed Disease Use Case",
                    [
                        "Retrieve tissue expression for Breast Cancer",
                        "Retrieve clinical compounds for Alopecia",
                    ],
                    key="disease_fixed_use_case",
                    help="Choose a pre-configured use case to fetch disease-related data.",
                )
                if st.button("Fetch Data", key="disease_fixed_fetch"):
                    if use_case == "Retrieve tissue expression for Breast Cancer":
                        query_display = DISEASE_QUERIES["breast_cancer_tissue_expression"]
                        result = query_opentargets(query_display)
                        rows = result.get("data", {}).get("disease", {}).get("associatedTargets", {}).get("rows", [])
                        data = []
                        for row in rows:
                            for expr in row["target"]["expressions"]:
                                data.append({
                                    "Tissue": expr["tissue"]["label"],
                                    "Protein Level": expr["protein"]["level"]
                                })
                        st.markdown("### Response Table: Tissue Expression for Breast Cancer")
                        display_results(data)

                    elif use_case == "Retrieve clinical compounds for Alopecia":
                        query_display = DISEASE_QUERIES["clinical_compounds_by_id"]
                        result = query_opentargets(query_display, {"efoId": "EFO_0000724"})
                        drugs = result.get("data", {}).get("disease", {}).get("knownDrugs", {}).get("rows", [])
                        data = [{"Drug Name": d["drug"]["name"], "Phase": d["phase"]} for d in drugs]
                        st.markdown("### Response Table: Clinical Compounds for Alopecia")
                        display_results(data)

            elif mode == "Dynamic Use Cases":
                use_case = st.selectbox(
                    "Select a Dynamic Disease Use Case",
                    [
                        "Retrieve approved compounds for a disease",
                        "Search diseases by keyword",
                    ],
                    key="disease_dynamic_use_case",
                    help="Select a dynamic use case and input disease-specific parameters to fetch data.",
                )
                if use_case == "Search diseases by keyword":
                    query_string = st.text_input(
                        "Enter keyword to search diseases:",
                        key="search_query",
                        help="Provide a keyword to search for diseases (e.g., Alopecia).",
                    )
                    if st.button("Search Diseases"):
                        query_display = DISEASE_QUERIES["search_diseases"]
                        result = query_opentargets(query_display, {"queryString": query_string})
                        diseases = result.get("data", {}).get("search", {}).get("hits", [])
                        data = [{"Disease ID": d["id"], "Description": d["description"]} for d in diseases if d["entity"] == "disease"]
                        st.markdown("### Response Table: Search Results for Diseases")
                        display_results(data)

                elif use_case == "Retrieve approved compounds for a disease":
                    efo_id = st.text_input(
                        "Enter EFO ID:",
                        key="disease_dynamic_efo_id",
                        help="Provide the EFO ID for the disease (e.g., EFO_0000349).",
                    )
                    if st.button("Fetch Data", key="disease_dynamic_fetch") and efo_id:
                        query_display = DISEASE_QUERIES["clinical_compounds_by_id"]
                        result = query_opentargets(query_display, {"efoId": efo_id})
                        drugs = result.get("data", {}).get("disease", {}).get("knownDrugs", {}).get("rows", [])
                        data = [{"Drug Name": d["drug"]["name"], "Phase": d["phase"]} for d in drugs]
                        st.markdown("### Response Table: Approved Compounds for the Disease")
                        display_results(data)

        except Exception as e:
            st.error(f"An error occurred in the Disease tab: {e}")

        # Query Display Section
        if query_display:
            with st.expander("Query Executed"):
                st.code(query_display, language="graphql")
