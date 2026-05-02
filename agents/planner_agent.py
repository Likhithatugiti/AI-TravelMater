"""
Planner Agent
Creates an elaborate day-wise travel plan incorporating flights,
hotels, restaurants, and activities using Gemini AI.
"""

import os
import google.generativeai as genai
from utils.prompts import PLANNER_SYSTEM_PROMPT


class PlannerAgent:
    """
    Gemini-powered agent that produces a structured day-by-day
    itinerary based on researcher output and hotel/restaurant data.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY environment variable is not set."
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.6,
                "top_p": 0.9,
                "max_output_tokens": 4096,
            },
        )

    def create_itinerary(
        self,
        user_inputs: dict,
        destination_info: str,
        hotels_restaurants: str,
    ) -> str:
        """
        Generate a detailed day-wise itinerary.

        Args:
            user_inputs: dict with travel preferences and constraints.
            destination_info: research output from ResearcherAgent.
            hotels_restaurants: hotel & restaurant output from HotelRestaurantAgent.

        Returns:
            Markdown-formatted itinerary string.
        """
        destination = user_inputs.get("destination_city", "")
        departure = user_inputs.get("departure_city", "")
        duration = user_inputs.get("trip_duration", 7)
        budget = user_inputs.get("budget", "Mid-range")
        theme = user_inputs.get("travel_theme", "")
        activities = ", ".join(user_inputs.get("activities", []))
        dep_date = user_inputs.get("departure_date", "")
        ret_date = user_inputs.get("return_date", "")

        prompt = PLANNER_SYSTEM_PROMPT.format(
            destination=destination,
            departure=departure,
            duration=duration,
            budget=budget,
            theme=theme,
            activities=activities,
            departure_date=dep_date,
            return_date=ret_date,
            destination_info=destination_info,
            hotels_restaurants=hotels_restaurants,
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as exc:
            return (
                f"⚠️ Planner Agent encountered an error: {exc}\n\n"
                "Please check your GEMINI_API_KEY."
            )
