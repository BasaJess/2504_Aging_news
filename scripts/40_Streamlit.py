import streamlit as st
from openai import OpenAI
import numpy as np
import random
import time

#from LLMver00 import return_my_question
import importlib
load_other_file = importlib.import_module("30_LLM_ver00")
return_my_question = load_other_file.return_my_question

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
        simulated_input = ask_30_LLM_latest_findings()
        handle_input(simulated_input)

# Accept user input
if prompt := st.chat_input("What is up?"):
    handle_input(prompt)
