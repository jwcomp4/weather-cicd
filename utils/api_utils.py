from datetime import datetime
import geopy
from geopy.geocoders import GoogleV3


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


locator = GoogleV3(api_key=GOOGLE_MAP_KEY, user_agent="newGeocoder")
