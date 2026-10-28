"""
Travel Coordinator Agent:
The Master Orchestrator Agent responsible for:
1. Receiving and validating user trip parameters.
2. Decomposing the planning problem into sub-tasks for specialized agents.
3. Managing sequential/parallel agent information flow (passing Destination Agent outputs to Itinerary Agent).
4. Collecting all sub-agent outputs.
5. Validating constraints (trip duration vs itinerary days, budget feasibility).
6. Synthesizing the final comprehensive Travel Plan.
"""

import time
from .destination_agent import DestinationAgent
from .itinerary_agent import ItineraryAgent
from .budget_agent import BudgetAgent
from .essentials_agent import TravelEssentialsAgent
from utils.helpers import format_inr
from utils.llm_service import get_llm_status

class TravelCoordinatorAgent:
    def __init__(self):
        self.name = "Travel Coordinator Agent"
        self.description = "Central coordinator that decomposes planning tasks, delegates to specialized agents, and synthesizes the final itinerary."
        
        # Instantiate child specialized agents
        self.destination_agent = DestinationAgent()
        self.itinerary_agent = ItineraryAgent()
        self.budget_agent = BudgetAgent()
        self.essentials_agent = TravelEssentialsAgent()

    def coordinate_trip_planning(self, user_requirements: dict) -> dict:
        """
        Execute multi-agent coordination workflow.
        Returns a complete structured travel plan object including execution metadata.
        """
        start_time = time.time()
        execution_logs = []

        def log_step(agent_name: str, status: str, detail: str):
            execution_logs.append({
                "agent": agent_name,
                "status": status,
                "detail": detail,
                "timestamp": round(time.time() - start_time, 3)
            })

        # Step 1: Coordinator initialization and task decomposition
        log_step(
            self.name,
            "In Progress",
            f"Received travel request for {user_requirements.get('destination')} ({user_requirements.get('days')} days, {user_requirements.get('travelers')} travelers). Decomposing planning tasks."
        )

        destination = user_requirements.get("destination")
        starting_city = user_requirements.get("starting_city")
        days = user_requirements.get("days", 3)
        travelers = user_requirements.get("travelers", 2)
        budget = user_requirements.get("budget", 10000.0)
        travel_style = user_requirements.get("travel_style", "Standard")
        interests = user_requirements.get("interests", ["Culture", "Food"])

        # Step 2: Delegate to Destination Agent
        log_step(
            self.destination_agent.name,
            "In Progress",
            f"Analyzing destination '{destination}' for interests: {', '.join(interests)}."
        )
        recommended_places = self.destination_agent.recommend_places(
            destination=destination,
            interests=interests,
            travel_style=travel_style,
            days=days
        )
        log_step(
            self.destination_agent.name,
            "Completed",
            f"Successfully curated {len(recommended_places)} attractions and activities."
        )

        # Step 3: Delegate to Itinerary Agent (Information sharing: receives recommended_places)
        log_step(
            self.itinerary_agent.name,
            "In Progress",
            f"Constructing {days}-day scheduled itinerary using {len(recommended_places)} recommended places."
        )
        itinerary = self.itinerary_agent.build_itinerary(
            destination=destination,
            days=days,
            recommended_places=recommended_places,
            interests=interests,
            travel_style=travel_style
        )
        log_step(
            self.itinerary_agent.name,
            "Completed",
            f"Generated structured schedule covering {len(itinerary)} days across Morning, Afternoon, and Evening slots."
        )

        # Step 4: Delegate to Budget Agent
        log_step(
            self.budget_agent.name,
            "In Progress",
            f"Estimating categorized travel costs for {travelers} travelers over {days} days against budget {format_inr(budget)}."
        )
        budget_report = self.budget_agent.estimate_budget(
            destination=destination,
            days=days,
            travelers=travelers,
            budget=budget,
            travel_style=travel_style
        )
        budget_status_msg = "Within Budget" if not budget_report.get("is_over_budget") else "Exceeds Target Budget (Adjustments Suggested)"
        log_step(
            self.budget_agent.name,
            "Completed",
            f"Budget estimated: Total {budget_report['formatted']['estimated_total']} ({budget_status_msg})."
        )

        # Step 5: Delegate to Travel Essentials Agent
        log_step(
            self.essentials_agent.name,
            "In Progress",
            f"Drafting packing list, documentation checklist, and safety tips for {destination}."
        )
        essentials_report = self.essentials_agent.generate_essentials(
            destination=destination,
            days=days,
            travel_style=travel_style,
            interests=interests
        )
        total_checklist_items = sum(len(items) for items in essentials_report.get("checklist", {}).values())
        log_step(
            self.essentials_agent.name,
            "Completed",
            f"Compiled {total_checklist_items} checklist items and {len(essentials_report.get('travel_tips', []))} travel tips."
        )

        # Step 6: Coordinator validation and final synthesis
        log_step(
            self.name,
            "In Progress",
            "Validating agent consistency, constraints, and synthesizing final Travel Plan."
        )

        # Constraint check: Day count verification
        days_consistent = len(itinerary) == days
        
        # Budget check summary
        budget_variance = budget_report.get("difference", 0)
        is_over_budget = budget_report.get("is_over_budget", False)
        
        if is_over_budget:
            coordinator_assessment = (
                f"The planned trip to {destination} is feasible, but the estimated cost of "
                f"{budget_report['formatted']['estimated_total']} exceeds your allocated budget of "
                f"{format_inr(budget)} by {format_inr(budget_variance)}. Please review the cost-saving "
                f"alternatives suggested by the Budget Agent below."
            )
        else:
            coordinator_assessment = (
                f"Your trip to {destination} has been successfully planned! The estimated total expense is "
                f"{budget_report['formatted']['estimated_total']}, staying safely within your budget of "
                f"{format_inr(budget)} with a healthy surplus of {format_inr(budget_variance)}."
            )

        total_duration = round(time.time() - start_time, 2)
        log_step(
            self.name,
            "Completed",
            f"Travel Plan finalized and validated in {total_duration}s."
        )

        llm_active, provider_name = get_llm_status()

        final_plan = {
            "metadata": {
                "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "execution_time_seconds": total_duration,
                "ai_engine": provider_name,
                "llm_active": llm_active,
                "days_validated": days_consistent
            },
            "trip_overview": {
                "starting_city": starting_city,
                "destination": destination,
                "days": days,
                "travelers": travelers,
                "budget": budget,
                "budget_formatted": format_inr(budget),
                "travel_style": travel_style,
                "interests": interests
            },
            "coordinator_assessment": coordinator_assessment,
            "execution_logs": execution_logs,
            "recommended_places": recommended_places,
            "itinerary": itinerary,
            "budget_breakdown": budget_report,
            "travel_essentials": essentials_report.get("checklist", {}),
            "travel_tips": essentials_report.get("travel_tips", [])
        }

        return final_plan
