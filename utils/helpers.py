"""
Helper utilities for Multi-Agent Travel Planner.
Includes currency formatting (Indian Rupee), input validation, and sanitization.
"""

def format_inr(amount):
    """
    Format a numeric amount into Indian Rupee representation (e.g. 100000 -> ₹1,00,000).
    Follows the Indian numbering system (3 digits, then groups of 2 digits).
    """
    try:
        val = int(round(float(amount)))
    except (ValueError, TypeError):
        return "₹0"
    
    is_negative = val < 0
    val_str = str(abs(val))
    
    if len(val_str) <= 3:
        formatted = val_str
    else:
        last_three = val_str[-3:]
        remaining = val_str[:-3]
        groups = []
        while len(remaining) > 2:
            groups.insert(0, remaining[-2:])
            remaining = remaining[:-2]
        if remaining:
            groups.insert(0, remaining)
        formatted = ",".join(groups) + "," + last_three
        
    prefix = "-₹" if is_negative else "₹"
    return f"{prefix}{formatted}"


def validate_trip_inputs(data):
    """
    Validate user inputs from the trip planning form.
    Returns: (is_valid: bool, error_message: str or None, cleaned_data: dict)
    """
    errors = []
    
    # 1. Starting City
    starting_city = str(data.get("starting_city", "")).strip()
    if not starting_city:
        errors.append("Starting city is required.")
    elif len(starting_city) < 2 or len(starting_city) > 50:
        errors.append("Starting city must be between 2 and 50 characters.")
        
    # 2. Destination
    destination = str(data.get("destination", "")).strip()
    if not destination:
        errors.append("Destination is required.")
    elif len(destination) < 2 or len(destination) > 50:
        errors.append("Destination must be between 2 and 50 characters.")
        
    # 3. Number of Days
    try:
        days = int(data.get("days", 0))
        if days < 1:
            errors.append("Number of days must be at least 1.")
        elif days > 30:
            errors.append("Number of days cannot exceed 30.")
    except (ValueError, TypeError):
        errors.append("Number of days must be a valid integer.")
        days = 1

    # 4. Number of Travelers
    try:
        travelers = int(data.get("travelers", 0))
        if travelers < 1:
            errors.append("Number of travelers must be at least 1.")
        elif travelers > 50:
            errors.append("Number of travelers cannot exceed 50.")
    except (ValueError, TypeError):
        errors.append("Number of travelers must be a valid integer.")
        travelers = 1

    # 5. Total Budget
    try:
        budget = float(data.get("budget", 0))
        if budget < 500:
            errors.append("Total budget must be at least ₹500.")
        elif budget > 10000000:
            errors.append("Total budget exceeds maximum allowed limit.")
    except (ValueError, TypeError):
        errors.append("Budget must be a valid numeric amount.")
        budget = 0.0

    # 6. Travel Style
    travel_style = str(data.get("travel_style", "Standard")).strip().capitalize()
    if travel_style not in ["Budget", "Standard", "Premium"]:
        travel_style = "Standard"

    # 7. Interests
    raw_interests = data.get("interests", [])
    if isinstance(raw_interests, str):
        # Could be comma-separated or JSON string
        if raw_interests.startswith("[") and raw_interests.endswith("]"):
            import json
            try:
                raw_interests = json.loads(raw_interests)
            except Exception:
                raw_interests = [i.strip() for i in raw_interests.strip("[]").split(",") if i.strip()]
        else:
            raw_interests = [i.strip() for i in raw_interests.split(",") if i.strip()]
    elif not isinstance(raw_interests, list):
        raw_interests = []
        
    valid_interests_map = {
        "nature": "Nature",
        "adventure": "Adventure",
        "beaches": "Beaches",
        "history": "History",
        "food": "Food",
        "shopping": "Shopping",
        "culture": "Culture"
    }
    
    cleaned_interests = []
    for item in raw_interests:
        norm = str(item).strip().lower()
        if norm in valid_interests_map:
            cleaned_interests.append(valid_interests_map[norm])
            
    if not cleaned_interests:
        cleaned_interests = ["Culture", "Food"]  # sensible default if none chosen

    cleaned_data = {
        "starting_city": starting_city,
        "destination": destination,
        "days": days,
        "travelers": travelers,
        "budget": round(budget, 2),
        "travel_style": travel_style,
        "interests": cleaned_interests
    }
    
    if errors:
        return False, " | ".join(errors), cleaned_data
    return True, None, cleaned_data
