import streamlit as st
import requests
import pandas as pd

BASE_URL = "https://api.platform.opentargets.org/api/v4/graphql"

def query_opentargets(query, variables=None):
    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

def query_clinvar_for_pathogenic_snps(gene_name):
    """
    Query ClinVar for pathogenic SNPs associated with a gene.
    Fetch only SNPs with 'Pathogenic' or 'Likely Pathogenic' significance.
    """
    try:
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term={gene_name}[gene]+AND+(pathogenic[clinical_significance]+OR+likely_pathogenic[clinical_significance])&retmode=json"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        st.error(f"Error querying ClinVar: {e}")
        return []

def fetch_clinvar_details(variation_ids):
    """
    Fetch detailed information about variations from ClinVar.
    Returns details such as:
    - Identifiers (e.g., NM IDs)
    - Variation ID
    - Accession
    """
    details = []
    try:
        for variation_id in variation_ids:
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=clinvar&id={variation_id}&retmode=json"
            response = requests.get(url)
            response.raise_for_status()
            variation = response.json().get("result", {}).get(str(variation_id), {})

            # Extract identifiers, variation ID, and accession
            identifiers = variation.get("title", "N/A")
            variation_id_field = variation_id  # Just the ID
            accession = variation.get("accession", "N/A")  # Just the accession number

            details.append({
                "Identifiers": identifiers,
                "Variation ID": variation_id_field,
                "Accession": accession,
            })
    except Exception as e:
        st.error(f"Error fetching ClinVar details: {e}")
    return details

def display_results(data):
    if not data:
        st.write("No results found.")
        return
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
