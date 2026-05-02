"""
Tests for utils/formatters.py
Run with: pytest tests/
"""

import pytest
from utils.formatters import format_flight_card, format_itinerary_html, budget_table_html


SAMPLE_FLIGHT = {
    "airline": "Test Airways",
    "airline_logo": "https://example.com/logo.png",
    "departure_airport": "Delhi International",
    "departure_time": "2025-06-01 10:00",
    "arrival_airport": "Bangkok Suvarnabhumi",
    "arrival_time": "2025-06-01 15:30",
    "duration": "5h 30m",
    "price": 800.0,
    "price_display": "$800",
    "booking_url": "https://example.com/book",
    "stops": 0,
    "stop_label": "Non-stop",
}


class TestFormatFlightCard:

    def test_contains_airline_name(self):
        html = format_flight_card(SAMPLE_FLIGHT)
        assert "Test Airways" in html

    def test_contains_price(self):
        html = format_flight_card(SAMPLE_FLIGHT)
        assert "$800" in html

    def test_contains_booking_url(self):
        html = format_flight_card(SAMPLE_FLIGHT)
        assert "https://example.com/book" in html

    def test_contains_stop_label(self):
        html = format_flight_card(SAMPLE_FLIGHT)
        assert "Non-stop" in html

    def test_contains_logo(self):
        html = format_flight_card(SAMPLE_FLIGHT)
        assert "https://example.com/logo.png" in html

    def test_no_logo_when_missing(self):
        flight_no_logo = {**SAMPLE_FLIGHT, "airline_logo": ""}
        html = format_flight_card(flight_no_logo)
        assert "<img" not in html


class TestFormatItineraryHtml:

    def test_wraps_content(self):
        html = format_itinerary_html("Day 1: Arrive in Bangkok")
        assert "Day 1: Arrive in Bangkok" in html
        assert "<div" in html

    def test_returns_string(self):
        result = format_itinerary_html("Some itinerary text")
        assert isinstance(result, str)


class TestBudgetTableHtml:

    def test_renders_all_categories(self):
        breakdown = {"Flights": 500, "Hotels": 300, "Food": 200, "Activities": 100}
        html = budget_table_html(breakdown)
        for category in breakdown:
            assert category in html

    def test_total_row_present(self):
        breakdown = {"Flights": 500, "Hotels": 300}
        html = budget_table_html(breakdown)
        assert "Total" in html
        assert "$800" in html

    def test_empty_breakdown(self):
        html = budget_table_html({})
        assert "Total" in html
        assert "$0" in html
