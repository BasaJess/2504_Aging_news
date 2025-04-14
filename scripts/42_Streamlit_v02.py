import streamlit as st
from openai import OpenAI
import importlib
import pandas as pd

# Load external modules
load_data_module = importlib.import_module("34_Most_relevant_docs_list_maker")
retrieve_most_relevant_docs_for_streamlit = load_data_module.retrieve_most_relevant_docs_for_streamlit

custom_llm_module = importlib.import_module("30_LLM_Assistant")
custom_agent = custom_llm_module.custom_llm_response  # assumes this is a function

# OpenAI client setup
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Session state setup
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "use_custom_llm" not in st.session_state:
    st.session_state["use_custom_llm"] = False

if "messages" not in st.session_state:
    st.session_state.messages = []

if "df_relevant" not in st.session_state:
    st.session_state.df_relevant = None

# Sidebar controls
with st.sidebar:
    if st.button("Click me :)"):
        st.session_state.df_relevant = retrieve_most_relevant_docs_for_streamlit()
        st.dataframe(st.session_state.df_relevant, use_container_width=True)

        # Trigger assistant greeting message
        greeting = (
            "According to my database, these are the latest 10 scientific papers most relevant to "
            "longevity and youth extension. Would you like details of any or a summary of all?"
        )
        st.session_state.messages.append({"role": "assistant", "content": greeting})
        with st.chat_message("assistant"):
            st.markdown(greeting)

    st.markdown("### LLM Selector")
    model_choice = st.radio("Choose the agent:", ("OpenAI", "Custom LLM"))
    st.session_state.use_custom_llm = (model_choice == "Custom LLM")


# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input handling
def handle_input(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response from selected LLM
    with st.chat_message("assistant"):
        if st.session_state.use_custom_llm:
            response = custom_agent(user_input, context=st.session_state.df_relevant)
            st.markdown(response)
        else:
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})


# Chat input field
if prompt := st.chat_input("What would you like to ask?"):
    handle_input(prompt)
