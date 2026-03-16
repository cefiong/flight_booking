import json
with open("flight.json", "r") as file:
    raw_response = json.load(file)

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
    #print(simplified[:1])
    pretty_json_string = json.dumps(simplified[:2], indent=4)
    print(pretty_json_string)