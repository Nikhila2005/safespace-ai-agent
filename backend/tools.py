# Step1: Setup Ollama with Medgemma tool
import ollama

def query_medgemma(prompt: str) -> str:
    """
    Calls MedGemma model with a therapist personality profile.
    Returns responses as an empathic mental health professional.
    """
    system_prompt = """You are Dr. Emily Hartman, a warm and experienced clinical psychologist. 
    Respond to patients with: 

    1. Emotional attunement ("I can sense how difficult this must be...")
    2. Gentle normalization ("Many people feel this way when...")
    3. Practical guidance ("What sometimes helps is...")
    4. Strengths-focused support ("I notice how you're...")

    Key principles:
    - Never use brackets or labels
    - Blend elements seamlessly
    - Vary sentence structure
    - Use natural transitions
    - Mirror the user's language level
    - Always keep the conversation going by asking open ended questions to dive into the root cause of patients problem
    """
    
    try:
        print(f"🔍 Calling MedGemma with prompt: {prompt}")
        response = ollama.chat(
            model='alibayram/medgemma:4b',
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            options={
                'num_predict': 350,  # Slightly higher for structured responses
                'temperature': 0.7,  # Balanced creativity/accuracy
                'top_p': 0.9        # For diverse but relevant responses
            }
        )
        result = response['message']['content'].strip()
        print(f"✅ MedGemma response: {result[:100]}...")
        return result
    except Exception as e:
        error_msg = f"MedGemma error: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return f"I'm having technical difficulties connecting to my therapeutic guidance system. However, I want you to know your feelings matter. Can you tell me more about what's making you feel sad?"

# Step2: Setup Twilio calling API tool
from twilio.rest import Client
from .config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, EMERGENCY_CONTACT


def call_emergency():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    call = client.calls.create(
        to=EMERGENCY_CONTACT,
        from_=TWILIO_FROM_NUMBER,
        url="http://demo.twilio.com/docs/voice.xml"  # Can customize message
    )

# Step3: Setup free APIs for finding therapists (no payment info required)
import requests
import json

def get_user_location() -> dict:
    """
    Automatically detect user's location using IP geolocation (free, no API key).
    Returns dict with lat, lon, and location name.
    """
    try:
        print("🌐 Detecting your location...")
        # Use ipapi.co - free, no API key required
        response = requests.get("https://ipapi.co/json/", timeout=5)
        data = response.json()
        
        lat = data.get("latitude")
        lon = data.get("longitude")
        city = data.get("city", "")
        region = data.get("region", "")
        country = data.get("country_name", "")
        
        location_name = f"{city}, {region}, {country}" if city else f"{region}, {country}"
        
        print(f"📍 Detected location: {location_name} ({lat}, {lon})")
        
        return {
            "lat": lat,
            "lon": lon,
            "name": location_name
        }
    except Exception as e:
        print(f"❌ Could not detect location: {e}")
        return None

def find_nearby_therapists(location: str = None, radius: int = 5) -> str:
    """
    Find nearby therapists using OpenStreetMap (completely free, no API key required).
    If no location is provided, automatically detects user's location.
    
    Args:
        location: Location name (e.g., "New York", "Mumbai", "90210") or None for auto-detect
        radius: Search radius in miles (default 5 miles for auto-detect, 25 for manual)
    
    Returns:
        Formatted string with therapist information
    """
    try:
        # If no location provided, auto-detect
        if not location or location == "your area":
            user_location = get_user_location()
            if user_location:
                lat = user_location["lat"]
                lon = user_location["lon"]
                display_name = user_location["name"]
                radius = 5  # Smaller radius for auto-detected location
                print(f"✅ Using auto-detected location: {display_name}")
            else:
                return "I couldn't detect your location automatically. Please specify a location like 'Find therapists near Bangalore'"
        else:
            # Geocode the provided location using Nominatim (free, no API key)
            print(f"🌍 Geocoding location: {location}")
            geocode_url = "https://nominatim.openstreetmap.org/search"
            geocode_params = {
                "q": location,
                "format": "json",
                "limit": 1
            }
            headers = {
                "User-Agent": "SafeSpace-Mental-Health-App/1.0"  # Required by Nominatim
            }
            
            geocode_response = requests.get(geocode_url, params=geocode_params, headers=headers)
            geocode_data = geocode_response.json()
            
            if not geocode_data:
                return f"Sorry, I couldn't find the location '{location}'. Please try:\n- A city name (e.g., 'New York')\n- A zip code (e.g., '10001')\n- A state name (e.g., 'California')"
            
            lat = float(geocode_data[0]["lat"])
            lon = float(geocode_data[0]["lon"])
            display_name = geocode_data[0]["display_name"]
            radius = 25  # Larger radius for manual location
            
            print(f"📍 Found coordinates: {lat}, {lon} ({display_name})")
        
        # Search OpenStreetMap for mental health facilities
        print("🗺️ Searching OpenStreetMap for facilities...")
        osm_results = search_openstreetmap(lat, lon, radius, display_name)
        
        if osm_results:
            return osm_results
        
        # If OpenStreetMap didn't return results, provide helpful resources
        print("⚠️ OpenStreetMap returned no results, providing alternative resources...")
        
        result = f"""I couldn't find specific mental health facilities near {display_name} in the database, but here are some resources to help:

**Search Online Directories:**
- Psychology Today: https://www.psychologytoday.com/us/therapists
- GoodTherapy: https://www.goodtherapy.org/therapists
- TherapyDen: https://www.therapyden.com
- BetterHelp (Online Therapy): https://www.betterhelp.com

**Immediate Support (24/7):**
📞 **National Helpline**: 1-800-662-4357 (Free, confidential)
💬 **Crisis Text Line**: Text HOME to 741741
☎️ **988 Suicide & Crisis Lifeline**: Call or text 988

**💡 Tips for finding a therapist:**
1. Check with your insurance for in-network providers
2. Ask your doctor for referrals
3. Search "[your city] mental health services" online
4. Many therapists offer telehealth/online sessions
5. Ask about sliding scale fees if cost is a concern
"""
        
        return result

        
    except Exception as e:
        error_msg = f"Error finding therapists: {str(e)}"
        print(f"❌ {error_msg}")
        import traceback
        traceback.print_exc()
        return f"""I encountered an error while searching. Here are crisis resources:

**Immediate Help:**
- 988 Suicide & Crisis Lifeline
- Crisis Text Line: Text HOME to 741741
- National Helpline: 1-800-662-4357

**Find Therapists Online:**
- Psychology Today: https://www.psychologytoday.com/us/therapists
- BetterHelp: https://www.betterhelp.com"""





