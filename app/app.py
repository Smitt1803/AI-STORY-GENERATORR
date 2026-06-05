# import streamlit as st
# import requests
# from gtts import gTTS
# import base64
# from io import BytesIO
# import json
# import time
# import random
# import os
# import fpdf  # Added for PDF export

# # API endpoint
# API_URL = "http://127.0.0.1:8000/generate/"

# # App settings
# # def load_config():
# #     try:
# #         with open('config.json', 'r') as f:
# #             return json.load(f)
# #     except:
# #         return {"theme": "dark", "recent_stories": [], "voice": "Default male", "speech_speed": 1.0}

# if 'favorite_stories' not in st.session_state:
#     st.session_state.favorite_stories = []


# def load_config():
#     try:
#         with open('config.json', 'r') as f:
#             config = json.load(f)
#             # If favorites exist in config, load them
#             if 'favorite_stories' in config:
#                 st.session_state.favorite_stories = config['favorite_stories']
#             return config
#     except:
#         return {"theme": "dark", "recent_stories": [], "voice": "Default male", "speech_speed": 1.0}


# def save_config(config):
#     # Ensure favorites are included in the config
#     if 'favorite_stories' not in config and hasattr(st.session_state, 'favorite_stories'):
#         config['favorite_stories'] = st.session_state.favorite_stories
    
#     with open('config.json', 'w') as f:
#         json.dump(config, f)

# # def save_config(config):
# #     with open('config.json', 'w') as f:
# #         json.dump(config, f)

# # Init session state and load config
# if 'config' not in st.session_state:
#     st.session_state.config = load_config()
# if 'story_history' not in st.session_state:
#     st.session_state.story_history = []
# if 'favorite_stories' not in st.session_state:
#     st.session_state.favorite_stories = []
# if 'random_prompt' not in st.session_state:
#     st.session_state.random_prompt = ""
# if 'user_prompt' not in st.session_state:
#     st.session_state.user_prompt = ""

# # Fetch available models from API (fallback to default if API unreachable)
# def fetch_models():
#     try:
#         response = requests.get("http://127.0.0.1:8000/models")
#         if response.status_code == 200:
#             return response.json()["models"]
#         else:
#             return ["default", "creative", "concise"]
#     except:
#         return ["default", "creative", "concise"]

# if 'models' not in st.session_state:
#     st.session_state.models = fetch_models()

# # App layout
# st.set_page_config(page_title="AI Story Generator", layout="wide")


# def apply_theme(theme):
#     if theme == "Dark":
#         st.markdown("""
#         <style>
#         .main {
#             background-color: #1E1E1E;
#             color: #FFFFFF;
#         }
#         .stButton button {
#             background-color: #4F4F4F;
#             color: white;
#         }
#         .stTextInput input, .stTextArea textarea {
#             background-color: #2D2D2D;
#             color: #FFFFFF;
#         }
#         .stSelectbox select {
#             background-color: #2D2D2D;
#             color: #FFFFFF;
#         }
#         div[data-testid="stSidebar"] {
#             background-color: #252525;
#             color: #FFFFFF;
#         }
#         /* Fix for story display area in dark mode */
#         .story-container {
#             font-family: Georgia, serif;
#             line-height: 1.6;
#             background-color: #2D2D2D !important; 
#             padding: 20px;
#             border-radius: 10px;
#             border-left: 5px solid #007bff;
#             color: #E0E0E0 !important;
#         }
#         /* Fix for tabs in dark mode */
#         .stTabs [data-baseweb="tab-list"] {
#             background-color: #1E1E1E;
#         }
#         .stTabs [data-baseweb="tab"] {
#             color: #FFFFFF;
#         }
#         /* Fix for cards in dark mode */
#         .story-card {
#             border: 1px solid #444;
#             border-radius: 5px;
#             padding: 10px;
#             margin-bottom: 15px;
#             background-color: #2D2D2D;
#             color: #E0E0E0;
#         }
#         .favorite-card {
#             border: 1px solid #444;
#             border-radius: 5px;
#             padding: 10px;
#             margin-bottom: 15px;
#             border-left: 5px solid #FF6B6B;
#             background-color: #2D2D2D;
#             color: #E0E0E0;
#         }
#         /* Fix for summary box in dark mode */
#         .summary-box {
#             background-color: #263238;
#             padding: 15px;
#             border-radius: 5px;
#             color: #E0E0E0;
#         }
#         </style>
#         """, unsafe_allow_html=True)
#     else:
#         # Light theme styling (default)
#         st.markdown("""
#         <style>
#         .story-container {  
#             font-family: Georgia, serif;
#             line-height: 1.6;
#             background-color: #f9f9f9;
#             padding: 20px;
#             border-radius: 10px;
#             border-left: 5px solid #007bff;
#         }
#         .story-card {
#             border: 1px solid #ddd;
#             border-radius: 5px;
#             padding: 10px;
#             margin-bottom: 15px;
#         }
#         .favorite-card {
#             border: 1px solid #ddd;
#             border-radius: 5px;
#             padding: 10px;
#             margin-bottom: 15px;
#             border-left: 5px solid #FF6B6B;
#         }
#         .summary-box {
#             background-color: #f0f7ff;
#             padding: 15px;
#             border-radius: 5px;
#         }
#         </style>
#         """, unsafe_allow_html=True)

