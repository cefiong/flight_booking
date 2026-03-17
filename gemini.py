from google import genai
from google.genai import types
import os

from pydantic import BaseModel, Field
from typing import List, Optional

from dotenv import load_dotenv
load_dotenv()


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DUFFEL_API_KEY = os.getenv("DUFFEL_API_KEY")
DUFFEL_BASE_URL = os.getenv("DUPPEL_API_BASE_URL")


class Flight(BaseModel):
    pass

class Flights(BaseModel):
    flights: List[Flight] = []



def get_iata_from_city(city: str) -> list[str]:
    """Get the IATA codes for the given city.

    Args:
        city: The city to get the IATA code for.

    Returns:
        The IATA code for the given city.
    """
    if city == "Vienna":
        return ["VIE"]
    elif city == "London":
        return ["LON"]
    else:
        return ["MUC"]


def search_flight(source_airport_iata: str, target_airport_iata: str, flight_date: str) -> list[dict]:
    """Search flight from source_airport to target_airport for the specified flight date.

    Args:
        source_airport_iata: Source Airport IATA code.
        target_airport_iata: Destination Airport IATA code.
        flight_date: The flight date.

    Returns:
        A dictionary containing the flights details. Also ask user to select a flight from the list.
    """
    flights = [
        {"source": "VIE", "destination": "MUC", "time": "08:00", "flight_time": "2 hrs","price": "50 euros", "flight_id": "1"},
        {"source": "VIE", "destination": "MUC", "time": "12:00", "flight_time": "1hr 30mins","price": "100 euros", "flight_id": "2"},
        {"source": "VIE", "destination": "MUC", "time": "14:00", "flight_time": "2 hrs", "price": "59 euros", "flight_id": "3"},
    ]

    return flights


def show_updated_flight_details(flight_id: str) -> dict:
    """Show updated flight details.
    Args:
        flight_id: The flight ID.

    Returns:
        A dictionary containing the updated flight details for the chosen flight ID.
    """

    print("The chosen flight ID is: ", flight_id)

    return {"source": "VIE", "destination": "MUC", "time": "08:00", "flight_time": "2 hrs","actual_price": "120 euros", "flight_id": flight_id},


# Configure the client
client = genai.Client(api_key=GEMINI_API_KEY)
config = types.GenerateContentConfig(
    tools=[get_iata_from_city, search_flight, show_updated_flight_details]
)


conversation_history = []

user = input("User: ")
while user != "quit":
    # Add user message
    conversation_history.append(
        types.Content(
            role="user",
            parts=[types.Part(text=user)]
        )
    )

    # Make the request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation_history,
        config=config,
    )
    print(f"{response.text}")

    # Add model response to history
    conversation_history.append(response.candidates[0].content)

    user = input("User: ")