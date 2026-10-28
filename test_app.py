"""
Automated Integration Test for Multi-Agent Travel Planner
Tests all 5 agents, helpers, and Flask routes.
"""

import sys
if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except AttributeError:
        pass

from app import app
from utils.helpers import format_inr, validate_trip_inputs
from agents.coordinator_agent import TravelCoordinatorAgent

def test_helpers():
    print("Testing Helpers...")
    assert format_inr(1000) == "₹1,000", f"Expected ₹1,000, got {format_inr(1000)}"
    assert format_inr(10000) == "₹10,000", f"Expected ₹10,000, got {format_inr(10000)}"
    assert format_inr(100000) == "₹1,00,000", f"Expected ₹1,00,000, got {format_inr(100000)}"
    
    # Validation test
    valid, err, cleaned = validate_trip_inputs({
        "starting_city": "Pune",
        "destination": "Goa",
        "days": "3",
        "travelers": "2",
        "budget": "10000",
        "travel_style": "Budget",
        "interests": ["Beaches", "Food"]
    })
    assert valid is True, f"Validation failed: {err}"
    assert cleaned["days"] == 3
    assert cleaned["budget"] == 10000.0
    print("✓ Helpers passed.")

def test_multi_agent_coordination():
    print("Testing TravelCoordinatorAgent...")
    coordinator = TravelCoordinatorAgent()
    req = {
        "starting_city": "Pune",
        "destination": "Goa",
        "days": 3,
        "travelers": 2,
        "budget": 10000.0,
        "travel_style": "Budget",
        "interests": ["Beaches", "Food"]
    }
    plan = coordinator.coordinate_trip_planning(req)
    assert "recommended_places" in plan and len(plan["recommended_places"]) > 0
    assert "itinerary" in plan and len(plan["itinerary"]) == 3
    assert "budget_breakdown" in plan
    assert "travel_essentials" in plan
    assert "execution_logs" in plan and len(plan["execution_logs"]) >= 5
    print(f"✓ Coordinator passed. Produced {len(plan['recommended_places'])} places, {len(plan['itinerary'])} days, Total: {plan['budget_breakdown']['formatted']['estimated_total']}.")

def test_flask_routes():
    print("Testing Flask Routes...")
    client = app.test_client()
    
    # 1. GET /
    res = client.get("/")
    assert res.status_code == 200, f"GET / returned {res.status_code}"
    assert b"Multi-Agent Travel Planner" in res.data
    
    # 2. GET /health
    res = client.get("/health")
    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "healthy"
    assert len(data["agents_loaded"]) == 5
    
    # 3. GET /api/sample-trip
    res = client.get("/api/sample-trip")
    assert res.status_code == 200
    assert res.get_json()["destination"] == "Goa"
    
    # 4. POST /api/plan-trip (JSON API)
    res = client.post("/api/plan-trip", json={
        "starting_city": "Pune",
        "destination": "Goa",
        "days": 3,
        "travelers": 2,
        "budget": 10000,
        "travel_style": "Budget",
        "interests": ["Beaches", "Food"]
    })
    assert res.status_code == 200
    api_json = res.get_json()
    assert api_json["success"] is True
    assert "plan" in api_json
    
    # 5. GET /plan/result
    res = client.get("/plan/result")
    assert res.status_code == 200
    assert b"Goa" in res.data
    assert b"Day-by-Day Itinerary" in res.data
    assert b"Estimated Budget Breakdown" in res.data
    
    print("✓ All Flask routes passed successfully!")

if __name__ == "__main__":
    test_helpers()
    test_multi_agent_coordination()
    test_flask_routes()
    print("\nALL AUTOMATED TESTS PASSED SUCCESSFULLY! (100% OK)")