# # Apply theme
# # def apply_theme(theme):
# #     if theme == "Dark":
# #         st.markdown("""
# #         <style>
# #         .main {
# #             background-color: #1E1E1E;
# #             color: #FFFFFF;
# #         }
# #         .stButton button {
# #             background-color: #4F4F4F;
# #             color: white;
# #         }
# #         .stTextInput input, .stTextArea textarea {
# #             background-color: #2D2D2D;
# #             color: #FFFFFF;
# #         }
# #         .stSelectbox select {
# #             background-color: #2D2D2D;
# #             color: #FFFFFF;
# #         }
# #         div[data-testid="stSidebar"] {
# #             background-color: #252525;
# #             color: #FFFFFF;
# #         }
# #         </style>
# #         """, unsafe_allow_html=True)

# # Custom PDF class to handle Unicode characters
# class UnicodePDF(fpdf.FPDF):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Add Unicode font support
#         self.add_font('DejaVu', '', 'DejaVuSansCondensed.ttf', uni=True)
#         self.add_font('DejaVu', 'B', 'DejaVuSansCondensed-Bold.ttf', uni=True)
    
#     # Override header/footer methods if needed
#     def header(self):
#         pass
    
#     def footer(self):
#         # Add page numbers at the bottom
#         self.set_y(-15)
#         self.set_font('DejaVu', '', 8)
#         self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# # Export to PDF function with simplified approach
# def export_to_pdf(title, story):
#     try:
#         # Create PDF with basic settings
#         pdf = fpdf.FPDF()
#         pdf.add_page()
        
#         # Set standard font (built into FPDF)
#         pdf.set_font("Arial", "B", 16)
        
#         # Clean title to ASCII-safe characters
#         clean_title = title.encode('ascii', 'ignore').decode('ascii') or "Generated Story"
        
#         # Title
#         pdf.cell(0, 10, clean_title, 0, 1, "C")
#         pdf.ln(10)
        
#         # Story content
#         pdf.set_font("Arial", "", 12)
        
#         # Handle story text - replace problematic characters
#         story_lines = story.split('\n')
#         for line in story_lines:
#             # Handle paragraph breaks
#             if line.strip() == '':
#                 pdf.ln(5)
#                 continue
                
#             # Clean line to ASCII-safe characters
#             clean_line = line.encode('ascii', 'replace').decode('ascii')
#             clean_line = clean_line.replace('?', '-')  # Replace replacement chars
            
#             # Process text in chunks to avoid overflow
#             pdf.multi_cell(0, 5, clean_line)
#             pdf.ln(2)
        
