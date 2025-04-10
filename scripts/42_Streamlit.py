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

    # Generate response from Llama 2 model
    response = replicate_client.run(
        "meta/llama-2-7b-chat",
        input={"prompt": user_input}
    )
    # Concatenate the list of strings into a single string
    full_response = "".join(response)

    # Append assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Sidebar for the button
with st.sidebar:
    if st.button("Click me :)"):
        simulated_input = "What time is it in Istanbul?"
        handle_input(simulated_input)

# Custom CSS to control chat interface layout
st.markdown("""
    <style>
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 80vh;
        }
        .chat-messages {
            flex-grow: 1;
            overflow-y: auto;
            padding-bottom: 10px;
        }
        .chat-input {
            position: sticky;
            bottom: 0;
            background: white;
            padding-top: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

# Main content area for chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Display chat messages from history on app rerun
st.markdown('<div class="chat-messages">', unsafe_allow_html=True)
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
st.markdown('</div>', unsafe_allow_html=True)

# Accept user input from chat input
st.markdown('<div class="chat-input">', unsafe_allow_html=True)
if prompt := st.chat_input("What is up?"):
    handle_input(prompt)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
