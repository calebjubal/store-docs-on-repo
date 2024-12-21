import streamlit as st
from github import Github

def login_page():
    st.title("GitHub Authentication")
    st.write("Log in with your GitHub Personal Access Token to access the app.")

    github_token_input = st.text_input(
        "Enter your GitHub Personal Access Token:",
        type="password",
        help="You can generate a token from your GitHub Developer settings."
    )

    if st.button("Login"):
        try:
            # Validate token
            g = Github(github_token_input)
            user = g.get_user()
            st.session_state.github_token = github_token_input
            st.session_state.github_user = user.login
            st.session_state.page = "app"  # Navigate to the main app page
            st.success(f"Logged in as {user.login}. Redirecting to the app...")
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Authentication failed: {e}")
