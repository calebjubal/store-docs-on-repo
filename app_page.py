import streamlit as st
import requests
import os
from urllib.parse import quote

# Define GitHub OAuth credentials
CLIENT_ID = "YOUR_GITHUB_CLIENT_ID"
CLIENT_SECRET = "YOUR_GITHUB_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8501/callback"  # or your deployed URL
OAUTH_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"

# Session state initialization
if "github_token" not in st.session_state:
    st.session_state.github_token = None
if "github_user" not in st.session_state:
    st.session_state.github_user = None
if "github_avatar" not in st.session_state:
    st.session_state.github_avatar = None
if "repo_name" not in st.session_state:
    st.session_state.repo_name = None

# Step 1: Login Page
if not st.session_state.github_token:
    st.title("Login with GitHub")
    st.markdown("Click the GitHub icon below to log in.")

    # GitHub login URL with OAuth
    login_url = f"{OAUTH_URL}?client_id={CLIENT_ID}&redirect_uri={quote(REDIRECT_URI)}&scope=repo"
    st.markdown(f'<a href="{login_url}" target="_blank"><img src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" width="100" alt="GitHub Login"></a>', unsafe_allow_html=True)
else:
    # Step 2: Use GitHub Token to fetch user data and repositories
    headers = {
        "Authorization": f"Bearer {st.session_state.github_token}",
        "Accept": "application/json",
    }
    user_data = requests.get("https://api.github.com/user", headers=headers).json()
    st.session_state.github_user = user_data["login"]
    st.session_state.github_avatar = user_data["avatar_url"]

    st.title(f"Hello, {st.session_state.github_user}!")
    st.image(st.session_state.github_avatar, width=50)

    repo_name = st.text_input("Enter the repository name (e.g., username/repo):", value=st.session_state.repo_name)
    st.session_state.repo_name = repo_name

    if repo_name:
        # Display file uploader for files
        file_type = st.selectbox(
            "Select the type of file to upload:",
            ["Video", "PDF", "Image", "Document (Word, PPTX)"]
        )
        uploaded_file = st.file_uploader(f"Upload your {file_type}:", type=['mp4', 'pdf', 'png', 'jpg', 'jpeg', 'docx', 'pptx'])

        if uploaded_file:
            # GitHub repository connection
            repo_url = f"https://api.github.com/repos/{repo_name}/contents"
            file_content = uploaded_file.getvalue()
            file_name = uploaded_file.name

            # Upload to GitHub
            if st.button("Upload to GitHub"):
                try:
                    # Create file in the GitHub repository
                    response = requests.put(
                        repo_url + "/" + file_name,
                        headers=headers,
                        json={
                            "message": f"Upload {file_type}: {file_name}",
                            "content": file_content.decode('utf-8').encode("utf-8").encode('base64')
                        }
                    )
                    response.raise_for_status()
                    st.success(f"File '{file_name}' uploaded successfully to {repo_name}!")
                except Exception as e:
                    st.error(f"Error: {e}")
