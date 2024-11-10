import streamlit as st
from utils import query_opentargets

def display():
    with st.container():
        st.markdown(
            """
            <div style="background-color: #f7f9fc; padding: 10px; border-radius: 5px;">
                <h2 style="color: #0077cc; text-align: center;">🛠️ Query Testing Tool</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # Input for Custom Query
        st.markdown("### GraphQL Query")
        custom_query = st.text_area("Enter your GraphQL query below:", height=200)

        # Optional Query Variables
        st.markdown("### Query Variables (Optional, JSON format)")
        variables = st.text_area(
            "Enter query variables in JSON format (if required):",
            height=100,
            help="Provide variables for the query. For example: {\"ensemblId\": \"ENSG00000167552\"}. Leave empty if not needed.",
        )

        if st.button("Run Query"):
            try:
                # Parse variables if provided
                var_data = None
                if variables.strip():
                    var_data = eval(variables)  # Convert string to dictionary (ensure JSON-like format)

                # Execute the query
                result = query_opentargets(custom_query, var_data)

                # Display Raw JSON Results
                st.markdown("### Query Results")
                if result:
                    with st.expander("View Raw Results"):
                        st.json(result)
                else:
                    st.error("No results found or an error occurred.")

            except Exception as e:
                st.error(f"An error occurred while executing the query: {e}")
