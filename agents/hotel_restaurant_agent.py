"""
Hotel & Restaurant Finder Agent
Recommends high-rated restaurants and hotels based on
user budget and preferences using Gemini AI.
"""

import os
import google.generativeai as genai
from utils.prompts import HOTEL_RESTAURANT_PROMPT


class HotelRestaurantAgent:
    """
    Gemini-powered agent that recommends hotels and restaurants
    tailored to the user's budget, theme, and activity preferences.
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
                "temperature": 0.65,
                "top_p": 0.9,
                "max_output_tokens": 2048,
            },
        )

    def recommend(self, user_inputs: dict, destination_info: str) -> str:
        """
        Generate hotel and restaurant recommendations.

        Args:
            user_inputs: dict with travel constraints and preferences.
            destination_info: research output from ResearcherAgent.

        Returns:
            Markdown-formatted hotel and restaurant recommendations.
        """
        destination = user_inputs.get("destination_city", "")
        budget = user_inputs.get("budget", "Mid-range")
        theme = user_inputs.get("travel_theme", "")
        activities = ", ".join(user_inputs.get("activities", []))
        duration = user_inputs.get("trip_duration", 7)

        prompt = HOTEL_RESTAURANT_PROMPT.format(
            destination=destination,
            budget=budget,
            theme=theme,
            activities=activities,
            duration=duration,
            destination_info=destination_info,
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as exc:
            return (
                f"⚠️ Hotel & Restaurant Agent encountered an error: {exc}\n\n"
                "Please check your GEMINI_API_KEY."
            )
