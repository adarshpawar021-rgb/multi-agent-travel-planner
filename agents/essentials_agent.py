"""
Travel Essentials Agent:
Specialized AI Agent responsible for generating personalized packing checklists
(documents, electronics, clothing, toiletries/health, destination-specific items)
and actionable practical travel tips tailored to destination, climate, and travel style.
"""

from utils.llm_service import query_llm

class TravelEssentialsAgent:
    def __init__(self):
        self.name = "Travel Essentials Agent"
        self.description = "Prepares tailored packing checklists, essential document guides, and safety/travel tips."

    def generate_essentials(self, destination: str, days: int, travel_style: str = "Standard", interests: list = None) -> dict:
        """
        Generates categorized checklist and travel tips.
        """
        if interests is None:
            interests = []

        # 1. Attempt LLM Generation if configured
        prompt = f"""
You are a travel preparation and safety specialist.
Destination: {destination}
Duration: {days} days
Travel Style: {travel_style}
Interests: {', '.join(interests)}

Generate a personalized travel packing checklist and practical destination travel tips.
Checklist must include categories:
- documents
- electronics
- clothing
- toiletries_and_health
- destination_specific
- useful_items

Return strictly valid JSON matching:
{{
  "checklist": {{
    "documents": ["item 1", "item 2"],
    "electronics": ["item 1", "item 2"],
    "clothing": ["item 1", "item 2"],
    "toiletries_and_health": ["item 1", "item 2"],
    "destination_specific": ["item 1", "item 2"],
    "useful_items": ["item 1", "item 2"]
  }},
  "travel_tips": [
    "Practical tip 1",
    "Practical tip 2",
    "Practical tip 3",
    "Practical tip 4"
  ]
}}
"""
        system_instruction = "You are an expert travel packing and safety consultant. Return strictly valid JSON."
        llm_response = query_llm(prompt, system_instruction=system_instruction, json_format=True)

        if llm_response and isinstance(llm_response, dict) and "checklist" in llm_response and "travel_tips" in llm_response:
            return llm_response

        # 2. Rule-Based Fallback Generator
        return self._generate_fallback_essentials(destination, days, travel_style, interests)

    def _generate_fallback_essentials(self, destination: str, days: int, travel_style: str, interests: list) -> dict:
        """Domain-driven rule generator for packing checklists and travel advice."""
        dest_lower = destination.lower()
        interests_lower = [i.lower() for i in interests]

        # Base items common to all travelers
        documents = [
            "Original Government ID Proof (Aadhaar Card / Passport / Voter ID / Driving License)",
            "Hotel & transport booking confirmations (saved offline as PDFs on phone)",
            "Emergency contact numbers note kept in wallet",
            "Student ID Card (if applicable, for museum/heritage monument discounts)"
        ]

        electronics = [
            "Smartphone with high-resolution camera",
            "Phone charger and high-speed multi-port cable",
            "High-capacity Power Bank (10,000–20,000 mAh for long sightseeing days)",
            "Earphones / Headphones for transit audio",
            "Universal travel adapter plug (if traveling internationally)"
        ]

        clothing = [
            f"{max(days, 3)} sets of breathable cotton shirts / t-shirts",
            "Comfortable pair of jeans / cotton cargo trousers or shorts",
            "Pair of broken-in walking sneakers / trainers with grip",
            "Comfortable sandals or slip-on flip-flops for casual walks",
            "Undergarments and extra pair of quick-dry socks"
        ]

        toiletries_and_health = [
            "Personal medical kit: Paracetamol, antacids, ORS hydration sachets, Band-aids, Pain balm",
            "Sunscreen lotion (SPF 50+ UVA/UVB protection)",
            "Mosquito repellent cream or roll-on (Odomos)",
            "Toiletry travel pouch: Toothbrush, toothpaste, shampoo sachets, face wash",
            "Pocket hand sanitizer and disinfectant wet wipes"
        ]

        useful_items = [
            "Durable 15-20L daypack for sightseeing and carrying essentials",
            "Reusable insulated water bottle to stay hydrated sustainably",
            "UV-protection sunglasses with polarized lenses",
            "Lightweight compact travel umbrella or foldable poncho",
            "Ziplock pouches / small dry-bag for toiletries and electronics"
        ]

        # Destination & interest tailored additions
        destination_specific = []
        travel_tips = []

        is_coastal = any(k in dest_lower for k in ["goa", "beach", "pondicherry", "kochi", "kerala", "daman", "puri", "mumbai", "andaman"]) or "beaches" in interests_lower
        is_mountain = any(k in dest_lower for k in ["manali", "shimla", "kullu", "leh", "ladakh", "ooty", "munnar", "darjeeling", "rishikesh", "nainital"]) or "adventure" in interests_lower
        is_heritage = any(k in dest_lower for k in ["jaipur", "agra", "delhi", "varanasi", "udaipur", "pune", "hampi"]) or "history" in interests_lower or "culture" in interests_lower

        if is_coastal:
            destination_specific.extend([
                "Quick-dry beach swimwear / swim shorts & UV-rash guard",
                "Waterproof phone pouch with neck lanyard for beach water sports",
                "Wide-brim sun hat or baseball cap",
                "Microfiber quick-dry beach towel"
            ])
            travel_tips.append("Stay cautious of strong undertow currents; swim only in designated lifegaurd-monitored beach zones.")
            travel_tips.append("Rent a scooter/two-wheeler with a valid helmet and license for the most cost-effective local transit.")
            travel_tips.append("Keep some physical cash handy, as coastal shacks and water sports counters sometimes face patchy UPI network connectivity.")

        if is_mountain:
            destination_specific.extend([
                "Warm fleece jacket or windproof thermal inner layer",
                "Sturdy trekking shoes with high-traction rubber soles",
                "Lip balm and moisturizing cold cream against mountain wind",
                "Motion-sickness tablets (Avomine) for winding ghat mountain roads"
            ])
            travel_tips.append("Layer your clothing in the mountains as daytime can be warm and nights drop sharply in temperature.")
            travel_tips.append("Start early for mountain viewpoints to avoid afternoon fog and peak holiday road traffic.")
            travel_tips.append("Keep offline maps downloaded on your phone as cellular data can drop in mountain passes.")

        if is_heritage:
            destination_specific.extend([
                "Modest breathable clothing covering shoulders and knees for temple/heritage visits",
                "Easy slip-on footwear (as shoes must frequently be removed at historic and holy shrines)",
                "Compact cloth tote bag for carrying shoes safely at temple gates"
            ])
            travel_tips.append("Hire licensed government audio-guides or group guides at major monuments for authentic historical context.")
            travel_tips.append("Check monument closing days (e.g. some monuments are closed on Mondays or Fridays) before heading out.")

        if not destination_specific:
            destination_specific.extend([
                f"City map or guidebook for {destination}",
                "Foldable reusable shopping bag for market souvenirs",
                "Comfortable slip-on shoes for versatile city exploring"
            ])

        # General practical travel tips
        travel_tips.append(f"Respect local cultural customs and dress etiquette while exploring public quarters of {destination}.")
        travel_tips.append("Always verify taxi/auto-rickshaw fares or ask them to run on the meter before boarding.")
        travel_tips.append("Stay hydrated with bottled or boiled water, and eat at busy food stalls where ingredients turn over rapidly.")

        return {
            "checklist": {
                "documents": documents,
                "electronics": electronics,
                "clothing": clothing,
                "toiletries_and_health": toiletries_and_health,
                "destination_specific": destination_specific,
                "useful_items": useful_items
            },
            "travel_tips": travel_tips[:5]
        }
