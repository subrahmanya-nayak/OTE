import streamlit as st
from utils import query_opentargets, display_results
from queries.drug_queries import DRUG_QUERIES

def get_chembl_id_from_name(drug_name):
    """Search for a drug by name and return its ChEMBL ID."""
    result = query_opentargets(DRUG_QUERIES["search_drug"], {"query": drug_name})
    hits = result.get("data", {}).get("search", {}).get("hits", [])
    if hits:
        return hits[0]["id"]  # Return the first match
    return None

def display():
    with st.container():
        # Section Header
        st.markdown(
            """
            <div style="background-color: #fff4e6; padding: 10px; border-radius: 5px;">
                <h2 style="color: #b45f06; text-align: center;">📂 Drug Use Cases</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Fixed and Dynamic Use Case Selection
        mode = st.radio(
            "Select Mode:",
            ["Fixed Use Cases", "Dynamic Use Cases"],
            key="drug_mode",
            help="Choose between pre-configured and dynamic use cases.",
        )

        query_display = None  # Store the query for later display

        try:
            if mode == "Fixed Use Cases":
                use_case = st.selectbox("Select a Fixed Drug Use Case", [
                    "Imatinib Phase 2 Diseases",
                    "Rituximab Approved Diseases"
                ], key="drug_fixed_use_case")
                if st.button("Fetch Data", key="drug_fixed_fetch"):
                    if use_case == "Imatinib Phase 2 Diseases":
                        query_display = DRUG_QUERIES["imatinib_phase_2"]
                        result = query_opentargets(query_display)
                        rows = result.get("data", {}).get("drug", {}).get("indications", {}).get("rows", [])
                        data = [{"Disease": r["disease"]["name"], "Max Phase": r["maxPhaseForIndication"]} for r in rows if r.get("disease")]
                        st.markdown("### Response Table: Results for Imatinib Phase 2 Diseases")
                        display_results(data)

                    elif use_case == "Rituximab Approved Diseases":
                        query_display = DRUG_QUERIES["rituximab_approved"]
                        result = query_opentargets(query_display)
                        rows = result.get("data", {}).get("drug", {}).get("indications", {}).get("rows", [])
                        data = [{"Disease": r["disease"]["name"], "Max Phase": r["maxPhaseForIndication"]} for r in rows if r.get("disease")]
                        st.markdown("### Response Table: Results for Rituximab Approved Diseases")
                        display_results(data)

            elif mode == "Dynamic Use Cases":
                use_case = st.selectbox("Select a Dynamic Drug Use Case", [
                    "Diseases in Phase 2 for a Drug",
                    "Adverse Events for a Drug"
                ], key="drug_dynamic_use_case")
                drug_name = st.text_input("Enter Drug Name:", key="drug_dynamic_name")
                if st.button("Fetch Data", key="drug_dynamic_fetch") and drug_name:
                    chembl_id = get_chembl_id_from_name(drug_name)
                    if not chembl_id:
                        st.error(f"No ChEMBL ID found for drug: {drug_name}")
                        return

                    if use_case == "Diseases in Phase 2 for a Drug":
                        query_display = DRUG_QUERIES["diseases_phase_2"]
                        result = query_opentargets(query_display, {"chemblId": chembl_id})
                        rows = result.get("data", {}).get("drug", {}).get("indications", {}).get("rows", [])
                        data = [{"Disease": r["disease"]["name"], "Max Phase": r["maxPhaseForIndication"]} for r in rows if r.get("disease")]
                        st.markdown("### Response Table: Results for Diseases in Phase 2")
                        display_results(data)

                    elif use_case == "Adverse Events for a Drug":
                        query_display = DRUG_QUERIES["adverse_events"]
                        result = query_opentargets(query_display, {"chemblId": chembl_id})
                        adverse_events = result.get("data", {}).get("drug", {}).get("adverseEvents", {}).get("rows", [])
                        data = [{"Event Name": ae["name"], "Count": ae["count"]} for ae in adverse_events]
                        st.markdown("### Response Table: Adverse Events for the Drug")
                        display_results(data)

        except Exception as e:
            st.error(f"An error occurred in the Drug tab: {e}")

        # Query Display Section
        if query_display:
            with st.expander("Query Executed"):
                st.code(query_display, language="graphql")
