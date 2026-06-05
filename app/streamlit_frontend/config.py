import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Authentication settings
AUTH_TOKEN_EXPIRY_DAYS = 7

# Story generation settings
DEFAULT_GENRE = "Fantasy"
DEFAULT_TONE = "Inspirational"
DEFAULT_STYLE = "No preference"
DEFAULT_LENGTH = "Medium"
DEFAULT_MODEL = "default"

# Cache settings
CACHE_EXPIRY = 3600  # 1 hour in seconds

# Timeout settings
REQUEST_TIMEOUT = 60  # seconds
ASYNC_JOB_TIMEOUT = 300  # 5 minutes

# User preferences (to be stored in database later)
DEFAULT_USER_PREFERENCES = {
    "dark_mode": False,
    "preferred_genre": DEFAULT_GENRE,
    "preferred_tone": DEFAULT_TONE,
    "preferred_style": DEFAULT_STYLE,
    "preferred_length": DEFAULT_LENGTH,
    "preferred_model": DEFAULT_MODEL,
}

# App metadata
APP_VERSION = "2.0.0"
APP_NAME = "AI Story Generator"
CONTACT_EMAIL = "support@aistorygenerator.com"








# """
# This is an alternative implementation using Streamlit's multi-page app structure
# with pages directory for better organization.

# Project structure:
# /streamlit_app/
# ├── main.py              # Main file with authentication
# ├── utils/
# │   ├── __init__.py      # Empty file to make utils a package
# │   ├── api_client.py    # API client functions
# │   ├── ui_components.py # Reusable UI components
# │   └── session.py       # Session state management
# └── pages/               # Pages directory for multipage app
#     ├── 1_Create_Story.py
#     ├── 2_My_Stories.py
#     └── 3_Story_Analysis.py
# """

# # main.py
# import streamlit as st
# import requests
# import json
# from datetime import datetime

# # Set page configuration
# st.set_page_config(
#     page_title="AI Story Generator",
#     page_icon="📚",
#     layout="wide",
#     initial_sidebar_state="expanded",
# )

# # Import utility functions
# from utils.api_client import make_api_request
# from utils.ui_components import apply_custom_css, render_login_form, render_register_form, render_otp_form

# # Initialize session state
# if "auth_token" not in st.session_state:
#     st.session_state.auth_token = None
# if "is_authenticated" not in st.session_state:
#     st.session_state.is_authenticated = False
# if "user_email" not in st.session_state:
#     st.session_state.user_email = None
# if "user_name" not in st.session_state:
#     st.session_state.user_name = None
# if "stories" not in st.session_state:
#     st.session_state.stories = []
# if "current_story" not in st.session_state:
#     st.session_state.current_story = None
# if "waiting_for_otp" not in st.session_state:
#     st.session_state.waiting_for_otp = False

# # Apply custom CSS
# apply_custom_css()

# # Main app function
# def main():
#     # Check if user is authenticated
#     if not st.session_state.is_authenticated:
#         if st.session_state.waiting_for_otp:
#             render_otp_verification_page()
#         else:
#             render_login_page()
#     else:
#         render_authenticated_page()

# def render_login_page():
#     """Display login page"""
#     st.markdown("<h1 class='main-header'>AI Story Generator</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='sub-header'>Login to start creating amazing stories</p>", unsafe_allow_html=True)
    
#     col1, col2 = st.columns([1, 1])
    
#     with col1:
#         # Login form
#         render_login_form()
    
#     with col2:
#         # Register form
#         render_register_form()

# def render_otp_verification_page():
#     """Display OTP verification page"""
#     st.markdown("<h1 class='main-header'>Verify OTP</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='sub-header'>Enter the OTP sent to your email</p>", unsafe_allow_html=True)
    
#     col1, col2, col3 = st.columns([1, 2, 1])
    
#     with col2:
#         render_otp_form()

# def render_authenticated_page():
#     """Welcome page after authentication"""
#     st.markdown("<h1 class='main-header'>Welcome to AI Story Generator</h1>", unsafe_allow_html=True)
#     st.markdown("<p class='sub-header'>Select an option from the sidebar to get started</p>", unsafe_allow_html=True)
    
#     # User info in sidebar
#     with st.sidebar:
#         st.title("Story Generator")
#         st.markdown(f"**Logged in as:** {st.session_state.user_email}")
        
#         if st.button("Logout"):
#             # Clear session state
#             st.session_state.auth_token = None
#             st.session_state.is_authenticated = False
#             st.session_state.user_email = None 
#             st.session_state.user_name = None
#             st.session_state.stories = []
#             st.session_state.current_story = None
#             st.experimental_rerun()
    
#     # Welcome content
#     st.markdown("""
#     ## Getting Started
    
#     Use the sidebar navigation to:
    
#     1. **Create Story**: Generate new AI-powered stories with custom parameters
#     2. **My Stories**: Browse your previously generated stories
#     3. **Story Analysis**: Analyze your stories with AI-powered tools
    
#     ### Tips for Story Generation
    
#     - Provide a clear and specific story prompt
#     - Experiment with different genres and tones
#     - Try different AI models for varied results
#     - Customize your protagonist and setting for more detailed stories
    
#     ### Available Models
    
#     - **default**: Balanced performance
#     - **llama3-70b**: High-quality, detailed stories
#     - **llama3-8b**: Faster generation, simpler stories
#     - **qwen-qwq-32b**: Creative storytelling
#     - **creative**: Higher creativity, more variation
#     - **concise**: Shorter, more focused stories
#     """)

# if __name__ == "__main__":
#     main()