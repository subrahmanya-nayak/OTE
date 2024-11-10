import streamlit as st
from tabs import drug_tab, disease_tab, target_tab

st.title("Open Targets Explorer")

# Tabs for Use Cases
tab1, tab2, tab3 = st.tabs(["Drug Use Cases", "Disease Use Cases", "Target Use Cases"])

with tab1:
    drug_tab.display()

with tab2:
    disease_tab.display()

with tab3:
    target_tab.display()
