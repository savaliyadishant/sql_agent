import streamlit as st
import yaml
import json
import pandas as pd
import time

from components.sidebar import render_sidebar
from components.chat_input import render_chat_input
from components.config_ui import render_config_screen
from core.prompt_builder import build_prompt
from core.llm_generator import generate_sql, generate_natural_response
from core.query_executor import execute_query
from core.sql_validator import validate_sql

# Set page configuration
st.set_page_config(page_title="Gen AI SQL Agent", layout="wide")

# Simple login
def login_form():
    st.sidebar.title("🔐 Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.name = "Admin"
            st.experimental_rerun()
        else:
            st.sidebar.error("❌ Invalid credentials")

# Login logic
if "logged_in" not in st.session_state:
    login_form()
elif st.session_state.logged_in:
    st.sidebar.success(f"✅ Logged in as: {st.session_state.name} ({st.session_state.username})")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.clear())

    # Define role
    role = "admin"

    # Load role permissions
    with open("config/roles.json") as f:
        ROLE_PERMISSIONS = json.load(f)

    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    screen = st.sidebar.radio("Go to:", ["GenAI Assistant", "Configuration"])

    if screen == "GenAI Assistant":
        st.markdown("## 🤖 Gen AI Assistant")
        user_query, submitted = render_chat_input()
        selected_db = render_sidebar()

        if user_query and submitted:
            prompt = build_prompt(user_query, role, selected_db)
            st.code(prompt, language="sql")

            sql_query = generate_sql(prompt, role)
            st.code(sql_query, language="sql")

            allow_dml = ROLE_PERMISSIONS[role].get("allow_dml", False)
            validation = validate_sql(sql_query, allow_dml=allow_dml)

            if not validation["valid"]:
                st.error(f"❌ Invalid SQL Query: {validation['error']}")
                st.stop()

            result = execute_query(sql_query, selected_db, user_query, role)

            if result["error"]:
                st.error(f"❌ Query Execution Failed: {result['error']}")
            else:
                rows = result.get("rows")
                columns = result.get("columns")

                if rows is not None and columns is not None:
                    df_result = pd.DataFrame(rows, columns=columns)
                    if not df_result.empty:
                        st.subheader("🗣️ Natural Language Answer (Word-by-word)")
                        natural_response = generate_natural_response(user_query, df_result)

                        placeholder = st.empty()
                        typed_text = ""
                        for word in natural_response.split():
                            typed_text += word + " "
                            placeholder.markdown(typed_text + "▌")
                            time.sleep(0.1)
                        placeholder.markdown(typed_text.strip())
                    else:
                        st.warning("⚠️ Query executed successfully but returned no data.")
                else:
                    st.success("✅ Query executed successfully. (No data returned)")

    elif screen == "Configuration":
        render_config_screen()

else:
    st.warning("🔐 Please login to access the application.")
