import streamlit as st
import numpy as np

st.title("Neuefische School and Pool for digital talent")

with st.chat_message("assistant"):
    st.write("Hello")
    st.bar_chart(np.random.randn(30, 3))
