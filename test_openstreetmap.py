"""
Test OpenStreetMap Overpass API for mental health facilities
"""
import requests
import json

location_name = "New York"
lat = 40.7128
lon = -74.0060
radius_miles = 25
radius_meters = int(radius_miles * 1609.34)

print(f"🗺️ Testing OpenStreetMap Overpass API...")
print(f"Location: {location_name}")
print(f"Coordinates: {lat}, {lon}")
print(f"Radius: {radius_miles} miles ({radius_meters} meters)\n")

overpass_url = "https://overpass-api.de/api/interpreter"

# Query for mental health facilities
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

print("📡 Sending request to Overpass API...")
try:
    response = requests.post(overpass_url, data={"data": overpass_query}, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        # Save response
        with open("openstreetmap_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Saved response to openstreetmap_response.json\n")
        
        elements = data.get("elements", [])
        print(f"📊 Found {len(elements)} facilities\n")
        
        if elements:
            print("First 3 facilities:")
            for i, element in enumerate(elements[:3], 1):
                tags = element.get("tags", {})
                print(f"\n{i}. {tags.get('name', 'Unnamed facility')}")
                print(f"   Type: {element.get('type')}")
                print(f"   Tags: {tags}")
                
                if element["type"] == "node":
                    print(f"   Coordinates: {element.get('lat')}, {element.get('lon')}")
                else:
                    center = element.get("center", {})
                    print(f"   Coordinates: {center.get('lat')}, {center.get('lon')}")
        else:
            print("❌ No facilities found")
            print("\nLet's try a broader search...")
            
            # Try broader search
            broad_query = f"""
            [out:json];
            (
              node["amenity"="hospital"](around:{radius_meters},{lat},{lon});
              node["amenity"="clinic"](around:{radius_meters},{lat},{lon});
              node["amenity"="doctors"](around:{radius_meters},{lat},{lon});
              node["healthcare"](around:{radius_meters},{lat},{lon});
            );
            out center 5;
            """
            
            print("\n📡 Trying broader search...")
            response2 = requests.post(overpass_url, data={"data": broad_query}, timeout=30)
            
            if response2.status_code == 200:
                data2 = response2.json()
                elements2 = data2.get("elements", [])
                print(f"📊 Broader search found {len(elements2)} healthcare facilities\n")
                
                for i, element in enumerate(elements2[:5], 1):
                    tags = element.get("tags", {})
                    print(f"{i}. {tags.get('name', 'Unnamed')} - {tags.get('amenity', 'N/A')}")
    else:
        print(f"❌ Request failed with status {response.status_code}")
        print(response.text[:500])
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ Test complete!")
