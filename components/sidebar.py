import streamlit as st

def render_sidebar():
    st.sidebar.title("🗂️ Database selection")

    selected_db = st.sidebar.selectbox(  # ⬅️ Use selectbox for single select
        "Select Database:",
        ["Sample", "Inventory"]
    )

    st.sidebar.markdown("### 💬 Sample Questions")
    st.sidebar.markdown("""
    - Total number of customers?
    - Top 3 customers based on number of orders placed.
    """)

    return selected_db
