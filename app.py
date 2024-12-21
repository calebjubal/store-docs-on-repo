import streamlit as st

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "login"  # Start with the login page
if "github_token" not in st.session_state:
    st.session_state.github_token = None
if "github_user" not in st.session_state:
    st.session_state.github_user = None

# Page Navigation
if st.session_state.page == "login":
    from login_page import login_page
    login_page()
elif st.session_state.page == "app":
    from app_page import app_page
    app_page()
