import streamlit as st
from utils import query_opentargets, display_results
from queries.target_queries import TARGET_QUERIES

def display():
    st.header("Target Use Cases")
    mode = st.radio("Select Mode", ["Fixed Use Cases", "Dynamic Use Cases"], key="target_mode")

    try:
        if mode == "Fixed Use Cases":
            use_case = st.selectbox("Select a Fixed Target Use Case", [
                "List preclinical, clinical, and approved drugs for JAK2",
                "List high-expression cancers for JAK2"
            ], key="target_fixed_use_case")
            if st.button("Fetch Data", key="target_fixed_fetch"):
                if use_case == "List preclinical, clinical, and approved drugs for JAK2":
                    result = query_opentargets(TARGET_QUERIES["jak2_preclinical_drugs"])
                    drugs = result.get("data", {}).get("target", {}).get("knownDrugs", {}).get("rows", [])
                    data = [{"Drug Name": d["drug"]["name"], "Phase": d["phase"], "Mechanism": d["mechanismOfAction"]} for d in drugs]
                    display_results(data)

                elif use_case == "List high-expression cancers for JAK2":
                    result = query_opentargets(TARGET_QUERIES["jak2_high_expression_cancers"])
                    expressions = result.get("data", {}).get("target", {}).get("expressions", [])
                    data = [{"Tissue": e["tissue"]["label"], "Z-Score": e["rna"]["zscore"]} for e in expressions]
                    display_results(data)

        elif mode == "Dynamic Use Cases":
            use_case = st.selectbox("Select a Dynamic Target Use Case", [
                "Retrieve compounds for a target",
                "Retrieve cancers with high expression for a target"
            ], key="target_dynamic_use_case")
            ensembl_id = st.text_input("Enter Ensembl ID:", key="target_dynamic_ensembl_id")
            if st.button("Fetch Data", key="target_dynamic_fetch") and ensembl_id:
                if use_case == "Retrieve compounds for a target":
                    result = query_opentargets(TARGET_QUERIES["target_compounds"], {"ensemblId": ensembl_id})
                    drugs = result.get("data", {}).get("target", {}).get("knownDrugs", {}).get("rows", [])
                    data = [{"Drug Name": d["drug"]["name"], "Mechanism of Action": d["mechanismOfAction"]} for d in drugs]
                    display_results(data)

                elif use_case == "Retrieve cancers with high expression for a target":
                    result = query_opentargets(TARGET_QUERIES["cancer_high_expression"], {"ensemblId": ensembl_id})
                    expressions = result.get("data", {}).get("target", {}).get("expressions", [])
                    data = [{"Tissue": e["tissue"]["label"], "Z-Score": e["rna"]["zscore"]} for e in expressions]
                    display_results(data)

    except Exception as e:
        st.error(f"An error occurred in the Target tab: {e}")
