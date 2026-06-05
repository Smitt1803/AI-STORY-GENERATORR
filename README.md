# 📚 AI Story Generator

An advanced AI-powered story generation platform that allows users to create custom stories based on prompts, genres, tone, and style. This project includes a FastAPI backend for story generation and authentication, and a modern Streamlit-based frontend for user interaction.

---

##  Features

- Custom Story Generation (Genre, Tone, Style, Length, Plot Twist, etc.)
-  Multiple LLM model support (via Groq API)
-  Summarization, Title Generation, Entity & Theme Extraction, Sentiment Analysis
-  User Authentication (Email + OTP)
-  Async Job Processing for long stories
-  MongoDB for user data
-  Streamlit UI with Login/Register + Story Management
-  Text-to-Speech (TTS) and PDF/MP3 Downloads

---

---

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-story-generator.git
cd ai-story-generator
```

### 2. Install Dependencies
#### Create a virtual environment and install:

-  for env file - create virtual env
```bash
py -m venv venv
pip install -r requirements.txt
```


- for poetry 
```bash
poetry install
```

### 3. Setup Environment

Create a .env file with the following:

```bash
GROQ_API_KEY=your_groq_api_key
API_BASE_URL=http://localhost:8000
```

### 4. Start MongoDB

Ensure MongoDB is running locally on  **mongodb://localhost:27017.**

### 5. Run FastAPI Backend

```bash 
poetry run uvicorn app.main:app --reload
```

### 6. Run Streamlit Frontend

```bash
poetry run streamlit run .\app\streamlit_frontend\streamlit_app.py
```

--- 

## Authentication

- Users register via name, email, and password.

- Login flow includes OTP verification sent via email (implement send_email_otp in mail_utils.py).

- Passwords are securely hashed using bcrypt.


---

## Supported Models

You can select from the following LLMs:

  - llama3-70b

  - llama3-8b

  - qwen-qwq-32b

  - creative (high creativity)

  - concise (short & focused)

These are loaded via the Groq API (ChatGroq from langchain_groq).

---

## API Endpoints

| Endpoint           | Method | Description                   |
| ------------------ | ------ | ----------------------------- |
| `/register/`       | POST   | Register new user             |
| `/login/`          | POST   | Login user (triggers OTP)     |
| `/verify-otp/`     | POST   | Verify OTP & return JWT token |
| `/generate/`       | POST   | Generate story (sync)         |
| `/generate/async/` | POST   | Generate story (async)        |
| `/models`          | GET    | List available models         |



## Screenshots

![App Screenshot][def]

![App Screenshot][def2]

![App Screenshot][def3]

![App Screenshot][def4]

![App Screenshot][def5]

![App Screenshot][def6]

[def]: ./assets/st1.png

[def2]: ./assets/st2.png

[def3]: ./assets/st3.png

[def4]: ./assets/st4.png

[def5]: ./assets/st5.png

[def6]: ./assets/st6.png




