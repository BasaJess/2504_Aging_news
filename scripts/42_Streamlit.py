import streamlit as st
import replicate

# Set Replicate API token
replicate_client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle user input and generate response
def handle_input(user_input):
    # Append user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate response from Llama 2 model
    with st.chat_message("assistant"):
        response = replicate_client.run(
            "meta/llama-2-7b-chat",
            input={"prompt": user_input}
        )
        # Concatenate the list of strings into a single string
        full_response = "".join(response)
        # Display the concatenated response
        st.markdown(full_response)

    # Append assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar for the button
with st.sidebar:
    if st.button("Click me :)"):
        simulated_input = "What time is it in Istanbul?"
        handle_input(simulated_input)

# Main content area with columns
col1, col2 = st.columns([1, 3])  # Adjust the ratio as needed

with col2:
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input from chat input
    if prompt := st.chat_input("What is up?"):
        handle_input(prompt)
