import streamlit as st
from tabs import drug_tab, disease_tab, target_tab

# Page Configuration
st.set_page_config(
    page_title="Open Targets Explorer",
    page_icon="🔍",
    layout="centered",  # Default layout to centered
    initial_sidebar_state="expanded"
)

# Custom CSS for Sidebar
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        padding: 20px;
    }
    .sidebar .sidebar-content h2 {
        color: #4a4a8e;
        margin-top: 10px;
        margin-bottom: 10px;
        font-size: 1.2rem;
    }
    .sidebar .sidebar-content .block-container {
        background-color: #f9f9f9;
        border-radius: 5px;
        padding: 15px;
    }
    .sidebar .sidebar-content hr {
        margin: 15px 0;
        border: none;
        height: 1px;
        background-color: #ccc;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar Navigation
st.sidebar.title("🔍 Open Targets Explorer")
st.sidebar.markdown(
    """
    Explore drug, disease, and target associations using the Open Targets platform.
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

# Use Case Navigation with Separators
st.sidebar.markdown("**Navigate Between Use Cases**")
options = st.sidebar.radio(
    "Select a Tab",
    ["Drug Use Cases", "Disease Use Cases", "Target Use Cases"],
    index=0,
    format_func=lambda x: f"📂 {x}" if x == "Drug Use Cases" else f"🩺 {x}" if x == "Disease Use Cases" else f"🧬 {x}",
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

# Main Page
if options == "Drug Use Cases":
    drug_tab.display()
elif options == "Disease Use Cases":
    disease_tab.display()
elif options == "Target Use Cases":
    target_tab.display()
