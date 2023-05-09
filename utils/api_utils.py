from datetime import datetime
import geopy
from geopy.geocoders import GoogleV3
from config import GOOGLE_MAP_KEY


# Function that formats the start/end date for the API request for historical weather
def start_end(year):
    today = datetime.now()
    if len(str(today.month)) < 2:
        month = "0" + str(today.month)
    else:
        month = str(today.month)
    if len(str(today.day)) < 2:
        day = "0" + str(today.day)
    else:
        day = str(today.day)
    start_date = year + "-" + month + "-" + day
    end_date = start_date
    return start_date, end_date


# Function used to locate "sunrise", "sunset", and "moon_phase"
def astro(current_weather, param):
    sky = current_weather["forecast"]["forecastday"][0]["astro"][param]
    return sky


locator = GoogleV3(api_key=GOOGLE_MAP_KEY, user_agent="newGeocoder")
