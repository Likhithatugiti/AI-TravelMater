"""AI TravelMate – Utilities Package"""

from .flight_utils import fetch_flights, extract_cheapest_flights
from .formatters import format_flight_card, format_itinerary_html, budget_table_html
from .currency_utils import get_currency_info
from .prompts import (
    RESEARCHER_SYSTEM_PROMPT,
    TRAVEL_TIPS_PROMPT,
    PLANNER_SYSTEM_PROMPT,
    HOTEL_RESTAURANT_PROMPT,
)

__all__ = [
    "fetch_flights",
    "extract_cheapest_flights",
    "format_flight_card",
    "format_itinerary_html",
    "budget_table_html",
    "get_currency_info",
    "RESEARCHER_SYSTEM_PROMPT",
    "TRAVEL_TIPS_PROMPT",
    "PLANNER_SYSTEM_PROMPT",
    "HOTEL_RESTAURANT_PROMPT",
]
