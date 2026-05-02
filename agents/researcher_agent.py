"""
Researcher Agent
Collects destination information including attractions, culture, climate,
and activities matching user preferences using Gemini AI.
"""

import os
import google.generativeai as genai
from utils.prompts import RESEARCHER_SYSTEM_PROMPT, TRAVEL_TIPS_PROMPT


class ResearcherAgent:
    """
    Gemini-powered agent that researches the destination and
    returns structured information about attractions, climate,
    culture, and activities.
    """

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "GEMINI_API_KEY environment variable is not set. "
                "Please add it to your .env file."
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 2048,
            },
        )

    def research(self, user_inputs: dict) -> str:
        """
        Research the destination and return a detailed information string.

        Args:
            user_inputs: dict with keys departure_city, destination_city,
                         trip_duration, budget, travel_theme, activities.

        Returns:
            Markdown-formatted string with destination research.
        """
        destination = user_inputs.get("destination_city", "")
        theme = user_inputs.get("travel_theme", "")
        activities = ", ".join(user_inputs.get("activities", []))
        duration = user_inputs.get("trip_duration", 7)
        budget = user_inputs.get("budget", "Mid-range")

        prompt = RESEARCHER_SYSTEM_PROMPT.format(
            destination=destination,
            theme=theme,
            activities=activities,
            duration=duration,
            budget=budget,
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as exc:
            return (
                f"⚠️ Research Agent encountered an error: {exc}\n\n"
                f"Please verify your GEMINI_API_KEY and network connection."
            )

    def get_travel_tips(self, user_inputs: dict) -> str:
        """
        Generate travel tips for the destination.

        Args:
            user_inputs: dict containing destination_city, travel_theme, budget.

        Returns:
            HTML-formatted travel tips string.
        """
        destination = user_inputs.get("destination_city", "")
        budget = user_inputs.get("budget", "Mid-range")
        theme = user_inputs.get("travel_theme", "")

        prompt = TRAVEL_TIPS_PROMPT.format(
            destination=destination,
            budget=budget,
            theme=theme,
        )

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as exc:
            return f"⚠️ Could not fetch travel tips: {exc}"
