import streamlit as st
import importlib
from openai import OpenAI
import pandas as pd

# Import your custom assistant
custom_llm = importlib.import_module("30_LLM_Assistant")

# Import the function to retrieve the most relevant documents
load_other_file = importlib.import_module("34_Most_relevant_docs_list_maker")
retrieve_most_relevant_docs_for_streamlit = load_other_file.retrieve_most_relevant_docs_for_streamlit

# Load OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# State initialization
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "use_custom_llm" not in st.session_state:
    st.session_state["use_custom_llm"] = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "relevant_df" not in st.session_state:
    st.session_state.relevant_df = pd.DataFrame()

# Function to handle user interaction
def handle_input(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Use selected LLM
    if st.session_state["use_custom_llm"]:
        with st.chat_message("assistant"):
            response = custom_llm.ask_30_LLM_latest_findings(user_input)
            st.markdown(response)
    else:
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})

# Sidebar controls
with st.sidebar:
    if st.button("Show 10 Most Relevant Papers"):
        st.session_state.relevant_df = retrieve_most_relevant_docs_for_streamlit()
        st.session_state.messages.append({
            "role": "assistant",
            "content": "According to my database, these are the latest 10 scientific papers most relevant to longevity and youth extension. Would you like details of any or a summary of all?"
        })

    # LLM Toggle
    st.session_state["use_custom_llm"] = st.checkbox("Use custom assistant (30_LLM_Assistant)?", value=False)

# Display relevant DataFrame if available
if not st.session_state.relevant_df.empty:
    st.dataframe(st.session_state.relevant_df, use_container_width=True)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask something..."):
    handle_input(prompt)
