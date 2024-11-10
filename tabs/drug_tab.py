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
    st.header("Drug Use Cases")
    mode = st.radio("Select Mode", ["Fixed Use Cases", "Dynamic Use Cases"], key="drug_mode")

    try:
        if mode == "Fixed Use Cases":
            use_case = st.selectbox("Select a Fixed Drug Use Case", [
                "Imatinib Phase 2 Diseases",
                "Rituximab Approved Diseases"
            ], key="drug_fixed_use_case")
            if st.button("Fetch Data", key="drug_fixed_fetch"):
                if use_case == "Imatinib Phase 2 Diseases":
                    result = query_opentargets(DRUG_QUERIES["imatinib_phase_2"])
                    rows = result.get("data", {}).get("drug", {}).get("indications", {}).get("rows", [])
                    data = [{"Disease": r["disease"]["name"], "Max Phase": r["maxPhaseForIndication"]} for r in rows if r.get("disease")]
                    display_results(data)

                elif use_case == "Rituximab Approved Diseases":
                    result = query_opentargets(DRUG_QUERIES["rituximab_approved"])
                    rows = result.get("data", {}).get("drug", {}).get("indications", {}).get("rows", [])
                    data = [{"Disease": r["disease"]["name"], "Max Phase": r["maxPhaseForIndication"]} for r in rows if r.get("disease")]
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
                    result = query_opentargets(DRUG_QUERIES["diseases_phase_2"], {"chemblId": chembl_id})
                    rows = result.get("data", {}).get("drug", {}).get("indications", {}).get("rows", [])
                    data = [{"Disease": r["disease"]["name"], "Max Phase": r["maxPhaseForIndication"]} for r in rows if r.get("disease")]
                    display_results(data)

                elif use_case == "Adverse Events for a Drug":
                    result = query_opentargets(DRUG_QUERIES["adverse_events"], {"chemblId": chembl_id})
                    adverse_events = result.get("data", {}).get("drug", {}).get("adverseEvents", {}).get("rows", [])
                    data = [{"Event Name": ae["name"], "Count": ae["count"]} for ae in adverse_events]
                    display_results(data)

    except Exception as e:
        st.error(f"An error occurred in the Drug tab: {e}")