#         # Return PDF as bytes
#         return pdf.output(dest='S').encode('latin-1', 'replace')
        
#     except Exception as e:
#         st.error(f"PDF generation failed: {str(e)}")
#         return None
    
# with st.sidebar:
#     st.title("📚 Story Workshop")
    
#     # Theme toggle
#     theme = st.selectbox("🎨 Theme", ["Light", "Dark"], 
#                         index=0 if st.session_state.config.get("theme") == "light" else 1)
    
#     # Apply theme immediately
#     st.session_state.config["theme"] = theme.lower()
#     apply_theme(theme)
#     save_config(st.session_state.config)
    
#     # Navigation
#     tab_selection = st.radio("Navigation", ["Create Story", "My Stories", "Settings"])
    
#     # Sample prompts
#     if tab_selection == "Create Story":
#         st.subheader("✨ Sample Ideas")
#         sample_prompts = [
#             "A traveler discovers a hidden village where time flows backwards.",
#             "A detective who can speak to the dead solves their most challenging case.",
#             "Two rival chefs compete for a prestigious award, but must work together when disaster strikes.",
#             "A botanist discovers a plant with unexpected magical properties."
#         ]
        
#         # Fixed random prompt button
#         if st.button("Random Prompt", key="random_prompt_btn"):
#             random_prompt = random.choice(sample_prompts)
#             # Store in session state to be used in the main area
#             st.session_state.user_prompt = random_prompt
#             # Force rerun to update text area immediately
#             st.rerun()
    
#     # Story history
#     if tab_selection == "My Stories":
#         st.subheader("📜 Story History")
#         if not st.session_state.story_history:
#             st.info("Your created stories will appear here")
#         else:
#             for idx, story_data in enumerate(st.session_state.story_history):
#                 st.write(f"**{story_data['title']}**")
#                 if st.button(f"Load ↩️", key=f"load_{idx}"):
#                     st.session_state.load_story = story_data
#                     st.rerun()
                    
#     # Settings section
#     if tab_selection == "Settings":
#         st.subheader("⚙️ Settings")
#         st.write("Voice Settings:")
#         voice_options = ["Default Female", "Default Male", "British Accent", "Australian Accent"]
#         selected_voice = st.selectbox("TTS Voice", voice_options, 
#                                      index=voice_options.index(st.session_state.config.get("voice", "Default Male")))
        
#         speech_speed = st.slider("Speech Speed", 0.5, 1.5, 
#                                st.session_state.config.get("speech_speed", 1.0), 0.1)
        
#         auto_save = st.checkbox("Enable Auto-Save", 
#                               st.session_state.config.get("auto_save", True))
        
#         # Save settings to config
#         if selected_voice != st.session_state.config.get("voice") or \
#            speech_speed != st.session_state.config.get("speech_speed") or \
#            auto_save != st.session_state.config.get("auto_save"):
#             st.session_state.config["voice"] = selected_voice
#             st.session_state.config["speech_speed"] = speech_speed
#             st.session_state.config["auto_save"] = auto_save
#             save_config(st.session_state.config)
#             st.success("Settings saved!")
        
#         if st.button("Clear History"):
#             st.session_state.story_history = []
#             st.success("History cleared!")

# if st.sidebar.checkbox("Debug Mode", False):
#     st.sidebar.write("## Debug Information")
    
#     if 'favorite_stories' in st.session_state:
#         st.sidebar.write(f"Number of favorites: {len(st.session_state.favorite_stories)}")
        
#         if len(st.session_state.favorite_stories) > 0:
#             st.sidebar.write("Favorite Titles:")
#             for i, fav in enumerate(st.session_state.favorite_stories):
#                 st.sidebar.write(f"{i+1}. {fav.get('title', 'Untitled')}")
#     else:
#         st.sidebar.write("No favorites in session state")
        
#     if 'config' in st.session_state:
#         st.sidebar.write("Config contains:")
#         for key in st.session_state.config:
#             st.sidebar.write(f"- {key}")
#     else:
#         st.sidebar.write("No config in session state")

