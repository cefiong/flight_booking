import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ai.tools import search_flights, get_iata_from_city

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# Configure the client

CLIENT = genai.Client(api_key=GEMINI_API_KEY)
CONFIG = types.GenerateContentConfig(
    tools=[get_iata_from_city, search_flights]
)

MODEL = "gemini-2.5-flash"