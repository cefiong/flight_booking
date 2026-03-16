import os
import requests
from dotenv import load_dotenv
load_dotenv()

DUFFEL_API_KEY = os.getenv("DUFFEL_API_KEY")
DUFFEL_BASE_URL = os.getenv("DUPPEL_API_BASE_URL")


# Duffel response is super long. Get only a part of it
def search_flight_result_trimmer(raw_response):
    simplified = []

    for offer in raw_response["data"]["offers"]:
        first_slice = offer["slices"][0]
        first_segment = first_slice["segments"][0]

        airline_info = {"id": offer["owner"]["id"], "name":  offer["owner"]["name"], "logo_symbol_url": offer["owner"]["logo_symbol_url"], "iata_code": offer["owner"]["iata_code"]}

        simplified.append({
            "offer_id": offer["id"],
            "airline": airline_info,
            "price": offer["total_amount"],
            "currency": offer["total_currency"],
            "departure": first_segment["departing_at"],
            "arrival": first_segment["arriving_at"],
            "origin": first_segment["origin"]["iata_code"],
            "destination": first_segment["destination"]["iata_code"],
            "stops": len(first_slice["segments"]) - 1
        })

    # Sort by price
    simplified.sort(key=lambda x: float(x["price"]))

    # Return only top 5
    return simplified[:5]



def search_flights(origin_iata, destination_iata, departure_date):
    url = f"{DUFFEL_API_KEY}/offer_requests"

    headers = {
        "Authorization": f"Bearer {DUFFEL_API_KEY}",
        "Duffel-Version": "v2",
        "Content-Type": "application/json"
    }

    body = {
        "data": {
            "slices": [
                {
                    "origin": origin_iata,
                    "destination": destination_iata,
                    "departure_date": departure_date
                }
            ],
            "passengers": [{"type": "adult"}],
            "cabin_class": "economy"
        }
    }

    res = requests.post(url, headers=headers, json=body)
    return search_flight_result_trimmer(res.json)


def create_order(offer_id):
    url = "https://api.duffel.com/air/orders"

    headers = {
        "Authorization": f"Bearer {DUFFEL_API_KEY}",
        "Duffel-Version": "v2",
        "Content-Type": "application/json"
    }

    body = {
        "data": {
            "type": "instant",
            "selected_offers": [offer_id],
            "payments": []  # Simplified
        }
    }

    res = requests.post(url, headers=headers, json=body)
    return res.json()