"""
Destination Agent:
Specialized AI Agent responsible for researching and recommending suitable places
and activities based on the user's destination, travel style, and interests.
"""

import json
from utils.llm_service import query_llm

class DestinationAgent:
    def __init__(self):
        self.name = "Destination Agent"
        self.description = "Recommends top places and curated activities based on destination and traveler interests."

    def recommend_places(self, destination: str, interests: list, travel_style: str = "Standard", days: int = 3) -> list:
        """
        Recommends a manageable list of places tailored to destination & user preferences.
        Returns a list of dicts: [{name, category, description, suggested_activity}, ...]
        """
        # Target number of recommendations based on trip length
        target_count = max(4, min(days * 2 + 1, 8))

        # 1. Attempt LLM Generation if configured
        prompt = f"""
You are an expert travel destination specialist.
Provide a list of {target_count} recommended places to visit in {destination}.
Traveler Interests: {', '.join(interests)}
Travel Style: {travel_style}
Trip Duration: {days} days

Return strictly valid JSON with key "places" containing an array of objects:
{{
  "places": [
    {{
      "name": "Place Name",
      "category": "One of: Nature, Adventure, Beaches, History, Food, Shopping, Culture",
      "description": "Short 1-2 sentence description highlighting key appeal.",
      "suggested_activity": "Specific recommended activity for this traveler."
    }}
  ]
}}
"""
        system_instruction = "You are a professional travel curator. Respond strictly with valid JSON."
        llm_response = query_llm(prompt, system_instruction=system_instruction, json_format=True)

        if llm_response and isinstance(llm_response, dict) and "places" in llm_response:
            places = llm_response["places"]
            if isinstance(places, list) and len(places) >= 3:
                return places[:target_count]

        # 2. Rule-Based Knowledge Base & Fallback Generator
        return self._generate_fallback_places(destination, interests, travel_style, target_count)

    def _generate_fallback_places(self, destination: str, interests: list, travel_style: str, count: int) -> list:
        """Intelligent fallback for curated destinations or dynamic generation for any city."""
        dest_key = destination.strip().lower()

        # Curated destination database for popular student & tourist destinations
        knowledge_base = {
            "goa": [
                {
                    "name": "Baga & Calangute Beachfront",
                    "category": "Beaches",
                    "description": "Famous energetic coastline with golden sands, beachfront shacks, and exhilarating water sports.",
                    "suggested_activity": "Parasailing, banana boat ride, and sunset stroll along the shore."
                },
                {
                    "name": "Aguada Fort & Portuguese Lighthouse",
                    "category": "History",
                    "description": "Well-preserved 17th-century Portuguese fortress overlooking the Arabian Sea.",
                    "suggested_activity": "Explore the stone ramparts and take panoramic seascape photos."
                },
                {
                    "name": "Basilica of Bom Jesus (Old Goa)",
                    "category": "Culture",
                    "description": "UNESCO World Heritage site renowned for magnificent Baroque architecture and sacred relics.",
                    "suggested_activity": "Architectural photography and admiring historic 16th-century artworks."
                },
                {
                    "name": "Anjuna & Flea Market Coast",
                    "category": "Shopping",
                    "description": "Bohemian coastal hub famous for vibrant handicraft stalls, music, and beach cafes.",
                    "suggested_activity": "Shop for souvenirs, handmade jewelry, and enjoy live acoustic music."
                },
                {
                    "name": "Dudhsagar Waterfalls Trail",
                    "category": "Nature",
                    "description": "Majestic four-tiered white cascade nestled deep within Bhagwan Mahaveer Sanctuary.",
                    "suggested_activity": "Jeep safari through lush green jungle and swimming in natural rock pools."
                },
                {
                    "name": "Fontainhas Latin Quarter",
                    "category": "Culture",
                    "description": "Heritage residential neighborhood characterized by colorful Portuguese colonial cottages and bakeries.",
                    "suggested_activity": "Self-guided walking heritage tour and sampling authentic Goan poi and bebinca."
                },
                {
                    "name": "Chapora Fort (Dil Chahta Hai Fort)",
                    "category": "History",
                    "description": "Iconic hilltop fort ruins offering picturesque views of the Vagator beach and coastline.",
                    "suggested_activity": "Catch the evening golden hour sunset with friends."
                },
                {
                    "name": "Fisherman's Wharf & Seafood Trail",
                    "category": "Food",
                    "description": "Riverside dining haven serving authentic Goan fish curry, prawn balchão, and fresh coastal delicacies.",
                    "suggested_activity": "Indulge in traditional Goan thali with live Konkani melodies."
                }
            ],
            "pune": [
                {
                    "name": "Shaniwar Wada",
                    "category": "History",
                    "description": "Historical 18th-century fortification seat of the Peshwa rulers of the Maratha Empire.",
                    "suggested_activity": "Audio-guided walk through the grand Delhi Gate and gardens."
                },
                {
                    "name": "Sinhagad Fort",
                    "category": "Adventure",
                    "description": "Hill fortress perched atop the Sahyadri range offering misty scenic mountain panoramas.",
                    "suggested_activity": "Morning trek to the top followed by hot Pithla Bhakri and Kanda Bhajji."
                },
                {
                    "name": "Aga Khan Palace",
                    "category": "History",
                    "description": "Graceful Italian-arched historic palace and national monument associated with Mahatma Gandhi.",
                    "suggested_activity": "Peaceful heritage garden walk and museum exhibition tour."
                },
                {
                    "name": "FC Road & Vaishali Trail",
                    "category": "Food",
                    "description": "Bustling student epicenter lined with trendy cafes, street fashion stalls, and legendary eateries.",
                    "suggested_activity": "Savor authentic Filter Coffee, Mysore Masala Dosa, and street shopping."
                },
                {
                    "name": "Koregaon Park & Osho Teerth Gardens",
                    "category": "Nature",
                    "description": "Tree-lined chic enclave with Japanese zen public park, boutique cafes, and artisanal bakeries.",
                    "suggested_activity": "Relaxing nature stroll followed by coffee tasting at artisan roasteries."
                },
                {
                    "name": "Vetal Tekdi",
                    "category": "Nature",
                    "description": "The highest natural point within city limits, famous among fitness enthusiasts and bird watchers.",
                    "suggested_activity": "Sunrise hike to enjoy a 360-degree skyline view of Pune."
                }
            ],
            "jaipur": [
                {
                    "name": "Amber Palace & Fort",
                    "category": "History",
                    "description": "Opulent hilltop fort with artistic Hindu-style elements, cobbled pathways, and the Sheesh Mahal mirror palace.",
                    "suggested_activity": "Explore the mirror palace and attend the evening light & sound show."
                },
                {
                    "name": "Hawa Mahal (Palace of Winds)",
                    "category": "Culture",
                    "description": "Iconic pink sandstone facade with 953 intricately carved jharokhas (casements).",
                    "suggested_activity": "Morning photography and rooftop cafe breakfast opposite the monument."
                },
                {
                    "name": "City Palace & Jantar Mantar",
                    "category": "Culture",
                    "description": "Royal royal residence complex alongside the world-renowned UNESCO astronomical observatory.",
                    "suggested_activity": "Marvel at massive stone sundials and royal ceremonial costumes."
                },
                {
                    "name": "Chokhi Dhani Ethnic Resort",
                    "category": "Food",
                    "description": "Traditional Rajasthani village themed cultural hub with folk dances, camel rides, and feasts.",
                    "suggested_activity": "Feast on authentic Dal Baati Churma with Ghee and watch Kalbelia dance."
                },
                {
                    "name": "Johari Bazaar & Bapu Bazaar",
                    "category": "Shopping",
                    "description": "Vibrant walled city markets famous for Jaipuri quilts, gemstones, block-printed textiles, and mojari.",
                    "suggested_activity": "Bargain shopping for handicrafts and sampling Pyaz Kachori."
                },
                {
                    "name": "Nahargarh Fort Sunset Point",
                    "category": "Adventure",
                    "description": "Ramparts standing on the edge of the Aravalli Hills overlooking the entire Pink City.",
                    "suggested_activity": "Enjoy sweeping sunset views over the illuminated city below."
                }
            ],
            "manali": [
                {
                    "name": "Solang Valley",
                    "category": "Adventure",
                    "description": "High mountain valley celebrated for alpine meadows and exhilarating snow & adventure sports.",
                    "suggested_activity": "Paragliding over pine forests, ATV rides, and zorbing."
                },
                {
                    "name": "Hadimba Devi Temple",
                    "category": "Culture",
                    "description": "Unique 16th-century wooden pagoda temple tucked inside a dense, towering cedar forest.",
                    "suggested_activity": "Nature photography amidst ancient deodar trees and cedar craft stalls."
                },
                {
                    "name": "Old Manali Village & Cafes",
                    "category": "Food",
                    "description": "Charming wooden hamlet with bohemian riverside cafes, live indie music, and apple orchards.",
                    "suggested_activity": "Wood-fired trout, Italian pizza, and relaxing by the bubbling Manalsu stream."
                },
                {
                    "name": "Jogini Waterfall Hike",
                    "category": "Nature",
                    "description": "Serene cascading waterfall reached via a scenic trek starting from Vashisht village.",
                    "suggested_activity": "Short forest trek with dip in clean natural mountain springs."
                },
                {
                    "name": "Mall Road & Tibetan Monasteries",
                    "category": "Shopping",
                    "description": "Heart of town featuring Tibetan handicraft centers, woolen shawls, and fragrant tea stalls.",
                    "suggested_activity": "Shop for Kullu shawls, wooden souvenirs, and hot momos."
                },
                {
                    "name": "Atal Tunnel & Sissu Valley",
                    "category": "Adventure",
                    "description": "Engineering marvel leading to the surreal, rugged Chandra river valley of Lahaul.",
                    "suggested_activity": "Drive through the 9km tunnel to view frozen waterfalls and snow peaks."
                }
            ]
        }

        # Check for direct key match or substring match
        matched_places = None
        for key, places in knowledge_base.items():
            if key in dest_key or dest_key in key:
                matched_places = places
                break

        if matched_places:
            # Sort or prioritize based on user interests
            interests_lower = [i.lower() for i in interests]
            prioritized = []
            others = []
            for p in matched_places:
                if p["category"].lower() in interests_lower:
                    prioritized.append(p)
                else:
                    others.append(p)
            result = prioritized + others
            return result[:count]

        # Generic dynamic generator for ANY city worldwide
        city_title = destination.strip().title()
        generic_categories = [
            ("History", f"{city_title} Heritage Fort & Historical Museum", f"Historic landmark showcasing the timeless heritage, royal artifacts, and architecture of {city_title}.", "Take a guided historical tour and explore the ancient ramparts."),
            ("Culture", f"Old Town {city_title} Cultural Center", f"Atmospheric central quarter famous for sacred architecture, traditional ceremonies, and local life.", "Witness authentic cultural performances and interact with local artisans."),
            ("Nature", f"{city_title} Botanical Gardens & Lake Park", f"Tranquil scenic retreat boasting lush flora, walking tracks, and reflective waterfront views.", "Enjoy a peaceful morning walk and leisure paddle boating on the lake."),
            ("Food", f"{city_title} Gourmet Food Street & Night Market", f"Bustling culinary hub packed with iconic regional eateries, sweet shops, and street snacks.", "Sample the signature local specialties and famous desserts."),
            ("Adventure", f"{city_title} Hill Viewpoint & Trekking Trail", f"Elevated scenic ridge offering panoramic vistas across the entire region.", "Scenic light hike to capture sunrise or sunset landscape views."),
            ("Shopping", f"{city_title} Central Handicrafts Bazaar", f"Traditional vibrant market renowned for local textiles, handcrafted souvenirs, and spices.", "Pick up locally crafted mementos and regional gift items."),
            ("Beaches", f"{city_title} Coastline & Waterfront Promenade", f"Inviting waterside promenade lined with palm trees, seaside snack stalls, and breeze.", "Unwind by the water, dip your toes, and enjoy evening coastal snacks.")
        ]

        # Select items aligned with interests first
        interests_lower = [i.lower() for i in interests]
        selected = []
        for cat, name, desc, act in generic_categories:
            if cat.lower() in interests_lower:
                selected.append({
                    "name": name,
                    "category": cat,
                    "description": desc,
                    "suggested_activity": act
                })
        
        # Fill remaining slots with remaining categories
        for cat, name, desc, act in generic_categories:
            if len(selected) >= count:
                break
            if not any(s["category"] == cat for s in selected):
                selected.append({
                    "name": name,
                    "category": cat,
                    "description": desc,
                    "suggested_activity": act
                })

        return selected[:count]
