from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


def load_llm(model_name="llama3-70b-8192"):
    """Load the default language model"""
    return ChatGroq(
        api_key=os.getenv("GROQ_API_KEY"),
        model=model_name,
        temperature=0.6,
    )


def get_available_models():
    """Get all available language models"""
    # Dictionary of available models - could be expanded
    models = {
        "llama3-70b": ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.6,
        ),
        "llama3-8b": ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.7,
        ),
        "qwen-qwq-32b": ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.8,
        ),
        "creative": ChatGroq(  # Model tuned for creative writing
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.9,  # Higher temperature for more creativity
        ),
        "concise": ChatGroq(  # Model tuned for shorter outputs
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.1-8b-instant",
            temperature=0.4,  # Lower temperature for more focused outputs
        )
    }

    return models

# from langchain.chat_models import ChatGroq
# from langchain_groq import ChatGroq
# import os
# from dotenv import load_dotenv

# load_dotenv()
# def load_llm():
#     return ChatGroq(
#         api_key=os.getenv("GROQ_API_KEY"),
#         model="llama3-70b-8192",  # or llama3-70b-8192 if enabled
#         temperature=0.6,
#     )
