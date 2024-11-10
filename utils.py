import streamlit as st
import requests
import pandas as pd

# API Base URL
BASE_URL = "https://api.platform.opentargets.org/api/v4/graphql"

# Function to query the Open Targets API
def query_opentargets(query, variables=None):
    headers = {"Content-Type": "application/json"}
    response = requests.post(BASE_URL, json={"query": query, "variables": variables}, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return None

# Function to display results using st.dataframe
def display_results(data):
    if not data:
        st.write("No results found.")
        return
    
    # Convert data to DataFrame
    df = pd.DataFrame(data)
    
    # Display the DataFrame with st.dataframe (includes built-in export to CSV)
    st.dataframe(df, use_container_width=True)