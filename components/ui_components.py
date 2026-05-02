"""
UI Components
Reusable Streamlit rendering functions for AI TravelMate.
"""

import streamlit as st
from typing import List, Dict, Any
from utils.formatters import format_flight_card


def render_header() -> None:
    """Render the application header banner."""
    st.markdown(
        """
        <div class="header-container">
            <div class="header-title">✈️ AI TravelMate</div>
            <div class="header-subtitle">
                Your intelligent companion for smart, personalised travel planning
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    """Placeholder – sidebar is rendered inline in app.py for tighter input control."""
    pass


def render_flight_section(
    flights: List[Dict[str, Any]], user_inputs: dict
) -> None:
    """
    Render the cheapest flights section.

    Args:
        flights: list of normalised flight dicts.
        user_inputs: original user inputs for context display.
    """
    dep = user_inputs.get("departure_city", "")
    arr = user_inputs.get("destination_city", "")
    dep_date = user_inputs.get("departure_date", "")
    ret_date = user_inputs.get("return_date", "")

    st.markdown(
        f"**Route:** `{dep}` → `{arr}` &nbsp;|&nbsp; "
        f"**Out:** {dep_date} &nbsp;|&nbsp; **Return:** {ret_date}",
        unsafe_allow_html=True,
    )

    if not flights:
        st.warning(
            "No flights found. Please check the IATA codes and dates, "
            "or verify your SERPAPI_KEY."
        )
        return

    cols = st.columns(len(flights))
    for col, flight in zip(cols, flights):
        with col:
            st.markdown(format_flight_card(flight), unsafe_allow_html=True)


def render_hotel_section(hotels_restaurants: str) -> None:
    """
    Render the Hotels & Restaurants recommendation section.

    Args:
        hotels_restaurants: Markdown string from HotelRestaurantAgent.
    """
    if not hotels_restaurants or hotels_restaurants.startswith("⚠️"):
        st.error(hotels_restaurants or "No hotel/restaurant data available.")
        return

    # Split into hotel and restaurant blocks if possible
    text = hotels_restaurants
    if "🍽️" in text or "Restaurant" in text:
        parts = text.split("🍽️", maxsplit=1)
        hotel_block = parts[0]
        rest_block = "🍽️" + parts[1] if len(parts) > 1 else ""
    else:
        hotel_block = text
        rest_block = ""

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🏨 Recommended Hotels")
        st.markdown(
            f'<div class="card">{hotel_block}</div>',
            unsafe_allow_html=True,
        )
    with col2:
        if rest_block:
            st.markdown("#### 🍽️ Recommended Restaurants")
            st.markdown(
                f'<div class="card">{rest_block}</div>',
                unsafe_allow_html=True,
            )


def render_itinerary_section(itinerary: str, user_inputs: dict) -> None:
    """
    Render the day-by-day itinerary.

    Args:
        itinerary: Markdown string from PlannerAgent.
        user_inputs: original user inputs dict.
    """
    if not itinerary or itinerary.startswith("⚠️"):
        st.error(itinerary or "No itinerary data available.")
        return

    duration = user_inputs.get("trip_duration", 0)
    destination = user_inputs.get("destination_city", "")

    st.info(
        f"📅 **{duration}-day itinerary** crafted for your **{destination}** adventure. "
        "Expand each day to see the full plan."
    )

    # Try to split by "Day" sections for expander UX
    lines = itinerary.split("\n")
    days: Dict[str, List[str]] = {}
    current_day = "Overview"

    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("day ") or stripped.startswith("## Day"):
            current_day = stripped.lstrip("#").strip()
            days.setdefault(current_day, [])
        else:
            days.setdefault(current_day, []).append(line)

    if len(days) <= 1:
        # Fallback: render as a single block
        st.markdown(
            f'<div class="card" style="line-height:1.9;">{itinerary}</div>',
            unsafe_allow_html=True,
        )
        return

    for day_title, day_lines in days.items():
        content = "\n".join(day_lines).strip()
        if not content:
            continue
        with st.expander(f"📅 {day_title}", expanded=(day_title == list(days.keys())[0])):
            st.markdown(content)