def search_openstreetmap(lat: float, lon: float, radius_miles: int, location_name: str) -> str:

    """
    Search OpenStreetMap for mental health facilities using Overpass API.
    Completely free, no API key required.
    """
    try:
        print(f"🗺️ Searching OpenStreetMap...")
        
        # Convert miles to meters for Overpass API
        radius_meters = int(radius_miles * 1609.34)
        
        # Overpass API query for mental health facilities
        overpass_url = "https://overpass-api.de/api/interpreter"
        
        # Query for healthcare facilities that might offer mental health services
        overpass_query = f"""
        [out:json];
        (
          node["amenity"="doctors"]["healthcare:speciality"~"psychiatry|psychology|mental_health"](around:{radius_meters},{lat},{lon});
          node["amenity"="clinic"]["healthcare:speciality"~"psychiatry|psychology|mental_health"](around:{radius_meters},{lat},{lon});
          node["healthcare"="psychotherapist"](around:{radius_meters},{lat},{lon});
          node["healthcare"="counselling"](around:{radius_meters},{lat},{lon});
          way["amenity"="doctors"]["healthcare:speciality"~"psychiatry|psychology|mental_health"](around:{radius_meters},{lat},{lon});
          way["amenity"="clinic"]["healthcare:speciality"~"psychiatry|psychology|mental_health"](around:{radius_meters},{lat},{lon});
          way["healthcare"="psychotherapist"](around:{radius_meters},{lat},{lon});
          way["healthcare"="counselling"](around:{radius_meters},{lat},{lon});
        );
        out center 10;
        """
        
        response = requests.post(overpass_url, data={"data": overpass_query}, timeout=30)
        data = response.json()
        
        if not data.get("elements"):
            print("⚠️ No results from OpenStreetMap")
            return None
        
        # Format results
        facilities = []
        for element in data["elements"][:5]:  # Limit to 5 results
            tags = element.get("tags", {})
            
            # Get coordinates
            if element["type"] == "node":
                elem_lat = element.get("lat")
                elem_lon = element.get("lon")
            else:  # way
                elem_lat = element.get("center", {}).get("lat")
                elem_lon = element.get("center", {}).get("lon")
            
            facility = {
                "name": tags.get("name", "Mental Health Facility"),
                "address": tags.get("addr:street", "Address not available"),
                "city": tags.get("addr:city", ""),
                "phone": tags.get("phone", "N/A"),
                "website": tags.get("website", "N/A"),
                "specialty": tags.get("healthcare:speciality", "Mental Health"),
                "lat": elem_lat,
                "lon": elem_lon
            }
            facilities.append(facility)
        
        if not facilities:
            return None
        
        # Format output
        result = f"Here are mental health facilities near {location_name}:\n\n"
        for i, facility in enumerate(facilities, 1):
            result += f"{i}. **{facility['name']}**\n"
            if facility['address'] != "Address not available":
                result += f"   📍 {facility['address']}"
                if facility['city']:
                    result += f", {facility['city']}"
                result += "\n"
            result += f"   📞 {facility['phone']}\n"
            if facility['website'] != "N/A":
                result += f"   🌐 {facility['website']}\n"
            result += f"   🏥 Specialty: {facility['specialty']}\n"
            result += "\n"
        
        result += "\n💡 **Additional Resources:**\n"
        result += "- Psychology Today Therapist Finder: https://www.psychologytoday.com/us/therapists\n"
        result += "- National Helpline: 1-800-662-4357 (free, confidential, 24/7)\n"
        result += "- Crisis Text Line: Text HOME to 741741\n"
        
        return result
        
    except Exception as e:
        print(f"⚠️ OpenStreetMap search failed: {e}")
        import traceback
        traceback.print_exc()
        return None