# # Main area
# if tab_selection == "Create Story" or tab_selection not in ["Create Story", "My Stories", "Settings"]:
#     st.title("📖 AI Story Generator")
    
#     col1, col2 = st.columns([2, 1])
    
#     with col1:
#         # Story parameters
#         st.subheader("Story Parameters")
        
#         # Core story parameters
#         col_genre, col_tone, col_style = st.columns(3)
#         with col_genre:
#             genre = st.selectbox("🎭 Genre", ["Fantasy", "Sci-Fi", "Mystery", "Romance", "Horror", "Adventure", "Drama", "Historical", "Comedy"])
#         with col_tone:
#             tone = st.selectbox("🎨 Tone", ["Serious", "Humorous", "Dark", "Uplifting", "Suspenseful", "Romantic", "Dramatic", "Melancholic"])
#         with col_style:
#             style = st.selectbox("🖋️ Style", ["No preference", "Classic", "Modern", "Poetic", "Minimalist", "Descriptive", "Dialogue-heavy", "First Person", "Third Person"])
        
#         # Model selection (fixed)
#         model = st.selectbox("🤖 LLM Model", options=st.session_state.models, index=0, 
#                            help="Select which AI model to use for story generation")
        
#         # Advanced options
#         with st.expander("Advanced Options"):
#             col_len, col_complexity = st.columns(2)
#             with col_len:
#                 story_length = st.select_slider("Story Length", ["Very Short", "Short", "Medium", "Long"], value="Medium")
#             with col_complexity:
#                 complexity = st.select_slider("Complexity", ["Simple", "Moderate", "Complex"], value="Moderate")
            
#             has_twist = st.checkbox("Include plot twist", value=False)
#             mature_content = st.checkbox("Allow mature themes", value=False)
    
#     with col2:
#         # Character settings
#         st.subheader("Character Settings")
#         protagonist_name = st.text_input("👤 Protagonist Name", "")
#         protagonist_desc = st.text_area("Character Description", height=100, placeholder="Describe your protagonist's personality, appearance, or background...")
        
#         st.subheader("Setting")
#         setting = st.text_input("🏙️ Story Setting / Era", placeholder="Medieval kingdom, futuristic city, etc.")
    
#     # Prompt area
#     st.subheader("Your Story Idea")
    
#     # Use stored prompt value from session state
#     user_prompt = st.text_area("📝 Describe your story idea:", value=st.session_state.user_prompt, height=150, 
#                              max_chars=2000, help="Enter your story concept. Be as detailed or vague as you like.")
#     st.caption(f"Character count: {len(user_prompt)}/2000")
    
#     # Store the current value back to session state
#     st.session_state.user_prompt = user_prompt
    
#     # Generate button with options
#     col_gen, col_options = st.columns([1, 2])
#     with col_gen:
#         generate_button = st.button("✨ Generate Story", type="primary", use_container_width=True)
#     with col_options:
#         save_to_history = st.checkbox("Save to my stories", value=True)
    
#     # Build the full prompt with enhancements
#     def build_custom_prompt():
#         base = user_prompt.strip()
#         extra = []

#         if protagonist_name:
#             extra.append(f"The protagonist's name is {protagonist_name}.")
#         if protagonist_desc:
#             extra.append(f"Character description: {protagonist_desc}.")
#         if setting:
#             extra.append(f"The story is set in {setting}.")
#         if story_length == "Very Short":
#             extra.append("Make this a very short story, around 300-500 words.")
#         elif story_length == "Short":
#             extra.append("Make this a short story, around 500-1000 words.")
#         elif story_length == "Medium":
#             extra.append("Make this a medium-length story, around 1000-2000 words.")
#         elif story_length == "Long":
#             extra.append("Make this a longer story, around 2000-3000 words.")
#         if complexity == "Simple":
#             extra.append("Keep the plot straightforward and easy to follow.")
#         elif complexity == "Complex":
#             extra.append("Include nuanced plot elements and deeper character development.")
#         if not mature_content:
#             extra.append("Keep the content appropriate for general audiences.")
            
