import streamlit as st
from utils import query_opentargets, display_results
from queries.disease_queries import DISEASE_QUERIES

def display():
    st.header("Disease Use Cases")
    mode = st.radio("Select Mode", ["Fixed Use Cases", "Dynamic Use Cases"], key="disease_mode")

    try:
        if mode == "Fixed Use Cases":
            use_case = st.selectbox("Select a Fixed Disease Use Case", [
                "Retrieve tissue expression for Breast Cancer",
                "Retrieve clinical compounds for Alopecia"
            ], key="disease_fixed_use_case")
            if st.button("Fetch Data", key="disease_fixed_fetch"):
                if use_case == "Retrieve tissue expression for Breast Cancer":
                    result = query_opentargets(DISEASE_QUERIES["breast_cancer_tissue_expression"])
                    targets = result.get("data", {}).get("disease", {}).get("associatedTargets", {}).get("rows", [])
                    data = []
                    for target in targets:
                        for expr in target["target"]["expressions"]:
                            data.append({
                                "Tissue": expr["tissue"]["label"],
                                "Protein Level": expr["protein"]["level"]
                            })
                    display_results(data)

                elif use_case == "Retrieve clinical compounds for Alopecia":
                    result = query_opentargets(DISEASE_QUERIES["alopecia_clinical_compounds"])
                    drugs = result.get("data", {}).get("disease", {}).get("knownDrugs", {}).get("rows", [])
                    data = [{"Drug Name": d["drug"]["name"], "Phase": d["phase"]} for d in drugs]
                    display_results(data)

        elif mode == "Dynamic Use Cases":
            use_case = st.selectbox("Select a Dynamic Disease Use Case", [
                "Retrieve approved compounds for a disease",
                "Retrieve protein expression in brain regions for a disease"
            ], key="disease_dynamic_use_case")
            efo_id = st.text_input("Enter EFO ID:", key="disease_dynamic_efo_id")
            if st.button("Fetch Data", key="disease_dynamic_fetch") and efo_id:
                if use_case == "Retrieve approved compounds for a disease":
                    result = query_opentargets(DISEASE_QUERIES["approved_compounds"], {"efoId": efo_id})
                    drugs = result.get("data", {}).get("disease", {}).get("knownDrugs", {}).get("rows", [])
                    data = [{"Drug Name": d["drug"]["name"], "Phase": d["phase"]} for d in drugs]
                    display_results(data)

                elif use_case == "Retrieve protein expression in brain regions for a disease":
                    result = query_opentargets(DISEASE_QUERIES["brain_protein_expression"], {"efoId": efo_id})
                    targets = result.get("data", {}).get("disease", {}).get("associatedTargets", {}).get("rows", [])
                    data = []
                    for target in targets:
                        for expr in target["target"]["expressions"]:
                            data.append({
                                "Tissue": expr["tissue"]["label"],
                                "Protein Level": expr["protein"]["level"]
                            })
                    display_results(data)

    except Exception as e:
        st.error(f"An error occurred in the Disease tab: {e}")
