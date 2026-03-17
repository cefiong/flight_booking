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


def search_flights_api_call(origin_iata: str, destination_iata:str, departure_date:str):
    """Search flight from source_airport to target_airport for the specified flight date.

    Args:
        source_airport_iata: Source Airport IATA code.
        target_airport_iata: Destination Airport IATA code.
        flight_date: The flight date.

    Returns:
        A dictionary containing the flights details. Also ask user to select a flight from the list.
    """

    url = f"{DUFFEL_BASE_URL}/offer_requests"

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
    flight_result = search_flight_result_trimmer(res.json())
    print(flight_result)
    return flight_result



def search_flights(origin_iata: str, destination_iata:str, departure_date:str):
    """Search flight from source_airport to target_airport for the specified flight date.

    Args:
        source_airport_iata: Source Airport IATA code.
        target_airport_iata: Destination Airport IATA code.
        flight_date: The flight date.

    Returns:
        A dictionary containing the flights details. Also ask user to select a flight from the list.
    """

    flights = [
        {
            'offer_id': 'off_0000B4LV5mjGY4tBdIaXwS',
            'airline':
                {
                    'id': 'arl_00009VME7D6ivUu8dn35WK',
                    'name': 'Duffel Airways',
                    'logo_symbol_url': 'https://assets.duffel.com/img/airlines/for-light-background/full-color-logo/ZZ.svg',
                    'iata_code': 'ZZ'
                },
            'price': '49.18',
            'currency': 'EUR',
            'departure': '2026-06-22T16:15:00',
            'arrival': '2026-06-22T17:18:00',
            'origin': 'VIE',
            'destination': 'MUC',
            'stops': 0
        },
        {
            'offer_id': 'off_0000B4LV5smK3ctoOW44YI',
            'airline':
                {
                    'id': 'arl_00009VME7DCkZ5j0wTrtvG',
                    'name': 'Lufthansa',
                    'logo_symbol_url': 'https://assets.duffel.com/img/airlines/for-light-background/full-color-logo/LH.svg',
                    'iata_code': 'LH'
                },
            'price': '106.61',
            'currency': 'EUR',
            'departure': '2026-06-22T06:10:00',
            'arrival': '2026-06-22T07:10:00',
            'origin': 'VIE',
            'destination': 'MUC',
            'stops': 0
        },
        {
            'offer_id': 'off_0000B4LV5sly4wcENPtmzU',
            'airline':
                {
                    'id': 'arl_00009VME7DCkZ5j0wTrtvG',
                    'name': 'Lufthansa',
                    'logo_symbol_url': 'https://assets.duffel.com/img/airlines/for-light-background/full-color-logo/LH.svg',
                    'iata_code': 'LH'
                },
            'price': '106.61',
            'currency': 'EUR',
            'departure': '2026-06-22T13:15:00',
            'arrival': '2026-06-22T14:15:00',
            'origin': 'VIE',
            'destination': 'MUC',
            'stops': 0
        },
        {
            'offer_id': 'off_0000B4LV5slc6GKeMJjVRA',
            'airline':
                {
                    'id': 'arl_00009VME7DCkZ5j0wTrtvG',
                    'name': 'Lufthansa',
                    'logo_symbol_url': 'https://assets.duffel.com/img/airlines/for-light-background/full-color-logo/LH.svg',
                    'iata_code': 'LH'
                },
            'price': '106.61',
            'currency': 'EUR',
            'departure': '2026-06-22T19:55:00',
            'arrival': '2026-06-22T20:55:00',
            'origin': 'VIE',
            'destination': 'MUC',
            'stops': 0
        },
        {
            'offer_id': 'off_0000B4LV5r52N4gH7ynzQp',
            'airline': {
                'id': 'arl_00009VME7DCkZ5j0wTrtuw',
                'name': 'LOT Polish Airlines',
                'logo_symbol_url': 'https://assets.duffel.com/img/airlines/for-light-background/full-color-logo/LO.svg',
                'iata_code': 'LO'
            },
            'price': '129.98',
            'currency': 'EUR',
            'departure': '2026-06-22T19:30:00',
            'arrival': '2026-06-22T20:45:00',
            'origin': 'VIE',
            'destination': 'WAW',
            'stops': 1
        }
    ]
    return flights

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