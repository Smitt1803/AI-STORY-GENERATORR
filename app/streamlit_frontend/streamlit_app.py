import streamlit as st
import requests
import json
import time
from datetime import datetime
import pytz

# Base URL for the API
API_BASE_URL = "http://127.0.0.1:8000"  # Change this to your actual API URL

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'access_token' not in st.session_state:
    st.session_state.access_token = None
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'name' not in st.session_state:
    st.session_state.name = None
if 'story_history' not in st.session_state:
    st.session_state.story_history = []
if 'current_view' not in st.session_state:
    st.session_state.current_view = "login"
if 'otp_sent' not in st.session_state:
    st.session_state.otp_sent = False
if 'show_register' not in st.session_state:
    st.session_state.show_register = False

# App title and configuration
st.set_page_config(
    page_title="AI Story Generator",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 42px;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 30px;
    }
    .sub-header {
        font-size: 24px;
        font-weight: bold;
        color: #1E3A8A;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .story-title {
        font-size: 28px;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 15px;
    }
    .story-metadata {
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 15px;
    }
    .story-summary {
        font-size: 16px;
        font-style: italic;
        color: #4B5563;
        padding: 10px;
        border-left: 3px solid #1E3A8A;
        background-color: #F3F4F6;
        margin-bottom: 20px;
    }
    .story-content {
        font-size: 18px;
        line-height: 1.6;
        text-align: justify;
    }
    .theme-tag {
        display: inline-block;
        background-color: #DBEAFE;
        color: #1E40AF;
        padding: 5px 10px;
        margin-right: 10px;
        margin-bottom: 10px;
        border-radius: 15px;
        font-size: 14px;
    }
    .entity-tag {
        display: inline-block;
        background-color: #E0F2FE;
        color: #0369A1;
        padding: 5px 10px;
        margin-right: 10px;
        margin-bottom: 10px;
        border-radius: 15px;
        font-size: 14px;
    }
    .sentiment-positive {
        color: #059669;
        font-weight: bold;
    }
    .sentiment-negative {
        color: #DC2626;
        font-weight: bold;
    }
    .sentiment-neutral {
        color: #6B7280;
        font-weight: bold;
    }
    # .login-container {
    #     max-width: 500px;
    #     margin: 0 auto;
    #     padding: 20px;
    #     background-color: #F9FAFB;
    #     border-radius: 10px;
    #     box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    # }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
    }
    .spinner-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 50px 0;
    }
    .auth-link {
        color: #1E3A8A;
        text-align: center;
        cursor: pointer;
        text-decoration: underline;
        font-size: 14px;
    }
    .auth-link:hover {
        color: #2563EB;
    }
    .centered-text {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Function to register a new user
def register_user(name, email, password):
    try:
        response = requests.post(
            f"{API_BASE_URL}/register/",
            json={"name": name, "email": email, "password": password}
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Function to login a user
def login_user(email, password):
    try:
        response = requests.post(
            f"{API_BASE_URL}/login/",
            json={"email": email, "password": password}
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Function to verify OTP
def verify_otp(email, otp):
    try:
        response = requests.post(
            f"{API_BASE_URL}/verify-otp/",
            json={"email": email, "otp": otp}
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Function to generate a story
def generate_story(prompt, genre, tone, style, story_length, include_twist, 
                   protagonist_description=None, setting=None, model="default"):
    try:
        headers = {}
        if st.session_state.access_token:
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        
        response = requests.post(
            f"{API_BASE_URL}/generate/",
            json={
                "prompt": prompt,
                "genre": genre,
                "tone": tone,
                "style": style,
                "story_length": story_length,
                "include_twist": include_twist,
                "protagonist_description": protagonist_description,
                "setting": setting,
                "model": model
            },
            headers=headers
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Function to generate a story asynchronously
def generate_story_async(prompt, genre, tone, style, story_length, include_twist, 
                         protagonist_description=None, setting=None, model="default"):
    try:
        headers = {}
        if st.session_state.access_token:
            headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        
        response = requests.post(
            f"{API_BASE_URL}/generate/async/",
            json={
                "prompt": prompt,
                "genre": genre,
                "tone": tone,
                "style": style,
                "story_length": story_length,
                "include_twist": include_twist,
                "protagonist_description": protagonist_description,
                "setting": setting,
                "model": model
            },
            headers=headers
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Function to check the status of an asynchronous job
def check_job_status(job_id):
    try:
        response = requests.get(f"{API_BASE_URL}/job/{job_id}")
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

# Function to get available models
def get_available_models():
    try:
        response = requests.get(f"{API_BASE_URL}/models")
        if response.status_code == 200:
            return response.json()["models"]
        return ["default"]
    except Exception as e:
        return ["default"]

# Function to check API health
def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            return response.json(), True
        return {"status": "API unavailable"}, False
    except Exception as e:
        return {"error": str(e)}, False

# Function to toggle between login and register views
def toggle_auth_view():
    st.session_state.show_register = not st.session_state.show_register

# Function to display the login page
def show_login_page():
    st.markdown('<div class="main-header">Welcome to AI Story Generator</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        if not st.session_state.show_register:
            # Login Form
            st.markdown('<div class="sub-header">Login</div>', unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Login")
                
                if login_button:
                    if not email or not password:
                        st.error("Please provide both email and password")
                    else:
                        result, status_code = login_user(email, password)
                        if status_code == 200:
                            st.session_state.otp_sent = True
                            st.session_state.user_email = email
                            st.success("OTP sent to your email. Please verify.")
                            st.rerun()
                        else:
                            st.error(result.get("detail", "Login failed"))
            
            # Link to registration form
            st.markdown('<div class="centered-text">', unsafe_allow_html=True)
            st.markdown('<p>New user? <a class="auth-link" href="#" onClick="document.dispatchEvent(new Event(\'registerClick\'));">Register here</a></p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # JavaScript to handle the click event
            st.markdown("""
                <script>
                    document.addEventListener('registerClick', function() {
                        const elements = parent.document.querySelectorAll('button[kind=secondary]');
                        for (const element of elements) {
                            if (element.innerText === 'Switch to Register') {
                                element.click();
                            }
                        }
                    });
                </script>
            """, unsafe_allow_html=True)
            
            # Hidden button that will be clicked by JavaScript
            if st.button("Switch to Register", key="switch_to_register", type="secondary"):
                toggle_auth_view()
        else:
            # Registration Form
            st.markdown('<div class="sub-header">Register</div>', unsafe_allow_html=True)
            with st.form("register_form"):
                name = st.text_input("Name")
                reg_email = st.text_input("Email", key="reg_email")
                reg_password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password")
                register_button = st.form_submit_button("Register")
                
                if register_button:
                    if not name or not reg_email or not reg_password:
                        st.error("Please fill all required fields")
                    elif reg_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        result, status_code = register_user(name, reg_email, reg_password)
                        if status_code == 200:
                            st.success("Registration successful! Please login.")
                            # Automatically switch to login view
                            st.session_state.show_register = False
                            st.rerun()
                        else:
                            st.error(result.get("detail", "Registration failed"))
            
            # Link back to login form
            st.markdown('<div class="centered-text">', unsafe_allow_html=True)
            st.markdown('<p>Already have an account? <a class="auth-link" href="#" onClick="document.dispatchEvent(new Event(\'loginClick\'));">Login here</a></p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # JavaScript to handle the click event
            st.markdown("""
                <script>
                    document.addEventListener('loginClick', function() {
                        const elements = parent.document.querySelectorAll('button[kind=secondary]');
                        for (const element of elements) {
                            if (element.innerText === 'Switch to Login') {
                                element.click();
                            }
                        }
                    });
                </script>
            """, unsafe_allow_html=True)
            
            # Hidden button that will be clicked by JavaScript
            if st.button("Switch to Login", key="switch_to_login", type="secondary"):
                toggle_auth_view()
                
        st.markdown('</div>', unsafe_allow_html=True)

# Function to display the OTP verification page
def show_otp_verification():
    st.markdown('<div class="main-header">OTP Verification</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # st.markdown('<div class="login-container">', unsafe_allow_html=True)
        st.markdown(f"<p>An OTP has been sent to {st.session_state.user_email}</p>", unsafe_allow_html=True)
        
        with st.form("otp_form"):
            otp = st.text_input("Enter OTP")
            col1, col2 = st.columns(2)
            
            with col1:
                verify_button = st.form_submit_button("Verify OTP")
            
            with col2:
                if st.form_submit_button("Back to Login"):
                    st.session_state.otp_sent = False
                    st.rerun()
            
            if verify_button:
                if not otp:
                    st.error("Please enter the OTP")
                else:
                    result, status_code = verify_otp(st.session_state.user_email, otp)
                    if status_code == 200:
                        st.session_state.logged_in = True
                        st.session_state.access_token = result.get("access_token")
                        st.session_state.name = result.get("name", "User")
                        st.session_state.current_view = "story_generator"
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid OTP. Please try again.")
        
        st.markdown('</div>', unsafe_allow_html=True)

# Function to display the story generator page
def show_story_generator():
    st.markdown('<div class="main-header">AI Story Generator</div>', unsafe_allow_html=True)
    
    # Get available models
    available_models = get_available_models()
    
    with st.form("story_form"):
        st.markdown('<div class="sub-header">Story Details</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            prompt = st.text_area("Story Prompt", height=150, 
                                placeholder="Describe your story idea here...")
            
            genre = st.selectbox(
                "Genre",
                ["Fantasy", "Science Fiction", "Mystery", "Romance", "Horror", 
                 "Adventure", "Historical Fiction", "Thriller", "Comedy", "Drama"]
            )
            
            tone = st.selectbox(
                "Tone",
                ["Humorous", "Dark", "Inspirational", "Melancholic", "Suspenseful",
                 "Romantic", "Philosophical", "Whimsical", "Serious", "Nostalgic"]
            )
            
            style = st.selectbox(
                "Writing Style",
                ["No preference", "Minimalist", "Descriptive", "Stream of consciousness", 
                 "Formal", "Conversational", "Poetic", "Academic"]
            )
        
        with col2:
            story_length = st.select_slider(
                "Story Length",
                options=["Very Short", "Short", "Medium", "Long", "Very Long"],
                value="Medium"
            )
            
            include_twist = st.checkbox("Include plot twist")
            
            protagonist = st.text_input(
                "Protagonist Description (Optional)",
                placeholder="Age, personality traits, background..."
            )
            
            setting = st.text_input(
                "Setting (Optional)",
                placeholder="Time period, location, environment..."
            )
            
            model = st.selectbox("Select Model", available_models)
        
        generate_button = st.form_submit_button("Generate Story")
        
        if generate_button:
            if not prompt:
                st.error("Please provide a story prompt")
            elif len(prompt) < 10:
                st.error("Please provide a more detailed prompt")
            else:
                with st.spinner("Generating your story... This may take a while depending on the story length."):
                    if story_length in ["Long", "Very Long"]:
                        # Use async generation for longer stories
                        result, status_code = generate_story_async(
                            prompt, genre, tone, style, story_length, include_twist,
                            protagonist, setting, model
                        )
                        
                        if status_code == 200 and "request_id" in result:
                            job_id = result["request_id"]
                            
                            # Poll for job completion
                            progress_bar = st.progress(0)
                            status_text = st.empty()
                            
                            complete = False
                            start_time = time.time()
                            
                            while not complete and time.time() - start_time < 300:  # 5-minute timeout
                                job_result, job_status_code = check_job_status(job_id)
                                
                                if job_status_code == 200:
                                    status = job_result.get("status")
                                    
                                    if status == "completed":
                                        complete = True
                                        # Add to story history
                                        story_data = {
                                            "title": job_result.get("title", "Untitled Story"),
                                            "generated_text": job_result.get("generated_text", ""),
                                            "summary": job_result.get("summary", ""),
                                            "entities": job_result.get("entities", []),
                                            "created_at": datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
                                            "genre": genre,
                                            "tone": tone,
                                            "prompt": prompt
                                        }
                                        st.session_state.story_history.insert(0, story_data)
                                        st.session_state.current_view = "view_story"
                                        st.session_state.current_story_index = 0
                                        st.rerun()
                                    elif status == "failed":
                                        st.error(f"Story generation failed: {job_result.get('error', 'Unknown error')}")
                                        complete = True
                                    else:
                                        # Update progress
                                        progress = 0.5  # We don't know actual progress, so use animation
                                        progress_bar.progress(progress)
                                        status_text.text(f"Status: {status}. Please wait...")
                                        time.sleep(2)  # Poll every 2 seconds
                                else:
                                    st.error("Error checking job status")
                                    break
                            
                            if not complete:
                                st.error("Timeout: Story generation is taking longer than expected. Check 'My Stories' later.")
                    else:
                        # Use sync generation for shorter stories
                        result, status_code = generate_story(
                            prompt, genre, tone, style, story_length, include_twist,
                            protagonist, setting, model
                        )
                        
                        if status_code == 200:
                            # Add to story history
                            story_data = {
                                "title": result.get("title", "Untitled Story"),
                                "generated_text": result.get("generated_text", ""),
                                "summary": result.get("summary", ""),
                                "entities": result.get("entities", []),
                                "themes": result.get("themes", []),
                                "sentiment": result.get("sentiment", {}),
                                "word_count": result.get("word_count", 0),
                                "created_at": datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S"),
                                "genre": genre,
                                "tone": tone,
                                "prompt": prompt
                            }
                            st.session_state.story_history.insert(0, story_data)
                            st.session_state.current_view = "view_story"
                            st.session_state.current_story_index = 0
                            st.rerun()
                        else:
                            st.error(result.get("detail", "Story generation failed"))

# Function to display a single story
def show_story_view():
    if st.session_state.story_history and len(st.session_state.story_history) > st.session_state.current_story_index:
        story = st.session_state.story_history[st.session_state.current_story_index]
        
        # Title and metadata
        st.markdown(f'<div class="story-title">{story["title"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="story-metadata">Genre: {story["genre"]} | Tone: {story["tone"]} | Created: {story["created_at"]}</div>', 
                    unsafe_allow_html=True)
        
        # Story summary
        st.markdown(f'<div class="story-summary">{story["summary"]}</div>', unsafe_allow_html=True)
        
        # Story entities & themes
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="sub-header">Characters & Places</div>', unsafe_allow_html=True)
            entities_html = ""
            for entity in story.get("entities", []):
                entities_html += f'<span class="entity-tag">{entity}</span>'
            st.markdown(f'<div>{entities_html}</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="sub-header">Themes</div>', unsafe_allow_html=True)
            themes_html = ""
            for theme in story.get("themes", []):
                themes_html += f'<span class="theme-tag">{theme}</span>'
            st.markdown(f'<div>{themes_html}</div>', unsafe_allow_html=True)
        
        # Sentiment analysis
        if "sentiment" in story and story["sentiment"]:
            sentiment = story["sentiment"]
            sentiment_class = "sentiment-neutral"
            if sentiment.get("sentiment") == "positive":
                sentiment_class = "sentiment-positive"
            elif sentiment.get("sentiment") == "negative":
                sentiment_class = "sentiment-negative"
            
            st.markdown(f'<div class="sub-header">Emotional Tone</div>', unsafe_allow_html=True)
            st.markdown(f'<p>This story has a <span class="{sentiment_class}">{sentiment.get("sentiment", "neutral")}</span> emotional tone '
                        f'(confidence: {round(sentiment.get("confidence", 0) * 100)}%)</p>', unsafe_allow_html=True)
        
        # Word count
        if "word_count" in story:
            st.markdown(f'<p>Word Count: {story["word_count"]}</p>', unsafe_allow_html=True)
        
        # Full story content
        st.markdown('<div class="sub-header">Full Story</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="story-content">{story["generated_text"]}</div>', unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("← Previous Story", disabled=st.session_state.current_story_index >= len(st.session_state.story_history) - 1):
                st.session_state.current_story_index += 1
                st.rerun()
        
        with col2:
            if st.button("Back to Generator"):
                st.session_state.current_view = "story_generator"
                st.rerun()
        
        with col3:
            if st.button("Next Story →", disabled=st.session_state.current_story_index <= 0):
                st.session_state.current_story_index -= 1
                st.rerun()
    else:
        st.error("No story found")
        if st.button("Back to Generator"):
            st.session_state.current_view = "story_generator"
            st.rerun()

# Function to display the story history page
def show_story_history():
    st.markdown('<div class="main-header">My Stories</div>', unsafe_allow_html=True)
    
    if not st.session_state.story_history:
        st.info("You haven't generated any stories yet.")
        if st.button("Create Your First Story"):
            st.session_state.current_view = "story_generator"
            st.rerun()
    else:
        for i, story in enumerate(st.session_state.story_history):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f'<div class="story-title">{story["title"]}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="story-metadata">Genre: {story["genre"]} | Created: {story["created_at"]}</div>', 
                                unsafe_allow_html=True)
                    st.markdown(f'<div class="story-summary">{story["summary"]}</div>', unsafe_allow_html=True)
                
                with col2:
                    if st.button("Read Story", key=f"read_{i}"):
                        st.session_state.current_story_index = i
                        st.session_state.current_view = "view_story"
                        st.rerun()
                
                st.markdown("---")

# Sidebar navigation
def sidebar_navigation():
    st.sidebar.markdown("# AI Story Generator")
    
    # Check and display API status
    health_info, is_healthy = check_api_health()
    status_color = "green" if is_healthy else "red"
    st.sidebar.markdown(f"API Status: <span style='color:{status_color};'>●</span> {'Online' if is_healthy else 'Offline'}", 
                        unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.sidebar.markdown(f"### Welcome, {st.session_state.name if st.session_state.name else 'User'}")
        
        if st.sidebar.button("Create Story"):
            st.session_state.current_view = "story_generator"
            st.rerun()
        
        if st.sidebar.button("My Stories"):
            st.session_state.current_view = "story_history"
            st.rerun()
        
        if st.sidebar.button("Logout"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.session_state.logged_in = False
            st.session_state.current_view = "login"
            st.session_state.otp_sent = False
            st.session_state.show_register = False
            st.rerun()
    else:
        st.sidebar.markdown("### Please login to continue")
        
        if st.session_state.otp_sent and st.sidebar.button("Back to Login"):
            st.session_state.otp_sent = False
            st.rerun()
    
    # App information
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "This application uses advanced AI to generate creative stories based on your ideas. "
        "You can specify the genre, tone, writing style, and other parameters to customize your story."
    )
    
    # Version information
    st.sidebar.markdown("---")
    st.sidebar.markdown("v2.0.0")
    st.sidebar.markdown("[Report an issue](mailto:support@aistorygenerator.com)")

# Main function to control the app flow
def main():
    sidebar_navigation()
    
    if not st.session_state.logged_in:
        if st.session_state.otp_sent:
            show_otp_verification()
        else:
            show_login_page()
    else:
        if st.session_state.current_view == "story_generator":
            show_story_generator()
        elif st.session_state.current_view == "view_story":
            show_story_view()
        elif st.session_state.current_view == "story_history":
            show_story_history()
        else:
            show_story_generator()

if __name__ == "__main__":
    main()