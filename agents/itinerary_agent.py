"""
Itinerary Agent:
Specialized AI Agent responsible for creating a realistic day-by-day itinerary.
Consumes the curated places provided by the Destination Agent and arranges them
into balanced morning, afternoon, and evening activity slots.
"""

import json
from utils.llm_service import query_llm

class ItineraryAgent:
    def __init__(self):
        self.name = "Itinerary Agent"
        self.description = "Organizes recommended attractions into a balanced day-by-day schedule with morning, afternoon, and evening slots."

    def build_itinerary(self, destination: str, days: int, recommended_places: list, interests: list, travel_style: str = "Standard") -> list:
        """
        Builds a structured day-by-day plan.
        Returns: list of day dicts:
        [
          {
            "day": 1,
            "theme": "Day Theme/Title",
            "morning": {"time": "...", "place": "...", "activity": "..."},
            "afternoon": {"time": "...", "place": "...", "activity": "..."},
            "evening": {"time": "...", "place": "...", "activity": "..."}
          }, ...
        ]
        """
        # 1. Attempt LLM Generation if configured
        places_summary = "\n".join([f"- {p.get('name')}: {p.get('description')} ({p.get('suggested_activity')})" for p in recommended_places])
        prompt = f"""
You are an expert itinerary scheduling agent.
Create a structured {days}-day itinerary for a trip to {destination}.
Travel Style: {travel_style}
Interests: {', '.join(interests)}
Recommended Places to include:
{places_summary}

Organize each day into "morning", "afternoon", and "evening" slots. Avoid repetition.
Return strictly valid JSON with key "itinerary" as an array of objects matching:
{{
  "itinerary": [
    {{
      "day": 1,
      "theme": "Short Catchy Theme for the day",
      "morning": {{
        "time": "09:00 AM - 12:30 PM",
        "place": "Place Name",
        "activity": "Concrete activity description"
      }},
      "afternoon": {{
        "time": "01:30 PM - 04:30 PM",
        "place": "Place Name",
        "activity": "Concrete activity description"
      }},
      "evening": {{
        "time": "05:30 PM - 08:30 PM",
        "place": "Place Name",
        "activity": "Concrete activity description"
      }}
    }}
  ]
}}
"""
        system_instruction = "You are a professional travel planner. Respond strictly with valid JSON."
        llm_response = query_llm(prompt, system_instruction=system_instruction, json_format=True)

        if llm_response and isinstance(llm_response, dict) and "itinerary" in llm_response:
            itin = llm_response["itinerary"]
            if isinstance(itin, list) and len(itin) == days:
                return itin

        # 2. Rule-Based Fallback Engine
        return self._generate_fallback_itinerary(destination, days, recommended_places, interests, travel_style)

    def _generate_fallback_itinerary(self, destination: str, days: int, places: list, interests: list, travel_style: str) -> list:
        """
        Generates a balanced, non-repetitive schedule using available recommended places
        and contextual time slots.
        """
        itinerary = []
        if not places:
            places = [
                {"name": f"{destination} City Exploration", "suggested_activity": "Sightseeing and local walking tour"},
                {"name": f"{destination} Heritage Quarter", "suggested_activity": "Visiting historic monuments"},
                {"name": f"{destination} Food Market", "suggested_activity": "Sampling traditional regional dishes"}
            ]

        place_index = 0
        total_places = len(places)

        themes = [
            "Arrival, Scenic Orientation & Local Flavors",
            "Deep Cultural Heritage & Signature Landmarks",
            "Nature Trails, Coastal Vistas & Leisure",
            "Artisanal Markets, Local Crafts & Food Trail",
            "Offbeat Escapes & Scenic Viewpoints",
            "Hidden Gems, Relaxation & Souvenir Gathering",
            "Farewell Vistas & Memorable Highlights"
        ]

        time_slots = {
            "morning": "09:00 AM - 12:30 PM",
            "afternoon": "01:30 PM - 04:30 PM",
            "evening": "05:30 PM - 08:30 PM"
        }

        for day_num in range(1, days + 1):
            theme = themes[(day_num - 1) % len(themes)]
            
            # Slot 1: Morning
            p_morning = places[place_index % total_places]
            place_index += 1
            
            # Slot 2: Afternoon
            p_afternoon = places[place_index % total_places]
            place_index += 1
            
            # Slot 3: Evening
            p_evening = places[place_index % total_places]
            place_index += 1

            # Build descriptive activities
            m_act = p_morning.get("suggested_activity") or f"Explore {p_morning.get('name')} in the morning freshness."
            if day_num == 1:
                m_act = f"Hotel check-in & morning orientation. Head over to {p_morning.get('name')} to begin your trip."

            a_act = p_afternoon.get("suggested_activity") or f"Visit {p_afternoon.get('name')} followed by regional dining."
            
            e_act = p_evening.get("suggested_activity") or f"Unwind at {p_evening.get('name')} and soak in sunset views."
            if day_num == days and days > 1:
                e_act = f"Sunset moments at {p_evening.get('name')} followed by a celebratory farewell dinner."

            day_plan = {
                "day": day_num,
                "theme": theme,
                "morning": {
                    "time": time_slots["morning"],
                    "place": p_morning.get("name"),
                    "activity": m_act
                },
                "afternoon": {
                    "time": time_slots["afternoon"],
                    "place": p_afternoon.get("name"),
                    "activity": a_act
                },
                "evening": {
                    "time": time_slots["evening"],
                    "place": p_evening.get("name"),
                    "activity": e_act
                }
            }
            itinerary.append(day_plan)

        return itinerary
