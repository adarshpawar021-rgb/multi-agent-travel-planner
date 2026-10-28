"""
Multi-Agent Travel Planner – AI-Based Intelligent Trip Planning System
Main Flask Application

Final Year B.Tech CSE Mini-Project
Demonstrating Multi-Agent Coordination, Specialization, and Task Decomposition.
"""

import sys
import os
import json

# Ensure UTF-8 output on Windows consoles to gracefully support INR symbol (₹)
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from agents.coordinator_agent import TravelCoordinatorAgent
from utils.helpers import validate_trip_inputs, format_inr
from utils.llm_service import get_llm_status

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "multi-agent-travel-planner-secret-key-2026")

# Instantiate the Master Coordinator Agent
coordinator = TravelCoordinatorAgent()

import uuid

# In-memory plan storage (avoids exceeding 4KB browser cookie limit while keeping app zero-database)
PLAN_CACHE = {}

def get_session_key():
    """Ensure a unique session identifier exists in the cookie."""
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return session["session_id"]

@app.route("/")
def index():
    """
    Landing page: features overview, project objectives, and trip planning form.
    Supports pre-filling when navigated from 'Modify Trip'.
    """
    prefill = session.get("last_inputs", None)
    llm_active, provider_name = get_llm_status()
    
    return render_template(
        "index.html",
        prefill=prefill,
        llm_active=llm_active,
        provider_name=provider_name
    )


@app.route("/plan", methods=["POST"])
def plan_trip_form():
    """
    Standard HTML Form submission endpoint.
    Validates inputs, triggers the Coordinator Agent, and renders the result view.
    """
    raw_data = {
        "starting_city": request.form.get("starting_city", ""),
        "destination": request.form.get("destination", ""),
        "days": request.form.get("days", ""),
        "travelers": request.form.get("travelers", ""),
        "budget": request.form.get("budget", ""),
        "travel_style": request.form.get("travel_style", "Standard"),
        "interests": request.form.getlist("interests")
    }

    is_valid, error_msg, cleaned_data = validate_trip_inputs(raw_data)
    if not is_valid:
        flash(error_msg, "danger")
        session["last_inputs"] = raw_data
        return redirect(url_for("index"))

    session_id = get_session_key()
    session["last_inputs"] = cleaned_data

    # Execute Multi-Agent Workflow
    try:
        plan = coordinator.coordinate_trip_planning(cleaned_data)
        PLAN_CACHE[session_id] = plan
        return render_template("result.html", plan=plan)
    except Exception as e:
        flash(f"An unexpected error occurred while planning your trip: {str(e)}", "danger")
        return redirect(url_for("index"))


@app.route("/api/plan-trip", methods=["POST"])
def api_plan_trip():
    """
    Asynchronous JSON API endpoint for interactive frontend with live agent status updates.
    """
    try:
        data = request.get_json(force=True) if request.is_json else request.form.to_dict()
    except Exception:
        data = request.form.to_dict()

    is_valid, error_msg, cleaned_data = validate_trip_inputs(data)
    if not is_valid:
        return jsonify({"success": False, "error": error_msg}), 400

    session_id = get_session_key()
    session["last_inputs"] = cleaned_data

    try:
        plan = coordinator.coordinate_trip_planning(cleaned_data)
        PLAN_CACHE[session_id] = plan
        return jsonify({"success": True, "plan": plan})
    except Exception as e:
        return jsonify({"success": False, "error": f"Agent execution failure: {str(e)}"}), 500


@app.route("/api/sample-trip")
def get_sample_trip():
    """
    Returns pre-configured sample trip dataset (Pune to Goa, 3 days, 2 travelers, ₹10,000)
    for rapid academic viva demonstration.
    """
    sample = {
        "starting_city": "Pune",
        "destination": "Goa",
        "days": 3,
        "travelers": 2,
        "budget": 10000,
        "travel_style": "Budget",
        "interests": ["Beaches", "Food", "Culture"]
    }
    return jsonify(sample)


@app.route("/plan/result")
def show_result():
    """
    Direct view to display the most recently generated plan.
    """
    session_id = get_session_key()
    plan = PLAN_CACHE.get(session_id)
    if not plan and PLAN_CACHE:
        # Fallback to the latest generated plan in memory
        plan = list(PLAN_CACHE.values())[-1]
        
    if not plan:
        flash("No active travel plan found. Please plan a new trip.", "info")
        return redirect(url_for("index"))
    return render_template("result.html", plan=plan)


@app.route("/health")
def health():
    """System health and agent readiness check."""
    llm_active, provider_name = get_llm_status()
    return jsonify({
        "status": "healthy",
        "project": "Multi-Agent Travel Planner",
        "agents_loaded": [
            coordinator.name,
            coordinator.destination_agent.name,
            coordinator.itinerary_agent.name,
            coordinator.budget_agent.name,
            coordinator.essentials_agent.name
        ],
        "ai_engine": provider_name,
        "llm_active": llm_active
    })


if __name__ == "__main__":
    port = int(os.environ.get("FLASK_PORT", 5000))
    print(f"\n=======================================================")
    print(f" Multi-Agent Travel Planner – Intelligent Trip System")
    print(f" Academic Mini-Project for AI Agent Development Lab")
    print(f" Running at: http://127.0.0.1:{port}")
    print(f"=======================================================\n")
    app.run(host="0.0.0.0", port=port, debug=True)
