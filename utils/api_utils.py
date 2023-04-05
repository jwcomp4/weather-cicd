from datetime import datetime
import geopy
from geopy.geocoders import Nominatim


def start_end():
    today = datetime.now()
    if len(str(today.month)) < 2:
        month = "0" + str(today.month)
    else:
        month = str(today.month)
    if len(str(today.day)) < 2:
        day = "0" + str(today.day)
    else:
        day = str(today.day)
    start_date = "1980" + "-" + month + "-" + day
    end_date = start_date
    return start_date, end_date


start_date, end_date = start_end()

locator = Nominatim(user_agent="myGeocoder")
