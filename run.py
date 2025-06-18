# import sqlite3

# conn = sqlite3.connect("data/sample_db2.sqlite")
# cursor = conn.cursor()

# # List all tables
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# tables = cursor.fetchall()
# print("Tables:", tables)

# # Show structure of each table
# for table_name, in tables:
#     print(f"\n🔍 Table: {table_name}")
#     cursor.execute(f"PRAGMA table_info({table_name});")
#     for col in cursor.fetchall():
#         print(col)

# conn.close()

# hash_passwords.py

# app.py

import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Must be the first Streamlit command
st.set_page_config(page_title="SQL Agent", layout="wide")

# Load config.yaml
with open('config/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    print(config)

# Create authenticator object
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Login widget
name, authentication_status, username = authenticator.login("Login", "main")

# Show different views based on auth state
if authentication_status:
    st.sidebar.success(f"Logged in as {name}")
    st.title("Welcome to the SQL Agent Dashboard")
    st.write(f"Hello **{name}** 👋 You are logged in as `{username}`")

    # Add your main app components here
    st.info("Here is where your SQL Agent UI will go.")

    # Logout button
    authenticator.logout("Logout", "sidebar")

elif authentication_status is False:
    st.error("❌ Incorrect username or password")

elif authentication_status is None:
    st.warning("Please enter your username and password")

