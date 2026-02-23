# Real-Time Therapist Search Implementation

## What Changed

Your SafeSpace AI Agent now uses **real-time data** instead of static responses when users ask for nearby therapists!

### Previous Implementation ❌
- Returned hardcoded fake therapist names and phone numbers
- Same response regardless of location
- No actual data

### New Implementation ✅
- Uses **SAMHSA** (Substance Abuse and Mental Health Services Administration) - US Government database
- Completely **FREE** - no API key or payment info required
- Falls back to **OpenStreetMap** for global coverage
- Provides direct links to search results with real facilities

---

## How It Works

1. **User asks for therapists**: "Find therapists near New York"
2. **AI extracts location**: Detects the location from the user's message
3. **Geocoding**: Converts location name to coordinates using OpenStreetMap's Nominatim API (free)
4. **SAMHSA Search**: Queries SAMHSA database for mental health facilities
5. **Returns results**: Provides a direct link to SAMHSA's website with:
   - Licensed mental health treatment facilities
   - Contact information
   - Services offered
   - Payment options

---

## APIs Used (All FREE!)

### 1. **SAMHSA (Primary)**
- **What**: US Government mental health facility database
- **Cost**: FREE
- **Coverage**: United States only
- **API Key**: Not required
- **Website**: https://findtreatment.samhsa.gov

### 2. **OpenStreetMap Nominatim (Geocoding)**
- **What**: Converts location names to coordinates
- **Cost**: FREE
- **Coverage**: Global
- **API Key**: Not required
- **Limitations**: Rate limited (1 request/second)

### 3. **OpenStreetMap Overpass API (Fallback)**
- **What**: Community-driven map data for healthcare facilities
- **Cost**: FREE
- **Coverage**: Global (data quality varies)
- **API Key**: Not required

---

## How to Test

### 1. Start the Backend
```bash
cd backend
python main.py
```

### 2. Start the Frontend
```bash
python frontend.py
```

### 3. Test Queries

Try these example queries in the chat:

**US Locations:**
- "Find therapists near New York"
- "I need a therapist in Los Angeles"
- "Show me mental health services in Chicago"
- "Find counselors near 90210" (zip code)

**Non-US Locations (will use OpenStreetMap):**
- "Find therapists in London"
- "Mental health services in Mumbai"
- "Therapists near Toronto"

---

## What Users Will See

When a user asks for therapists, they'll get:

```
🏥 SAMHSA Mental Health Treatment Facilities near New York

I've found resources through SAMHSA (Substance Abuse and Mental Health Services Administration):

🔗 Click here to view facilities: [Direct link to SAMHSA search]

What you'll find:
- Licensed mental health treatment facilities
- Contact information and addresses
- Services offered
- Payment options accepted

Additional SAMHSA Resources:
📞 SAMHSA National Helpline: 1-800-662-4357
   - Free, confidential, 24/7, 365 days a year
   - Treatment referral and information service
   - Available in English and Spanish

💬 Crisis Text Line: Text HOME to 741741
☎️ 988 Suicide & Crisis Lifeline: Call or text 988

💡 Tip: When calling facilities, ask about:
- Accepting new patients
- Insurance accepted
- Sliding scale fees
- Telehealth options
```

---

## Code Changes Summary

### Files Modified:

1. **`backend/tools.py`**
   - Added `find_nearby_therapists()` function
   - Added `search_samhsa()` function
   - Added `search_openstreetmap()` function (fallback)
   - Uses free APIs (no payment info required)

2. **`backend/ai_agent.py`**
   - Updated import to include `find_nearby_therapists`
   - Changed static response to call the actual function
   - Extracts location from user query

3. **`backend/config.py`**
   - No API keys needed!

---

## Limitations & Notes

### SAMHSA Limitations:
- **US only**: Only covers United States facilities
- **No JSON API**: SAMHSA doesn't provide a clean JSON API, so we provide direct links to their search page
- **Facility-focused**: Shows treatment facilities, not individual private practice therapists

### OpenStreetMap Limitations:
- **Data quality varies**: Community-driven, so coverage depends on region
- **Less comprehensive**: May not have as many listings as commercial services
- **Rate limits**: Nominatim has rate limits (1 req/sec)

### Alternatives for More Data:
If you need more comprehensive therapist listings, consider:
- **Psychology Today** (requires web scraping, may violate ToS)
- **Google Places API** (requires billing info even for free tier)
- **Yelp Fusion API** (free tier available with API key)

---

## Future Improvements

1. **Add Yelp API**: For more comprehensive results
2. **Cache results**: Store geocoding results to reduce API calls
3. **Parse SAMHSA HTML**: Extract actual facility data from SAMHSA's HTML response
4. **Add filters**: Allow users to filter by insurance, specialty, etc.
5. **Show distance**: Calculate and display distance from user's location

---

## Troubleshooting

### "I couldn't find the location"
- Make sure the location is spelled correctly
- Try using a zip code instead
- Try a larger city name

### "No results found"
- Try expanding the search radius
- Try a nearby city
- The area might not have facilities in the database

### API Timeout
- OpenStreetMap APIs can be slow sometimes
- The app will timeout after 30 seconds and provide alternative resources

---

## Support Resources

The app always provides these backup resources if search fails:

**US Resources:**
- SAMHSA National Helpline: 1-800-662-4357
- Crisis Text Line: Text HOME to 741741
- 988 Suicide & Crisis Lifeline

**Online Therapy:**
- Psychology Today: https://www.psychologytoday.com/us/therapists
- BetterHelp: https://www.betterhelp.com
- Talkspace: https://www.talkspace.com

---

## Questions?

If you have any questions or want to add more features, feel free to ask!