#         return base + " " + " ".join(extra)

#     # Generate story
#     if generate_button and user_prompt:
#         with st.spinner("✍️ Crafting your masterpiece..."):
#             try:
#                 # Show animated progress bar
#                 progress_bar = st.progress(0)
#                 for i in range(100):
#                     time.sleep(0.01)  # Simulate processing time
#                     progress_bar.progress(i + 1)
                
#                 final_prompt = build_custom_prompt()

#                 # Make API request with all parameters
#                 response = requests.post(API_URL, json={
#                     "prompt": final_prompt,
#                     "genre": genre,
#                     "tone": tone,
#                     "style": style,
#                     "story_length": story_length,
#                     "include_twist": has_twist,
#                     "protagonist_description": protagonist_desc,
#                     "setting": setting,
#                     "model": model  # Send selected model to API
#                 })

#                 if response.status_code == 200:
#                     data = response.json()
#                     story = data["generated_text"]
#                     summary = data["summary"]
#                     entities = data.get("entities", [])
#                     title = data.get("title", "Generated Story")
#                     themes = data.get("themes", ["Identity", "Growth", "Conflict", "Resolution"])
                    
#                     # Save to history if option selected
#                     if save_to_history:
#                         story_data = {
#                             "title": title,
#                             "story": story,
#                             "summary": summary,
#                             "entities": entities,
#                             "parameters": {
#                                 "genre": genre,
#                                 "tone": tone,
#                                 "style": style,
#                                 "model": model
#                             },
#                             "prompt": user_prompt,
#                             "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
#                         }
#                         st.session_state.story_history.insert(0, story_data)
                    
#                     # Create tabs for story and metadata
#                     tabs = st.tabs(["📘 Story", "🧾 Summary", "🔍 Analysis", "🎧 Audio"])

#                     # Story Tab
#                     with tabs[0]:
#                         st.header(title)
                        
#                         # Story with proper formatting
#                         story_formatted = story.replace("\n\n", "<br><br>").replace("\n", "<br>")
#                         st.markdown(f"""
#                         <div class="story-container">
#                         {story_formatted}
#                         </div>
#                         """, unsafe_allow_html=True)
                        
#                         # Action buttons
#                         col1, col2, col3 = st.columns(3)
#                         with col1:
#                             st.download_button("💾 Download as TXT", story, file_name=f"{title}.txt")
#                         with col2:
#                             try:
#                                 pdf_data = export_to_pdf(title, story)
#                                 if pdf_data:
#                                     st.download_button(
#                                         "📄 Export as PDF",
#                                         data=pdf_data,
#                                         file_name=f"{title.replace(' ', '_')}.pdf",
#                                         mime="application/pdf"
#                                     )
#                                 else:
#                                     st.warning("Could not generate PDF")
#                             except Exception as e:
#                                 st.error(f"PDF generation failed: {str(e)}")

#                         with col3:
#                             # Completely rebuilt Add to Favorites function
#                             if st.button("❤️ Add to Favorites", key=f"fav_add_{title[:10]}"):
#                                 # Create a unique key based on title to prevent conflicts
#                                 new_favorite = {
#                                     "title": title,
#                                     "summary": summary,
#                                     "story": story,
#                                     "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
#                                 }
                                
#                                 # Check if already in favorites
#                                 already_in_favorites = False
#                                 for existing in st.session_state.favorite_stories:
#                                     if existing.get('title') == title:
#                                         already_in_favorites = True
#                                         break
                                        
#                                 if not already_in_favorites:
#                                     # Make a deep copy of the current favorites
#                                     current_favorites = st.session_state.favorite_stories.copy()
#                                     # Add new story
#                                     current_favorites.append(new_favorite)
#                                     # Update session state with the new list
#                                     st.session_state.favorite_stories = current_favorites
                                    
