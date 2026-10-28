"""
Budget Agent:
Specialized AI Agent responsible for estimating realistic travel expenses
across 5 key categories (Accommodation, Food, Local Transport, Activities, Miscellaneous),
comparing total against user's budget, and offering practical cost-saving alternatives.
"""

import math
from utils.helpers import format_inr
from utils.llm_service import query_llm

class BudgetAgent:
    def __init__(self):
        self.name = "Budget Agent"
        self.description = "Estimates categorized travel expenses, compares with budget, and suggests cost-saving adjustments."

    def estimate_budget(self, destination: str, days: int, travelers: int, budget: float, travel_style: str = "Standard") -> dict:
        """
        Estimates breakdown and compares with user budget.
        """
        # 1. Attempt LLM Estimation if configured
        prompt = f"""
You are a financial travel planning agent.
Destination: {destination}
Trip Length: {days} days
Number of Travelers: {travelers}
User Budget: INR {budget}
Travel Style: {travel_style}

Calculate realistic approximate expenses in Indian Rupees (INR) for:
1. accommodation
2. food
3. transport
4. activities
5. miscellaneous

Compare total with user budget. If estimated total > budget, provide 2-3 specific cost-saving tips.
Return strictly valid JSON matching:
{{
  "accommodation": 4000,
  "food": 2500,
  "transport": 1500,
  "activities": 1200,
  "miscellaneous": 800,
  "cost_saving_suggestions": ["Tip 1", "Tip 2"]
}}
"""
        system_instruction = "You are a travel finance calculator. Return strictly JSON with numeric integer values for costs."
        llm_response = query_llm(prompt, system_instruction=system_instruction, json_format=True)

        if llm_response and isinstance(llm_response, dict) and "accommodation" in llm_response:
            try:
                acc = float(llm_response.get("accommodation", 0))
                food = float(llm_response.get("food", 0))
                trans = float(llm_response.get("transport", 0))
                act = float(llm_response.get("activities", 0))
                misc = float(llm_response.get("miscellaneous", 0))
                tips = llm_response.get("cost_saving_suggestions", [])
                
                est_total = acc + food + trans + act + misc
                if est_total > 0:
                    return self._package_result(acc, food, trans, act, misc, est_total, budget, tips)
            except Exception as e:
                print(f"[BudgetAgent] Error parsing LLM response: {e}")

        # 2. Rule-Based Calculation Engine
        return self._calculate_rule_based_budget(destination, days, travelers, budget, travel_style)

    def _calculate_rule_based_budget(self, destination: str, days: int, travelers: int, budget: float, travel_style: str) -> dict:
        """Calculates realistic tiered estimates based on travel style and travelers."""
        rooms_needed = math.ceil(travelers / 2)  # assuming double occupancy

        # Cost matrices per traveler / room in INR
        style = travel_style.capitalize()
        if style == "Budget":
            nightly_room_rate = 1200
            daily_food_per_person = 400
            daily_transit_per_person = 250
            daily_activities_per_person = 200
            daily_misc_per_person = 150
        elif style == "Premium":
            nightly_room_rate = 5500
            daily_food_per_person = 1800
            daily_transit_per_person = 1200
            daily_activities_per_person = 1000
            daily_misc_per_person = 600
        else:  # Standard
            nightly_room_rate = 2600
            daily_food_per_person = 800
            daily_transit_per_person = 500
            daily_activities_per_person = 450
            daily_misc_per_person = 300

        # Nights count is usually (days - 1) or at least 1 night
        nights = max(1, days - 1) if days > 1 else 1

        accommodation = nightly_room_rate * rooms_needed * nights
        food = daily_food_per_person * travelers * days
        transport = daily_transit_per_person * travelers * days
        activities = daily_activities_per_person * travelers * days
        miscellaneous = daily_misc_per_person * travelers * days

        estimated_total = accommodation + food + transport + activities + miscellaneous

        # Generate cost-saving suggestions if over budget
        cost_saving_suggestions = []
        if estimated_total > budget:
            diff = estimated_total - budget
            cost_saving_suggestions.append(f"Estimated costs exceed your target budget by {format_inr(diff)}.")
            cost_saving_suggestions.append("Accommodation: Consider verified hostels, guesthouses, or homestays instead of standard hotels.")
            cost_saving_suggestions.append("Local Commute: Rent shared two-wheelers/scooters or use metro/public buses instead of private cabs.")
            cost_saving_suggestions.append("Dining: Enjoy authentic regional street food stalls and local thali joints over fine-dining venues.")
            cost_saving_suggestions.append("Activities: Prioritize free public beaches, viewpoints, and open heritage spots.")
        else:
            savings = budget - estimated_total
            cost_saving_suggestions.append(f"Great job! Your trip plan is comfortably within budget with a surplus of {format_inr(savings)}.")
            cost_saving_suggestions.append("You have room for special souvenir shopping, water sports, or a celebratory rooftop dinner.")

        return self._package_result(
            accommodation, food, transport, activities, miscellaneous,
            estimated_total, budget, cost_saving_suggestions
        )

    def _package_result(self, acc, food, trans, act, misc, total, budget, tips):
        diff = total - budget
        is_over = diff > 0

        return {
            "accommodation": round(acc, 2),
            "food": round(food, 2),
            "transport": round(trans, 2),
            "activities": round(act, 2),
            "miscellaneous": round(misc, 2),
            "estimated_total": round(total, 2),
            "user_budget": round(budget, 2),
            "difference": round(abs(diff), 2),
            "is_over_budget": is_over,
            "status": "Exceeded Budget" if is_over else "Within Budget",
            "cost_saving_suggestions": tips,
            "formatted": {
                "accommodation": format_inr(acc),
                "food": format_inr(food),
                "transport": format_inr(trans),
                "activities": format_inr(act),
                "miscellaneous": format_inr(misc),
                "estimated_total": format_inr(total),
                "user_budget": format_inr(budget),
                "difference": format_inr(abs(diff)),
                "difference_label": f"+{format_inr(diff)} Over" if is_over else f"+{format_inr(abs(diff))} Surplus"
            }
        }