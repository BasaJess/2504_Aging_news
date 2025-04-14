import streamlit as st
from openai import OpenAI
import numpy as np
import random
import time

#import pandas as pd


#from LLMver00 import return_my_question
import importlib
load_other_file = importlib.import_module("34_Most_relevant_docs_list_maker")
retrieve_most_relevant_docs_for_streamlit = load_other_file.retrieve_most_relevant_docs_for_streamlit
#load_other_file = importlib.import_module("00_deprecated_30_LLM_ver00")
#return_my_question = load_other_file.return_my_question


from pathlib import Path
st.write("File path :" , Path(__file__).absolute() )
#st.write("File path :" , Path().absolute() )

# Set OpenAI API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set a default model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def handle_input(user_input):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
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

def ask_30_LLM_latest_findings():
    # Simulate a function that returns a question
    return return_my_question()


# Sidebar for the button
with st.sidebar:
    if st.button("Click me :)"):
        # call the most relevant documents
        df = retrieve_most_relevant_docs_for_streamlit()
        # display the df
        st.dataframe(df,use_container_width=True)
        simulated_input = "What time is in London?"# ask_30_LLM_latest_findings()
        handle_input(simulated_input)

# Accept user input
if prompt := st.chat_input("What is up?"):
    handle_input(prompt)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write(df)
