import streamlit as st
import importlib
import pandas as pd
import json

# Import the function to retrieve the most relevant documents
load_other_file = importlib.import_module("34_Most_relevant_docs_list_maker")
retrieve_most_relevant_docs_for_streamlit = load_other_file.retrieve_most_relevant_docs_for_streamlit

# Title and description
st.title("Top 10 Most Relevant Scientific Papers")
st.markdown("""
This tool retrieves the **10 latest and most relevant scientific papers** 
focused on longevity and youth extension. 

Click the button below to fetch, explore, and export the results.
""")

# Initialize session state for dataframe
if "relevant_df" not in st.session_state:
    st.session_state.relevant_df = pd.DataFrame()

# Button to retrieve relevant documents
if st.button("Show 10 Most Relevant Papers"):
    st.session_state.relevant_df = retrieve_most_relevant_docs_for_streamlit()

# Display the DataFrame
if not st.session_state.relevant_df.empty:
    st.markdown("### 📄 Results Table")

    # Show sorting-enabled table with full width
    st.dataframe(
        st.session_state.relevant_df.sort_values(by=["Relevance_for_longevity", "Date"], ascending=[False, False]),
        use_container_width=True
    )

    # Export options
    st.markdown("### 📁 Export Results")
    csv = st.session_state.relevant_df.to_csv(index=False)
    json_data = st.session_state.relevant_df.to_json(orient="records", indent=2)

    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="top_10_relevant_papers.csv",
        mime="text/csv"
    )

    st.download_button(
        label="Download as JSON",
        data=json_data,
        file_name="top_10_relevant_papers.json",
        mime="application/json"
    )

    # Optional: Show individual summaries under each row
    st.markdown("### 📚 Paper Summaries")
    for index, row in st.session_state.relevant_df.iterrows():
        with st.expander(f"{index+1}. {row['Summary'][:100]}..."):
            st.write(f"**Author:** {row['Author']}")
            st.write(f"**Date:** {row['Date']}")
            st.write(f"**Institution:** {row['Institution']}")
            st.write(f"**Peer Reviewed:** {row['Peer_Reviewed']}")
            st.write(f"**Relevance Score:** {row['Relevance_for_longevity']}")
            st.write("\n")
            st.write(row['Summary'])
