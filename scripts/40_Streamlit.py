import streamlit as st
import numpy as np

st.title("Neuefische School and Pool for digital talent")

with st.chat_message("assistant"):
    st.write("Hello")

prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")