# Multi-Agent Travel Planner – AI-Based Intelligent Trip Planning System

**B.Tech CSE Final Year – AI Agent Development Laboratory Mini Project**

[![Python Version](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.14-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/framework-Flask%203.1-black)](https://flask.palletsprojects.com/)
[![Architecture](https://img.shields.io/badge/architecture-Multi--Agent%20System-emerald)](#6-multi-agent-architecture)
[![Status](https://img.shields.io/badge/build-passing-brightgreen)](#)

---

## 1. Project Title
**Multi-Agent Travel Planner – AI-Based Intelligent Trip Planning System**  
*“Plan your trip with the help of multiple AI agents.”*

---

## 2. Project Overview
The **Multi-Agent Travel Planner** is an intelligent, autonomous web application designed for a B.Tech CSE Final Year AI Agent Development laboratory mini project. Rather than relying on a single monolithic chatbot or prompt, the application demonstrates genuine **multi-agent coordination and specialization**: five purpose-built software agents collaborate to decompose travel requirements, research destinations, construct day-by-day itineraries, evaluate financial feasibility in Indian Rupees (INR), compile customized packing checklists, and enforce constraint validation.

The project features a **dual-mode AI engine**:
1. **Online LLM Engine:** Integrates with Google Gemini API (or OpenAI GPT) when an API key is provided.
2. **Deterministic Rule Engine (Offline/Viva Ready):** Operates 100% offline with zero external API dependencies, ensuring foolproof live demonstrations even during network outages in college laboratories.

---

## 3. Problem Statement
Traditional travel booking portals are fragmented, requiring users to manually cross-reference attraction blogs, map itineraries, calculate multi-category budgets, and remember packing essentials. Monolithic generative chatbots frequently produce hallucinated schedules, overlook financial budget constraints, or fail to structure daily activities logically.

There is a need for a modular, distributed AI system where specialized agents manage discrete cognitive sub-tasks and share structured information to synthesize a feasible, customized travel plan.

---

## 4. Objectives
- Demonstrate the principles of **Agent Specialization**, **Task Decomposition**, and **Inter-Agent Communication**.
- Provide a clean, student-friendly web interface with a live **Multi-Agent Coordination Dashboard**.
- Enforce strict constraint validation (matching user budget, trip length, and traveler preferences).
- Provide a beginner-friendly codebase in Python and Flask that is easy to explain during academic viva-voce examinations.

---

## 5. Features
- **One-Click Viva Demo:** Includes a pre-configured sample trip (Pune → Goa, 3 Days, 2 Travelers, ₹10,000, Budget Style, Beaches & Food) for instant demonstration.
- **Live Agent Execution Dashboard:** Visualizes agent states (`Queued` → `Processing` → `Completed`) with real elapsed execution timestamps.
- **Curated Destination Highlights:** Tailored recommendations matching traveler interests (Nature, Adventure, Beaches, History, Food, Shopping, Culture).
- **Day-by-Day Structured Schedule:** Realistic allocation of Morning, Afternoon, and Evening activities without repetition.
- **Categorized Budget Estimation:** Itemized breakdown for Accommodation, Food, Local Transport, Activities, and Miscellaneous with automated surplus/overrun calculation in Indian Rupees (INR `₹`).
- **Dynamic Cost-Saving Recommendations:** Automatically triggered whenever estimated expenses exceed user budget.
- **Interactive Packing Checklist:** Categorized into Essential Documents, Electronics, Clothing, Toiletries/Health, Destination Gear, and Useful Items with interactive checkable boxes and completion counters.
- **Plan Modification & Print/PDF Export:** Allows instant trip parameter tweaking or saving as a formatted PDF report.

---

## 6. Multi-Agent Architecture

```
                       ┌─────────────────────────┐
                       │       User Input        │
                       │ (Destination, Days,     │
                       │  Travelers, Budget,     │
                       │  Style, Interests)      │
                       └────────────┬────────────┘
                                    │
                                    ▼
                 ┌──────────────────────────────────────┐
                 │    Travel Coordinator Agent          │
                 │   - Input Validation & Cleaning      │
                 │   - Task Decomposition               │
                 └──────────────┬───────────────────────┘
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
        ▼                       ▼                       ▼
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│ Destination Agent│    │   Budget Agent   │    │ Essentials Agent │
│ - Curates Places │    │ - Calculates     │    │ - Packing Items  │
│ - Activity Match │    │   5-Cat Expenses │    │ - Safety Tips    │
└───────┬──────────┘    │ - Budget Check   │    └────────┬─────────┘
        │               └────────┬─────────┘             │
        │ [Recommended           │                       │
        │  Places]               │                       │
        ▼                        │                       │
┌──────────────────┐             │                       │
│ Itinerary Agent  │             │                       │
│ - Day-Wise Slots │             │                       │
│ - Morning/Aft/Eve│             │                       │
└───────┬──────────┘             │                       │
        │                        │                       │
        └────────────────────────┼───────────────────────┘
                                 │
                                 ▼
                 ┌──────────────────────────────────────┐
                 │     Coordinator Synthesis Agent      │
                 │   - Verify Constraint Consistency    │
                 │   - Validate Duration & Feasibility  │
                 │   - Assemble Final Travel Plan       │
                 └──────────────┬───────────────────────┘
                                │
                                ▼
                       ┌─────────────────────────┐
                       │    Final Travel Plan    │
                       │  (Dashboard + Result UI)│
                       └─────────────────────────┘
```

---

## 7. Agent Responsibilities

| Agent Name | Input Received | Core Responsibility | Output Produced |
| :--- | :--- | :--- | :--- |
| **Travel Coordinator Agent** | Complete User Form Data | Receives inputs, decomposes workflow, passes intermediate state between agents, validates day/budget constraints, and synthesizes the plan. | Complete Structured Travel Plan & Execution Logs |
| **Destination Agent** | Destination, Interests, Travel Style, Duration | Researches and recommends a manageable list of attractions and activities matching traveler interests. | List of places with names, categories, descriptions, and suggested activities |
| **Itinerary Agent** | Destination, Days, Recommended Places (from Destination Agent), Interests | Organizes curated places into balanced Day 1..N schedules across Morning, Afternoon, and Evening slots without repetition. | Day-by-day itinerary objects with time slots and activities |
| **Budget Agent** | Destination, Days, Travelers, Budget, Travel Style | Calculates itemized approximate expenses (Stay, Food, Transit, Activities, Misc) in INR and compares against user budget. | Itemized cost breakdown, total, surplus/deficit, and cost-saving suggestions |
| **Travel Essentials Agent**| Destination, Days, Travel Style, Interests | Compiles a customized packing list and practical local travel/safety advice. | 6 categorized checklists and destination-tailored travel tips |

---

## 8. Technology Stack
- **Backend:** Python 3.10+ / 3.14, Flask 3.1
- **Frontend:** Semantic HTML5, Vanilla CSS3 (Custom Design System, CSS Variables, Responsive Grid), Modern JavaScript (ES6+)
- **Icons & Typography:** Font Awesome 6.5, Google Fonts (*Outfit* and *Plus Jakarta Sans*)
- **AI Integration:** Google Gemini 1.5 Flash REST API / OpenAI GPT-4o-mini / Built-in Domain Rule Engine
- **Data Persistence:** In-memory session plan cache (Zero external database configuration required)

---

## 9. Project Directory Structure
```
multi_agent_travel_planner/
│
├── app.py                      # Flask server, route controllers, session handling
├── requirements.txt            # Python dependencies (flask, python-dotenv, requests)
├── test_app.py                 # Automated unit and integration test suite
├── README.md                   # Comprehensive academic documentation
├── .env.example                # Template for optional LLM API keys
│
├── agents/                     # Specialized AI Agent modules
│   ├── __init__.py             # Agent exports
│   ├── coordinator_agent.py    # Master coordinator & workflow orchestrator
│   ├── destination_agent.py    # Destination curator & activity matcher
│   ├── itinerary_agent.py      # Day-by-day schedule organizer
│   ├── budget_agent.py         # 5-category expense calculator & feasibility checker
│   └── essentials_agent.py     # Packing checklist & safety tips generator
│
├── templates/                  # HTML5 Templates
│   ├── index.html              # Landing page, feature cards, form, live dashboard
│   └── result.html             # Final synthesized travel plan and print view
│
├── static/                     # Frontend Assets
│   ├── style.css               # Modern responsive styling & design tokens
│   └── script.js               # Interactive form handling, sample auto-fill, DOM updates
│
└── utils/                      # Helper Utilities
    ├── __init__.py             # Package init
    ├── helpers.py              # INR currency formatting & input validation logic
    └── llm_service.py          # Modular AI caller with automatic fallback detection
```

---

## 10. Installation & Setup Instructions

### Prerequisites
- Python 3.10 or higher installed on your system.

### Step 1: Clone / Navigate to Project Directory
```bash
cd "c:\Users\adarsh\Desktop\AIAD_multiagent travel planner"
```

### Step 2: Install Required Dependencies
```bash
python -m pip install -r requirements.txt
```

*(Installed packages: `Flask>=3.0.0`, `python-dotenv>=1.0.0`, `requests>=2.31.0`)*

### Step 3: (Optional) Configure LLM API Key
If you wish to run with live Google Gemini AI, copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Open `.env` and set your key:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```
> **Note:** If no API key is set, the application will automatically run in **Intelligent Offline Mode** with full functionality!

---

## 11. How to Run the Project

### Run the Flask Application
```bash
python app.py
```
*(On Windows systems where `python` points to Microsoft Store, use: `& "C:\Users\<username>\AppData\Local\Programs\Python\Python314\python.exe" app.py`)*

### Access the Web Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 12. Testing the Project

An automated test suite is provided in [`test_app.py`](test_app.py). Run:
```bash
python test_app.py
```
This runs automated tests verifying:
1. `validate_trip_inputs` edge cases (min days, empty fields, negative budgets).
2. `format_inr` Indian numbering system conversions (`₹1,00,000`).
3. `TravelCoordinatorAgent` orchestration and inter-agent data passing.
4. Flask endpoints (`/`, `/health`, `/api/sample-trip`, `/api/plan-trip`, `/plan/result`).

---

## 13. Sample Input & Output Demonstration

### Sample Input
- **Starting City:** `Pune`
- **Destination:** `Goa`
- **Number of Days:** `3`
- **Number of Travelers:** `2`
- **Total Budget:** `₹10,000`
- **Travel Style:** `Budget`
- **Interests:** `Beaches`, `Food`, `Culture`

### Sample Output Summary
- **Recommended Places:** Baga & Calangute Beachfront, Aguada Fort & Portuguese Lighthouse, Basilica of Bom Jesus, Anjuna Coast, Fisherman's Wharf Seafood Trail, Fontainhas Latin Quarter, Chapora Fort.
- **Itinerary:**
  - *Day 1:* Arrival & Coastal Orientation (Morning: Baga Beach, Afternoon: Fisherman's Wharf, Evening: Aguada Fort sunset).
  - *Day 2:* Deep Cultural Heritage (Morning: Basilica of Bom Jesus, Afternoon: Fontainhas Latin Quarter, Evening: Chapora Fort).
  - *Day 3:* Markets & Leisure (Morning: Anjuna Flea Market, Afternoon: Calangute Beach, Evening: Farewell coastal dinner).
- **Budget Breakdown:**
  - Accommodation (2 nights): `₹2,400`
  - Food & Dining: `₹2,400`
  - Local Transport: `₹1,500`
  - Activities & Entry: `₹1,200`
  - Miscellaneous Buffer: `₹900`
  - **Estimated Total:** `₹8,400`
  - **Status:** *Within Budget* (Surplus: `₹1,600`)
- **Packing Checklist:** 24 items categorized with interactive checkboxes.
- **Travel Tips:** Tailored coastal advice on undertow safety, two-wheeler rentals, and cash availability for beach shacks.

---

## 14. Viva-Voce Questions & Explanations

### Q1: What makes this a "Multi-Agent System" instead of a standard chatbot?
**Answer:** A conventional chatbot processes a single unstructured prompt monolithically. In this project, the problem is explicitly decomposed into independent sub-domains managed by distinct agents (`DestinationAgent`, `ItineraryAgent`, `BudgetAgent`, `EssentialsAgent`) coordinated by `TravelCoordinatorAgent`. Information is structured (JSON/Python dictionaries) and passed sequentially (e.g., the `ItineraryAgent` strictly consumes the output of the `DestinationAgent`).

### Q2: How does the system handle budget constraint violations?
**Answer:** The `BudgetAgent` computes categorized costs based on traveler count, trip duration, and travel style. It compares the sum against the user's budget. If `estimated_total > user_budget`, the status switches to `Exceeded Budget`, and the agent automatically generates specific cost-cutting recommendations (e.g., switching from standard hotels to homestays, or choosing public transit).

### Q3: How is offline resilience achieved?
**Answer:** The LLM integration in `utils/llm_service.py` is modular. When an API key is missing or network connectivity drops, each agent seamlessly falls back to an intelligent rule-based knowledge base without throwing unhandled exceptions.

---

## 15. Future Scope
- Integration with live OpenStreetMap or Mapbox APIs for interactive route plotting.
- Real-time weather forecasting API integration to dynamically adjust outdoor vs indoor day plans.
- Multi-currency conversion for international travel destinations.
- Integration of a vector database (RAG) for localized travel reviews and hidden spots.

---

## 16. Academic Declaration
This mini-project was developed in fulfillment of the requirements for the **B.Tech Computer Science & Engineering Final Year AI Agent Development Laboratory**.
