# ✅ Real-Time Therapist Search - WORKING SOLUTION

## Summary

Your SafeSpace AI Agent now returns **REAL mental health facilities** with actual names, addresses, and phone numbers using **OpenStreetMap** (completely free, no API key needed)!

---

## What You Get Now

When users ask "Find therapists near New York", they get responses like:

```
🏥 Mental Health Treatment Facilities near New York

Found 10 facilities:

1. **Chait Mental Health Center**
   📍 669 Castleton Avenue, West Brighton, 10301
   📞 +1 718 442 2225
   🌐 https://simhs.org/behavioral-health-services/
   🏥 Specialty: psychiatry

2. **Carroll Gardens Psychotherapy**
   📍 Brooklyn, NY
   📞 +1-718-243-1432
   🏥 Specialty: Mental Health

3. **First Step Children Center**
   📍 2955 Brighton 4th Street, Brooklyn, 11235
   📞 +1 718-509-4909
   🌐 https://www.firststepny.com/
   🏥 Specialty: child_psychiatry, paediatrics
   🕐 Hours: Mo-Fr 09:00-17:30

... and more!

Plus SAMHSA link for additional resources
```

---

## How It Works

1. **User asks**: "Find therapists near [location]"
2. **Geocoding**: Converts location to coordinates (free, OpenStreetMap Nominatim)
3. **Search**: Queries OpenStreetMap for mental health facilities within 25 miles
4. **Returns**: Real facility names, addresses, phones, websites, specialties
5. **Bonus**: Adds SAMHSA link for more comprehensive US facilities

---

## APIs Used (All 100% FREE!)

### OpenStreetMap Overpass API
- **Cost**: FREE forever
- **API Key**: Not required
- **Coverage**: Global
- **Data**: Community-driven, real facilities
- **Rate Limit**: Reasonable (don't spam)

### OpenStreetMap Nominatim (Geocoding)
- **Cost**: FREE
- **API Key**: Not required  
- **Rate Limit**: 1 request/second

---

## Test It Now!

### 1. Make sure both servers are running:

**Backend** (already running):
```bash
uv run backend/main.py
```

**Frontend**:
```bash
uv run streamlit run frontend.py
```

### 2. Open the app:
Go to: http://localhost:8501

### 3. Try these queries:

**US Cities:**
- "Find therapists near New York"
- "I need a therapist in Los Angeles"
- "Show me mental health services in Chicago"
- "Find counselors near San Francisco"

**Other Cities:**
- "Find therapists in London"
- "Mental health services in Toronto"
- "Therapists near Mumbai"

---

## What Changed

### Files Modified:

1. **`backend/tools.py`**
   - ✅ `find_nearby_therapists()` - Main function
   - ✅ `search_openstreetmap()` - Queries Overpass API and parses real facility data
   - ✅ Removed complex SAMHSA scraping (not needed)
   - ✅ Returns actual facility names, addresses, phones, websites

2. **`backend/ai_agent.py`**
   - ✅ Calls `find_nearby_therapists()` instead of returning static data
   - ✅ Extracts location from user query

3. **`pyproject.toml`**
   - ✅ Added `beautifulsoup4` (for future enhancements)

---

## Example Response

```
**🏥 Mental Health Treatment Facilities near New York, New York, United States**

Here are mental health facilities near your location:

1. **Chait Mental Health Center**
   📍 669 Castleton Avenue, West Brighton, 10301
   📞 +1 718 442 2225
   🌐 https://simhs.org/behavioral-health-services/
   🏥 Specialty: psychiatry

2. **Carroll Gardens Psychotherapy**
   📞 +1-718-243-1432
   🏥 Specialty: Mental Health

3. **RevCore**
   📞 +1-718-514-6007
   🌐 https://revcorerecovery.com
   🏥 Specialty: addiction counseling
   🕐 Hours: Mo-Fr 09:00-19:30; Sa 08:00-13:00

4. **Mind Body Seven**
   📍 200 Prospect Park West, 11215
   📞 +1-212-621-7770
   🌐 https://www.mindbody7.com
   🏥 Specialty: Mental Health

5. **Brooklyn Center for Psychotherapy**
   📍 300 Flatbush Avenue, 11217
   📞 +1-718-622-2000
   🌐 https://newdirectionsbrooklyn.com
   🏥 Specialty: Mental Health

**🏥 Additional Resource - SAMHSA (US Government Database):**
For more comprehensive US facilities, visit:
https://findtreatment.samhsa.gov/locator?sAddr=New+York&sType=MH&sDistanceUnit=MI&sDistance=25

**Additional Resources:**
- Psychology Today Therapist Finder: https://www.psychologytoday.com/us/therapists
- SAMHSA National Helpline: 1-800-662-4357 (free, confidential, 24/7)
- Crisis Text Line: Text HOME to 741741
```

---

## Advantages of OpenStreetMap

✅ **Completely Free** - No payment info, no API key
✅ **Real Data** - Actual facility names, addresses, phones
✅ **Global Coverage** - Works worldwide (data quality varies)
✅ **No JavaScript Required** - Direct API access
✅ **Community-Driven** - Constantly updated by volunteers
✅ **Detailed Info** - Specialties, hours, websites, accessibility

---

## Limitations

⚠️ **Data Quality Varies** - Depends on community contributions in that area
⚠️ **Not as Comprehensive** - May have fewer listings than commercial services
⚠️ **No Ratings** - Doesn't include patient reviews
⚠️ **Rate Limits** - Don't spam the API (be respectful)

---

## If You Want More Data

If OpenStreetMap doesn't return enough results in some areas, you can:

1. **Add Yelp Fusion API** (free tier available)
2. **Add Google Places API** (requires billing info)
3. **Combine multiple sources** for best coverage

---

## Next Steps

1. ✅ Test the app with different locations
2. ✅ Verify the data looks good
3. ✅ If needed, we can add more data sources
4. ✅ Can add filtering (by specialty, insurance, etc.)

---

## Questions?

The implementation is complete and working! Try it out and let me know if you want to:
- Add more data sources
- Filter results by specialty
- Add distance calculations
- Improve the formatting
- Anything else!

🎉 **You now have a working real-time therapist search!**
