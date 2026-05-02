"""
Flight Utilities
Fetches real-time flight data from Google Flights via SerpAPI
and extracts the cheapest / most relevant options.
"""

import os
import requests
from typing import List, Dict, Any


SERPAPI_BASE_URL = "https://serpapi.com/search"


def fetch_flights(user_inputs: dict) -> List[Dict[str, Any]]:
    """
    Retrieve flight results from Google Flights via SerpAPI.

    Args:
        user_inputs: dict containing departure_city, destination_city,
                     departure_date, return_date.

    Returns:
        List of raw flight result dicts from the API response.
        Returns an empty list if the API key is missing or the call fails.
    """
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        # Return mock data so the UI can still be demoed without a live key
        return _mock_flights(user_inputs)

    params = {
        "engine": "google_flights",
        "departure_id": user_inputs.get("departure_city", ""),
        "arrival_id": user_inputs.get("destination_city", ""),
        "outbound_date": user_inputs.get("departure_date", ""),
        "return_date": user_inputs.get("return_date", ""),
        "currency": "USD",
        "hl": "en",
        "api_key": api_key,
        "type": "1",  # Round trip
    }

    try:
        response = requests.get(SERPAPI_BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data.get("best_flights", []) + data.get("other_flights", [])
    except requests.exceptions.Timeout:
        print("⚠️ SerpAPI request timed out. Returning mock data.")
        return _mock_flights(user_inputs)
    except requests.exceptions.HTTPError as exc:
        print(f"⚠️ SerpAPI HTTP error: {exc}. Returning mock data.")
        return _mock_flights(user_inputs)
    except Exception as exc:
        print(f"⚠️ Unexpected error fetching flights: {exc}. Returning mock data.")
        return _mock_flights(user_inputs)


def extract_cheapest_flights(
    flights: List[Dict[str, Any]], top_n: int = 3
) -> List[Dict[str, Any]]:
    """
    Sort flights by price and return the cheapest `top_n` options.

    Args:
        flights: raw list of flight dicts.
        top_n: number of cheapest flights to return (default 3).

    Returns:
        Sorted list of up to `top_n` flight dicts with normalised keys.
    """
    if not flights:
        return []

    normalised = []
    for f in flights:
        try:
            price = float(str(f.get("price", "9999999")).replace(",", "").replace("$", ""))
            legs = f.get("flights", [{}])
            first_leg = legs[0] if legs else {}
            last_leg = legs[-1] if len(legs) > 1 else first_leg

            normalised.append({
                "airline": first_leg.get("airline", "Unknown Airline"),
                "airline_logo": first_leg.get("airline_logo", ""),
                "departure_airport": first_leg.get("departure_airport", {}).get("name", "—"),
                "departure_time": first_leg.get("departure_airport", {}).get("time", "—"),
                "arrival_airport": last_leg.get("arrival_airport", {}).get("name", "—"),
                "arrival_time": last_leg.get("arrival_airport", {}).get("time", "—"),
                "duration": f.get("total_duration", "—"),
                "price": price,
                "price_display": f"${price:,.0f}",
                "booking_url": f.get("booking_token", "#"),
                "stops": len(legs) - 1,
                "stop_label": "Non-stop" if len(legs) == 1 else f"{len(legs)-1} stop(s)",
            })
        except (ValueError, TypeError, KeyError):
            continue

    normalised.sort(key=lambda x: x["price"])
    return normalised[:top_n]


# ─── Mock data (used when SERPAPI_KEY is absent) ──────────────────────────────

def _mock_flights(user_inputs: dict) -> List[Dict[str, Any]]:
    """Return three placeholder flight records for UI demonstration."""
    dep = user_inputs.get("departure_city", "DEL")
    arr = user_inputs.get("destination_city", "BKK")
    dep_date = user_inputs.get("departure_date", "2025-01-01")

    return [
        {
            "flights": [
                {
                    "airline": "British Airways",
                    "airline_logo": "",
                    "departure_airport": {"name": f"{dep} International Airport", "time": f"{dep_date} 09:30"},
                    "arrival_airport": {"name": f"{arr} International Airport", "time": f"{dep_date} 14:00"},
                }
            ],
            "total_duration": "4h 30m",
            "price": "62030",
        },
        {
            "flights": [
                {
                    "airline": "Air India",
                    "airline_logo": "",
                    "departure_airport": {"name": f"{dep} International Airport", "time": f"{dep_date} 11:15"},
                    "arrival_airport": {"name": f"{arr} International Airport", "time": f"{dep_date} 16:30"},
                }
            ],
            "total_duration": "5h 15m",
            "price": "63956",
        },
        {
            "flights": [
                {
                    "airline": "Etihad",
                    "airline_logo": "",
                    "departure_airport": {"name": f"{dep} International Airport", "time": f"{dep_date} 07:00"},
                    "arrival_airport": {"name": f"{arr} International Airport", "time": f"{dep_date} 13:45"},
                }
            ],
            "total_duration": "6h 45m",
            "price": "85210",
        },
    ]
