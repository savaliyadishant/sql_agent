import streamlit as st

def render_chat_input():
    with st.form(key="chat_form"):
        user_query = st.text_input("Enter your natural language query:", "")
        submitted = st.form_submit_button("Send")
    return user_query, submitted
