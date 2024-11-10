import streamlit as st
from utils import query_opentargets, display_results
from queries.target_queries import TARGET_QUERIES

def display():
    with st.container():
        st.markdown(
            """
            <div style="background-color: #e6f7ff; padding: 10px; border-radius: 5px;">
                <h2 style="color: #00509e; text-align: center;">🧬 Target Use Cases</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Fixed and Dynamic Use Case Selection
        mode = st.radio(
            "Select Mode:",
            ["Fixed Use Cases", "Dynamic Use Cases"],
            key="target_mode",
            help="Choose between pre-configured and dynamic use cases.",
        )

        query_display = None  # Store the query for later display

        try:
            if mode == "Fixed Use Cases":
                use_case = st.selectbox(
                    "Select a Fixed Target Use Case",
                    [
                        "List preclinical, clinical, and approved drugs for JAK2",
                        "Retrieve cancers with high expression for JAK2",
                    ],
                    key="target_fixed_use_case",
                    help="Choose a pre-configured use case to fetch data for a specific target.",
                )
                if st.button("Fetch Data", key="target_fixed_fetch"):
                    if use_case == "List preclinical, clinical, and approved drugs for JAK2":
                        query_display = TARGET_QUERIES["jak2_preclinical_drugs"]
                        result = query_opentargets(query_display)
                        drugs = result.get("data", {}).get("target", {}).get("knownDrugs", {}).get("rows", [])
                        data = [{"Drug Name": d["drug"]["name"], "Phase": d["phase"], "Status": d["status"]} for d in drugs]
                        st.markdown("### Response Table: Preclinical, Clinical, and Approved Drugs for JAK2")
                        display_results(data)

                    elif use_case == "Retrieve cancers with high expression for JAK2":
                        query_display = TARGET_QUERIES["cancer_high_expression"]
                        result = query_opentargets(query_display, {"ensemblId": "ENSG00000167552"})
                        diseases = result.get("data", {}).get("target", {}).get("associatedDiseases", {}).get("rows", [])
                        data = [{"Cancer": d["disease"]["name"], "Score": d["score"]} for d in diseases if d.get("disease")]
                        st.markdown("### Response Table: Cancers with High Expression for JAK2")
                        display_results(data)

            elif mode == "Dynamic Use Cases":
                use_case = st.selectbox(
                    "Select a Dynamic Target Use Case",
                    [
                        "Retrieve compounds for a target",
                        "Retrieve cancers with high expression for a target",
                    ],
                    key="target_dynamic_use_case",
                    help="Select a dynamic use case and input target-specific parameters to fetch data.",
                )
                ensembl_id = st.text_input(
                    "Enter Ensembl ID:",
                    key="target_dynamic_ensembl_id",
                    help="Provide the Ensembl ID for the target (e.g., ENSG00000169083).",
                )
                if st.button("Fetch Data", key="target_dynamic_fetch") and ensembl_id:
                    if use_case == "Retrieve compounds for a target":
                        query_display = TARGET_QUERIES["target_compounds"]
                        result = query_opentargets(query_display, {"ensemblId": ensembl_id})
                        drugs = result.get("data", {}).get("target", {}).get("knownDrugs", {}).get("rows", [])
                        data = [{"Drug Name": d["drug"]["name"], "Mechanism of Action": d["mechanismOfAction"]} for d in drugs]
                        st.markdown("### Response Table: Compounds for the Target")
                        display_results(data)

                    elif use_case == "Retrieve cancers with high expression for a target":
                        query_display = TARGET_QUERIES["cancer_high_expression"]
                        result = query_opentargets(query_display, {"ensemblId": ensembl_id})
                        diseases = result.get("data", {}).get("target", {}).get("associatedDiseases", {}).get("rows", [])
                        data = [{"Cancer": d["disease"]["name"], "Score": d["score"]} for d in diseases if d.get("disease")]
                        st.markdown("### Response Table: Cancers with High Expression for the Target")
                        display_results(data)

        except Exception as e:
            st.error(f"An error occurred in the Target tab: {e}")

        # Query Display Section
        if query_display:
            with st.expander("Query Executed"):
                st.code(query_display, language="graphql")
