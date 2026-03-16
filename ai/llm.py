# llm.py
import os
import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types

from models.chat import LLMResponse

load_dotenv()

TOOLS = [
    {
        "name": "search_flights",
        "description": "Search flights using IATA airport codes",
        "parameters": {
            "type": "object",
            "properties": {
                "origin_iata": {"type": "string"},
                "destination_iata": {"type": "string"},
                "departure_date": {"type": "string"}
            },
            "required": [
                "origin_iata",
                "destination_iata",
                "departure_date"
            ]
        }
    },
    {
        "name": "book_flight",
        "description": "Book a selected flight offer",
        "parameters": {
            "type": "object",
            "properties": {
                "offer_id": {"type": "string"}
            },
            "required": ["offer_id"]
        }
    }
]

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
current_date = datetime.datetime.now()

system_prompt1 = f"""
You are a Flight booking assistant that understands user intention and calls relevant tools only.
Also, extract the IATA codes for Cities in User query. The current date is {current_date}.
"""

system_prompt = f"""
You are an AI flight booking assistant.

Your job is to help users search and book flights using available backend tools.

Important rules:

1. Always extract structured information from the user message when possible:
   - origin_city
   - origin_airport (IATA code)
   - destination_city
   - destination_airport (IATA code)
   - date
   - time preference (morning, afternoon, evening)

2. If required information is missing, ask the user for clarification instead of calling a tool.

3. Only call tools when enough information is available.

4. When flights are shown, ask the user to select one option.

5. When the user selects a flight, retrieve the latest details before booking.

6. Always confirm with the user before creating a booking.

7. Be conversational and natural.

Today's date is: {current_date}
"""

client = genai.Client(api_key=GEMINI_API_KEY)

tools = types.Tool(function_declarations=TOOLS)
#CONFIG = types.GenerateContentConfig(tools=[tools], system_instruction=system_prompt, response_mime_type="application/json", response_json_schema=LLMResponse.model_json_schema())

CONFIG = types.GenerateContentConfig(tools=[tools], system_instruction=system_prompt, response_mime_type="application/json")
MODEL = "gemini-2.5-flash"