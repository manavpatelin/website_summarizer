# app.py
import streamlit as st
from summary import summarize  # import the function from the module

st.title("Website Summarizer")
url = st.text_input("Enter URL")

if url:
    st.write("Summarizing...")
    summary = summarize(url)
    st.markdown(summary)

