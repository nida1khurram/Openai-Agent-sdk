import os
from agents import Agent, Runner
from dotenv import load_dotenv
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# __________________________________________

client = AsyncOpenAI(
    api_key = GEMINI_API_KEY,
    base_url = 'https://generativelanguage.googleapis.com/v1beta/openai/'
)