#                                     # Save state to config file to ensure persistence
#                                     if 'config' in st.session_state:
#                                         st.session_state.config['favorite_stories'] = st.session_state.favorite_stories
#                                         save_config(st.session_state.config)
                                    
#                                     st.success("✅ Added to favorites successfully!")
#                                     # Force refresh to see changes
#                                     st.rerun()
#                                 else:
#                                     st.info("This story is already in your favorites!")

#                     # Summary Tab
#                     with tabs[1]:
#                         st.subheader("Story Summary")
#                         st.markdown(f"""
#                         <div class="summary-box">
#                         {summary}
#                         </div>
#                         """, unsafe_allow_html=True)

#                     # Analysis Tab
#                     with tabs[2]:
#                         st.subheader("Story Analysis")
                        
#                         # Characters and places
#                         st.write("📌 Characters & Places:")
#                         if entities:
#                             st.write(", ".join(entities))
#                         else:
#                             st.info("No named entities found.")
                            
#                         # Theme analysis
#                         st.write("🎯 Themes:")
#                         if themes:
#                             st.write(", ".join(themes))
#                         else:
#                             st.info("No themes detected.")
                        
#                         # Word count analysis
#                         word_count = len(story.split())
#                         st.metric("Word Count", word_count)
                        
#                         # Reading time estimate
#                         reading_time = round(word_count / 200)  # Average reading speed
#                         st.metric("Estimated Reading Time", f"{reading_time} min")

#                     # Audio Tab
#                     with tabs[3]:
#                         st.subheader("Text-to-Speech")
                        
#                         # Apply voice settings from config
#                         voice_settings = st.session_state.config
#                         selected_voice = voice_settings.get("voice", "Default Male")
#                         speech_speed = voice_settings.get("speech_speed", 1.0)
                        
#                         st.write(f"Voice: {selected_voice}")
#                         st.write(f"Speed: {speech_speed}x")
                        
#                         # Map selected voice to language/accent parameters for gTTS
#                         lang = "en"
#                         tld = "com"  # Default US accent
                        
#                         if "British" in selected_voice:
#                             tld = "co.uk"
#                         elif "Australian" in selected_voice:
#                             tld = "com.au"
                        
#                         # Adjust speech speed
#                         slow_option = False
#                         if speech_speed < 0.8:
#                             slow_option = True
                        
#                         # TTS implementation with proper voice settings and error handling
#                         try:
#                             with st.spinner("Generating audio..."):
#                                 # Limit text length for performance
#                                 text_for_tts = story[:3000] if len(story) > 3000 else story
                                
#                                 # Clean the text for TTS to avoid encoding issues
#                                 clean_text = text_for_tts.encode('utf-8', 'ignore').decode('utf-8')
                                
#                                 # Create TTS object with selected parameters
#                                 tts = gTTS(text=clean_text, lang=lang, tld=tld, slow=slow_option)
#                                 tts_file = BytesIO()
#                                 tts.write_to_fp(tts_file)
#                                 tts_file.seek(0)
                                
#                                 st.audio(tts_file.read(), format="audio/mp3")
                                
#                                 if len(story) > 3000:
#                                     st.info("Note: Audio limited to the first part of the story for performance reasons.")
#                         except Exception as e:
#                             st.error(f"Could not generate audio: {str(e)}")
#                             st.info("Try a shorter text segment or check your internet connection.")
#                         else:
#                             # Download audio option
#                             tts_file.seek(0)  # Reset position to start of file
#                             audio_bytes = tts_file.getvalue()
#                             st.download_button(
#                                 label="Download Audio",
#                                 data=audio_bytes,
#                                 file_name=f"{title}.mp3",
#                                 mime="audio/mp3"
#                             )
#                 else:
#                     st.error(f"❌ Failed to generate story. Server returned status code {response.status_code}")
#                     if response.status_code == 422:
#                         st.error("The server couldn't process your request. Check that all required fields are filled correctly.")
#                     elif response.status_code == 429:
#                         st.error("Rate limit exceeded. Please wait a moment and try again.")
#                     else:
#                         st.error("Unknown error. Please check if the API server is running.")
#             except Exception as e:
#                 st.error(f"⚠️ Error: {e}")
#                 st.error("API connection error. Please make sure the backend server is running.")
#     elif generate_button and not user_prompt:
#         st.warning("⚠️ Please enter a story prompt.")

