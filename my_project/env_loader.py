# env_loader.py
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY not found in environment variables")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1",  # Groq's endpoint
)
