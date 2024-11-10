import streamlit as st
from tabs import drug_tab, disease_tab, target_tab, query_testing_tab

# Page Configuration
st.set_page_config(
    page_title="Open Targets Explorer",
    page_icon="🔍",
    layout="centered",  # Default layout
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
st.sidebar.title("🔍 Open Targets Explorer")
st.sidebar.markdown(
    """
    Explore drug, disease, and target associations using the Open Targets platform.
    """
)
st.sidebar.markdown("---")

# Use Case Navigation
options = st.sidebar.radio(
    "Select a Tab",
    [
        "Drug Use Cases",
        "Disease Use Cases",
        "Target Use Cases",
        "Query Testing Tool",
    ],
    index=0,
    format_func=lambda x: f"📂 {x}" if x == "Drug Use Cases" else f"🩺 {x}" if x == "Disease Use Cases" else f"🧬 {x}" if x == "Target Use Cases" else f"🛠️ {x}",
)
st.sidebar.markdown("---")

# Footer in Sidebar
st.sidebar.markdown(
    """
    <div style="text-align: center; font-size: 0.85rem; color: gray;">
        Built with ❤️ using <b>Streamlit</b> | © 2024 Open Targets Explorer
    </div>
    """,
    unsafe_allow_html=True,
)

# Display selected tab
if options == "Drug Use Cases":
    drug_tab.display()
elif options == "Disease Use Cases":
    disease_tab.display()
elif options == "Target Use Cases":
    target_tab.display()
elif options == "Query Testing Tool":
    query_testing_tab.display()