# elif tab_selection == "My Stories":
#     st.title("My Stories Library")
    
#     # Create tabs for regular stories and favorites
#     lib_tabs = st.tabs(["All Stories", "Favorites"])
    
#     with lib_tabs[0]:
#         # Display the list of saved stories
#         if not st.session_state.story_history:
#             st.info("You haven't created any stories yet. Go to Create Story to get started!")
#         else:
#             # Search and filter
#             search_term = st.text_input("🔍 Search your stories", "")
            
#             # Filter stories based on search term
#             filtered_stories = st.session_state.story_history
#             if search_term:
#                 filtered_stories = [s for s in st.session_state.story_history if 
#                                     search_term.lower() in s['title'].lower() or 
#                                     search_term.lower() in s['summary'].lower()]
            
#             # Create a grid layout for stories
#             cols = st.columns(3)
#             for idx, story in enumerate(filtered_stories):
#                 with cols[idx % 3]:
#                     st.markdown(f"""
#                     <div class="story-card">
#                         <h3>{story['title']}</h3>
#                         <p><small>{story['timestamp']}</small></p>
#                         <p>{story['summary'][:100]}...</p>
#                     </div>
#                     """, unsafe_allow_html=True)
                    
#                     if st.button(f"Read Story 📖", key=f"read_{idx}"):
#                         st.session_state.selected_story = story
#                         st.rerun()
    
#     with lib_tabs[1]:
#         # Display favorite stories
#         if not st.session_state.favorite_stories:
#             st.info("You haven't added any stories to favorites yet.")
#         else:
#             # Create a grid layout for favorite stories
#             fav_cols = st.columns(3)
#             for idx, story in enumerate(st.session_state.favorite_stories):
#                 with fav_cols[idx % 3]:
#                     st.markdown(f"""
#                     <div class="favorite-card">
#                         <h3>{story['title']}</h3>
#                         <p><small>{story['timestamp']}</small></p>
#                         <p>{story['summary'][:100]}...</p>
#                     </div>
#                     """, unsafe_allow_html=True)
                    
#                     if st.button(f"Read Favorite 📖", key=f"fav_read_{idx}"):
#                         st.session_state.selected_story = story
#                         st.rerun()
                    
#                     if st.button(f"Remove ❌", key=f"fav_rem_{idx}"):
#                         st.session_state.favorite_stories.pop(idx)
#                         st.success("Removed from favorites!")
#                         st.rerun()
    
#     # Display selected story if available
#     if hasattr(st.session_state, 'selected_story'):
#         st.subheader(st.session_state.selected_story['title'])
#         st.write(f"Created: {st.session_state.selected_story['timestamp']}")
        
#         tabs = st.tabs(["Story", "Details"])
#         with tabs[0]:
#             st.write(st.session_state.selected_story['story'])
            
#             # Export options
#             col1, col2 = st.columns(2)
#             with col1:
#                 st.download_button("💾 Download as TXT", 
#                                   st.session_state.selected_story['story'], 
#                                   file_name=f"{st.session_state.selected_story['title']}.txt")
#             with col2:
#                 # Export to PDF with unicode handling
#                 try:
#                     pdf_file = export_to_pdf(st.session_state.selected_story['title'], 
#                                            st.session_state.selected_story['story'])
#                     st.download_button(
#                         "📄 Export as PDF",
#                         data=pdf_file,
#                         file_name=f"{st.session_state.selected_story['title']}.pdf",
#                         mime="application/pdf"
#                     )
#                 except Exception as e:
#                     st.error(f"PDF generation failed: {str(e)}")
            
