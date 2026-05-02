"""
AI TravelMate - An Intelligent Agent for Smart Travel Planning and Assistance
Main Streamlit Application Entry Point
"""

import streamlit as st
from datetime import date, timedelta
from agents.researcher_agent import ResearcherAgent
from agents.planner_agent import PlannerAgent
from agents.hotel_restaurant_agent import HotelRestaurantAgent
from utils.flight_utils import fetch_flights, extract_cheapest_flights
from utils.formatters import format_itinerary_html, format_flight_card
from components.ui_components import render_header, render_sidebar, render_flight_section
from components.ui_components import render_hotel_section, render_itinerary_section

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI TravelMate",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Global */
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .main { padding: 1rem 2rem; }

    /* Header */
    .header-container {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .header-title {
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .header-subtitle {
        font-size: 1.1rem;
        opacity: 0.85;
        margin-top: 0.5rem;
    }

    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.2rem;
        border-left: 4px solid #0f3460;
    }
    .flight-card {
        background: #f8f9ff;
        border-radius: 10px;
        padding: 1.2rem;
        border: 1px solid #e0e7ff;
        margin: 0.5rem 0;
    }
    .price-badge {
        background: #0f3460;
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
    }

    /* Section headers */
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f3460;
        border-bottom: 2px solid #0f3460;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Spinner */
    .stSpinner { color: #0f3460; }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #0f3460, #16213e);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(15,52,96,0.3);
    }

    /* Tips box */
    .tips-box {
        background: #fff8e1;
        border-left: 4px solid #ffc107;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# ─── Header ───────────────────────────────────────────────────────────────────
render_header()

# ─── Sidebar – User Inputs ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🗺️ Plan Your Trip")
    st.markdown("---")

    departure_city = st.text_input(
        "🛫 Departure City (IATA code)",
        value="DEL",
        help="E.g., DEL for Delhi, BOM for Mumbai, NYC for New York"
    )
    destination_city = st.text_input(
        "🛬 Destination City (IATA code)",
        value="BKK",
        help="E.g., BKK for Bangkok, SIN for Singapore, DXB for Dubai"
    )

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        departure_date = st.date_input(
            "📅 Departure Date",
            value=date.today() + timedelta(days=14),
            min_value=date.today()
        )
    with col2:
        return_date = st.date_input(
            "📅 Return Date",
            value=date.today() + timedelta(days=21),
            min_value=date.today() + timedelta(days=1)
        )

    trip_duration = (return_date - departure_date).days
    st.info(f"🕐 Trip Duration: **{trip_duration} day(s)**")

    st.markdown("---")
    budget = st.selectbox(
        "💰 Budget (per person)",
        ["Budget (< $500)", "Economy ($500–$1500)", "Mid-range ($1500–$3000)", "Luxury (> $3000)"]
    )

    travel_theme = st.selectbox(
        "🎯 Travel Theme",
        ["Adventure", "Family Vacation", "Romantic Getaway", "Solo Travel", "Business", "Cultural Exploration"]
    )

    activities = st.multiselect(
        "🎪 Preferred Activities",
        ["Sightseeing", "Adventure Sports", "Nightlife", "Shopping", "Food & Cuisine",
         "Nature & Wildlife", "Historical Sites", "Beach & Water Sports", "Art & Museums"],
        default=["Sightseeing", "Food & Cuisine"]
    )

    st.markdown("---")

    # Packing checklist
    with st.expander("🧳 Packing Checklist"):
        st.checkbox("Passport / Visa")
        st.checkbox("Travel Insurance")
        st.checkbox("Foreign Currency")
        st.checkbox("Clothes")
        st.checkbox("Medications")
        st.checkbox("Chargers & Adapters")
        st.checkbox("Comfortable Footwear")

    generate_btn = st.button("✨ Plan Your Adventure", use_container_width=True)

# ─── Main Content ─────────────────────────────────────────────────────────────
if generate_btn:
    if not departure_city or not destination_city:
        st.error("Please enter both departure and destination cities.")
    elif departure_date >= return_date:
        st.error("Return date must be after departure date.")
    else:
        user_inputs = {
            "departure_city": departure_city.upper().strip(),
            "destination_city": destination_city.upper().strip(),
            "departure_date": str(departure_date),
            "return_date": str(return_date),
            "trip_duration": trip_duration,
            "budget": budget,
            "travel_theme": travel_theme,
            "activities": activities,
        }

        # ── Step 1: Flights ────────────────────────────────────────────────
        st.markdown('<div class="section-header">✈️ Cheapest Flight Options</div>', unsafe_allow_html=True)
        with st.spinner("Searching for the best flights..."):
            raw_flights = fetch_flights(user_inputs)
            cheapest = extract_cheapest_flights(raw_flights)
        render_flight_section(cheapest, user_inputs)

        st.markdown("---")

        # ── Step 2: AI Agents ──────────────────────────────────────────────
        researcher = ResearcherAgent()
        planner = PlannerAgent()
        hotel_agent = HotelRestaurantAgent()

        with st.spinner("🔍 Research Agent gathering destination insights..."):
            destination_info = researcher.research(user_inputs)

        with st.spinner("🏨 Hotel & Restaurant Agent finding the best stays and eats..."):
            hotels_restaurants = hotel_agent.recommend(user_inputs, destination_info)

        st.markdown('<div class="section-header">🏨 Hotels & Restaurants</div>', unsafe_allow_html=True)
        render_hotel_section(hotels_restaurants)

        st.markdown("---")

        with st.spinner("🗓️ Planner Agent crafting your personalised itinerary..."):
            itinerary = planner.create_itinerary(user_inputs, destination_info, hotels_restaurants)

        st.markdown('<div class="section-header">📋 Your Personalised Itinerary</div>', unsafe_allow_html=True)
        render_itinerary_section(itinerary, user_inputs)

        # ── Tips ───────────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown('<div class="section-header">💡 Tips for Your Journey</div>', unsafe_allow_html=True)
        with st.spinner("Generating travel tips..."):
            tips = researcher.get_travel_tips(user_inputs)
        st.markdown(f'<div class="tips-box">{tips}</div>', unsafe_allow_html=True)

        # ── Currency Exchange ──────────────────────────────────────────────
        st.markdown("---")
        with st.expander("💱 Currency Exchange Reference"):
            from utils.currency_utils import get_currency_info
            currency_html = get_currency_info(destination_city)
            st.markdown(currency_html, unsafe_allow_html=True)

else:
    # Landing state
    st.markdown("""
    <div style="text-align:center; padding: 3rem 1rem; color: #666;">
        <h2 style="color:#0f3460;">👈 Fill in your travel details to get started</h2>
        <p style="font-size:1.1rem;">
            AI TravelMate uses <strong>Google Gemini AI</strong> + <strong>real-time flight data</strong> 
            to craft a fully personalised trip plan — flights, hotels, restaurants, and a day-by-day itinerary.
        </p>
        <br/>
        <div style="display:flex; justify-content:center; gap:2rem; flex-wrap:wrap;">
            <div style="background:#f0f4ff; border-radius:12px; padding:1.5rem 2rem; min-width:180px;">
                <div style="font-size:2rem;">🤖</div>
                <div style="font-weight:600; margin-top:0.5rem;">Gemini AI Agents</div>
                <div style="font-size:0.9rem; color:#888;">Research, Plan & Recommend</div>
            </div>
            <div style="background:#f0fff4; border-radius:12px; padding:1.5rem 2rem; min-width:180px;">
                <div style="font-size:2rem;">✈️</div>
                <div style="font-weight:600; margin-top:0.5rem;">Live Flight Data</div>
                <div style="font-size:0.9rem; color:#888;">Powered by SerpAPI</div>
            </div>
            <div style="background:#fff8f0; border-radius:12px; padding:1.5rem 2rem; min-width:180px;">
                <div style="font-size:2rem;">🗓️</div>
                <div style="font-weight:600; margin-top:0.5rem;">Day-wise Itinerary</div>
                <div style="font-size:0.9rem; color:#888;">Budget-aware Planning</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
