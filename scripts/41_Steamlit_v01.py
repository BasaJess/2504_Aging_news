import streamlit as st
from openai import OpenAI
import importlib
import pandas as pd

# Import your custom function
load_other_file = importlib.import_module("34_Most_relevant_docs_list_maker")
retrieve_most_relevant_docs_for_streamlit = load_other_file.retrieve_most_relevant_docs_for_streamlit

# Optionally import custom agent
custom_agent = importlib.import_module("30_LLM_Assistant")

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Initialize session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "latest_df" not in st.session_state:
    st.session_state.latest_df = None
if "agent_triggered" not in st.session_state:
    st.session_state.agent_triggered = False

# Function to handle input via OpenAI
def handle_input(user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Infer yes/no if the agent was triggered
    if st.session_state.agent_triggered:
        if "yes" in user_input.lower():
            response = "Sure! Here's a summary of all 10 papers:"
            summaries = "\n\n".join(st.session_state.latest_df["Summary"].tolist())
            full_response = f"{response}\n\n{summaries}"
        elif "no" in user_input.lower():
            full_response = "Alright, feel free to ask me if you change your mind!"
        else:
            full_response = "I'm not sure I understood. Would you like a summary of all papers or details about a specific one?"
        st.session_state.agent_triggered = False
    else:
        # Regular OpenAI call
        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )
            full_response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Sidebar button to load top 10 papers
with st.sidebar:
    if st.button("Click me :)"):
        df = retrieve_most_relevant_docs_for_streamlit()
        st.session_state.latest_df = df
        st.dataframe(df, use_container_width=True)

        agent_msg = (
            "According to my database, these are the latest 10 scientific papers most relevant to longevity and youth extension. "
            "Would you like details of any or a summary of all?"
        )
        with st.chat_message("assistant"):
            st.markdown(agent_msg)
        st.session_state.messages.append({"role": "assistant", "content": agent_msg})
        st.session_state.agent_triggered = True

# Chat input
if prompt := st.chat_input("What would you like to know?"):
    handle_input(prompt)