#         with tabs[1]:
#             if 'parameters' in st.session_state.selected_story:
#                 st.write(f"**Genre:** {st.session_state.selected_story['parameters']['genre']}")
#                 st.write(f"**Tone:** {st.session_state.selected_story['parameters']['tone']}")
#                 st.write(f"**Style:** {st.session_state.selected_story['parameters'].get('style', 'No preference')}")
#                 st.write(f"**Model:** {st.session_state.selected_story['parameters'].get('model', 'default')}")
#                 st.write(f"**Original Prompt:** {st.session_state.selected_story['prompt']}")
#             else:
#                 st.info("No detailed parameters available for this story.")
                
#         if st.button("Back to Library"):
#             del st.session_state.selected_story
#             st.rerun()

# elif tab_selection == "Settings":
#     st.title("Settings")
#     st.write("Configure your story generation preferences here.")
    
#     # App settings
#     st.subheader("Application Settings")
#     animations_enabled = st.checkbox("Enable animations", 
#                                     value=st.session_state.config.get("animations_enabled", True))
#     auto_save = st.checkbox("Auto-save stories", 
#                            value=st.session_state.config.get("auto_save", True))
    
#     # Voice settings
#     st.subheader("Voice Settings")
#     voice_options = ["Default Female", "Default Male", "British Accent", "Australian Accent"]
#     selected_voice = st.selectbox("Default Voice", voice_options, 
#                                  index=voice_options.index(st.session_state.config.get("voice", "Default Male")))
    
#     speech_speed = st.slider("Default Speech Speed", 0.5, 1.5, 
#                             st.session_state.config.get("speech_speed", 1.0), 0.1)
    
#     # Language settings
#     st.subheader("Language Settings")
#     lang_options = ["English", "Spanish", "French", "German"]
#     lang_codes = {"English": "en", "Spanish": "es", "French": "fr", "German": "de"}
#     default_language = st.selectbox("Default Language", lang_options, 
#                                    index=lang_options.index(st.session_state.config.get("default_language", "English")))
    
#     # Store language code in config
#     st.session_state.config["language_code"] = lang_codes[default_language]
    
#     # Account section (placeholder for future implementation)
#     st.subheader("Account")
#     st.info("Login functionality coming soon!")
    
#     # Advanced settings
#     with st.expander("Advanced Settings"):
#         max_length = st.slider("Max Story Length (words)", 500, 5000, 
#                               st.session_state.config.get("max_length", 2500), 500)
        
#     # Save settings button
#     if st.button("Save Settings"):
#         st.session_state.config.update({
#             "animations_enabled": animations_enabled,
#             "auto_save": auto_save,
#             "voice": selected_voice,
#             "speech_speed": speech_speed,
#             "max_length": max_length,
#             "default_language": default_language
#         })
#         save_config(st.session_state.config)
#         st.success("Settings saved successfully!")
        
#     # Data management
#     st.subheader("Data Management")
    
#     if st.button("Export All Stories"):
#         # Create export data
#         export_data = {
#             "stories": st.session_state.story_history,
#             "favorites": st.session_state.favorite_stories,
#             "export_date": time.strftime("%Y-%m-%d %H:%M:%S")
#         }
        
#         # Convert to JSON
#         export_json = json.dumps(export_data, indent=4)
        
#         # Provide download button
#         st.download_button(
#             "Download JSON Export",
#             data=export_json,
#             file_name="story_workshop_export.json",
#             mime="application/json"
#         )
#         st.success("Export ready for download!")
        
#     if st.button("Clear All Data", type="primary"):
#         st.warning("This will delete all your saved stories. This action cannot be undone.")
#         confirm = st.checkbox("I understand the consequences")
#         if confirm and st.button("Confirm Delete"):
#             st.session_state.story_history = []
#             st.session_state.favorite_stories = []
#             st.success("All data has been cleared.")

# # Footer
# st.markdown("""
# ---
# <div style="text-align: center;">
# <p>AI Story Generator v2.0 | Created with ❤️ by You</p>
# </div>
# """, unsafe_allow_html=True)








