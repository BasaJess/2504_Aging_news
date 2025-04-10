import streamlit as st
import replicate

	

# Set Replicate API token
replicate_client = replicate.Client(api_token=st.secrets["REPLICATE_API_TOKEN"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from Llama 2 model
    with st.chat_message("assistant"):
        response = replicate_client.run(
            "meta/llama-2-7b-chat",
            input={"prompt": prompt}
        )
        # Concatenate the list of strings into a single string
        full_response = "".join(response)
        # Display the concatenated response
        st.markdown(full_response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})

    if st.button("Click me"", key="button1", help="This is a button")
    replicate_client.run(
            "meta/llama-2-7b-chat",
            input={"prompt": "Hello, world!"}
