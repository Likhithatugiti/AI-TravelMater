"""
Tests for utils/flight_utils.py
Run with: pytest tests/
"""

import pytest
from utils.flight_utils import extract_cheapest_flights, _mock_flights


# ─── Fixtures ─────────────────────────────────────────────────────────────────

SAMPLE_USER_INPUTS = {
    "departure_city": "DEL",
    "destination_city": "BKK",
    "departure_date": "2025-06-01",
    "return_date": "2025-06-08",
    "trip_duration": 7,
    "budget": "Mid-range ($1500–$3000)",
    "travel_theme": "Adventure",
    "activities": ["Sightseeing", "Adventure Sports"],
}

SAMPLE_RAW_FLIGHTS = [
    {
        "flights": [
            {
                "airline": "Test Airways",
                "airline_logo": "",
                "departure_airport": {"name": "Delhi International", "time": "2025-06-01 10:00"},
                "arrival_airport": {"name": "Bangkok International", "time": "2025-06-01 15:30"},
            }
        ],
        "total_duration": "5h 30m",
        "price": "800",
    },
    {
        "flights": [
            {
                "airline": "Cheap Fly",
                "airline_logo": "",
                "departure_airport": {"name": "Delhi International", "time": "2025-06-01 06:00"},
                "arrival_airport": {"name": "Bangkok International", "time": "2025-06-01 13:00"},
            }
        ],
        "total_duration": "7h 00m",
        "price": "550",
    },
    {
        "flights": [
            {
                "airline": "Premium Air",
                "airline_logo": "",
                "departure_airport": {"name": "Delhi International", "time": "2025-06-01 14:00"},
                "arrival_airport": {"name": "Bangkok International", "time": "2025-06-01 18:30"},
            }
        ],
        "total_duration": "4h 30m",
        "price": "1200",
    },
]


# ─── Tests ────────────────────────────────────────────────────────────────────

class TestExtractCheapestFlights:

    def test_returns_sorted_by_price(self):
        results = extract_cheapest_flights(SAMPLE_RAW_FLIGHTS, top_n=3)
        prices = [r["price"] for r in results]
        assert prices == sorted(prices), "Flights should be sorted ascending by price"

    def test_top_n_limit(self):
        results = extract_cheapest_flights(SAMPLE_RAW_FLIGHTS, top_n=2)
        assert len(results) == 2

    def test_returns_all_when_fewer_than_top_n(self):
        results = extract_cheapest_flights(SAMPLE_RAW_FLIGHTS[:1], top_n=5)
        assert len(results) == 1

    def test_empty_input_returns_empty(self):
        results = extract_cheapest_flights([])
        assert results == []

    def test_normalised_keys_present(self):
        results = extract_cheapest_flights(SAMPLE_RAW_FLIGHTS, top_n=1)
        expected_keys = {
            "airline", "airline_logo", "departure_airport", "departure_time",
            "arrival_airport", "arrival_time", "duration", "price",
            "price_display", "booking_url", "stops", "stop_label",
        }
        assert expected_keys.issubset(set(results[0].keys()))

    def test_price_display_format(self):
        results = extract_cheapest_flights(SAMPLE_RAW_FLIGHTS, top_n=1)
        assert results[0]["price_display"].startswith("$")

    def test_stops_calculation(self):
        results = extract_cheapest_flights(SAMPLE_RAW_FLIGHTS, top_n=3)
        for r in results:
            assert r["stops"] == 0  # All sample flights have 1 leg → non-stop
            assert r["stop_label"] == "Non-stop"


class TestMockFlights:

    def test_returns_three_flights(self):
        flights = _mock_flights(SAMPLE_USER_INPUTS)
        assert len(flights) == 3

    def test_contains_price_field(self):
        flights = _mock_flights(SAMPLE_USER_INPUTS)
        for f in flights:
            assert "price" in f

    def test_airline_names_present(self):
        flights = _mock_flights(SAMPLE_USER_INPUTS)
        airlines = [f["flights"][0]["airline"] for f in flights]
        assert "British Airways" in airlines
        assert "Air India" in airlines
        assert "Etihad" in airlines
