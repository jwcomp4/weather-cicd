import pandas as pd
import dash_design_kit as ddk
import requests
from datetime import datetime
import calendar
import geopy
from geopy.geocoders import GoogleV3
from config import GOOGLE_MAP_KEY, key
import json
import plotly
import plotly.express as px

# Functions and other utilities for making API requests, filtering data, cleaning it, and visualizing.


# Creating the locator object for geocoding:
locator = GoogleV3(api_key=GOOGLE_MAP_KEY, user_agent="newGeocoder")


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


# Function used to locate "sunrise", "sunset", and "moon_phase" within the current weather
def astro(weather, param):
    sky = weather["forecast"]["forecastday"][0]["astro"][param]
    return sky


# Function that cleans a dataframe by splitting a column and renaming the columns it split
# For the historical weather data, the splitter is "T"
# For the current weather data, the splitter is " "
def weather_clean(df, splitter, column):
    df1 = df["Hour"].str.split(splitter, expand=True)
    df1[column] = df[column]
    df1.rename(columns={0: "Date", 1: "Hour"}, inplace=True)
    return df1


# Function that filters current weather API response, creates a df, and cleans it:
def cw_filter(weather, col, weather_var):
    data = {
        "Hour": [x["time"] for x in weather["forecast"]["forecastday"][0]["hour"]],
        col: [y[weather_var] for y in weather["forecast"]["forecastday"][0]["hour"]],
    }
    df = pd.DataFrame(data)
    clean_df = weather_clean(df, " ", col)
    return clean_df


# Function that filters the current weather and finds the high and low temp for the day:
def high_low(weather):
    high = weather["forecast"]["forecastday"][0]["day"]["maxtemp_f"]
    low = weather["forecast"]["forecastday"][0]["day"]["mintemp_f"]
    return high, low


# Function that creates the ddk.DataCards and ddk.Card to hold weather information:
def weather_card(date, rise, set, moon, high, low, fig, fig2):
    sky_block = ddk.Card(
        id=date,
        children=[
            ddk.DataCard(
                id=date + "_sunrise", value=rise, label="Sunrise", icon="sun", width=100
            ),
            ddk.DataCard(
                id=date + "_sunset",
                value=set,
                label="Sunset",
                icon="cloud-sun",
                width=100,
            ),
            ddk.DataCard(
                id=date + "_moon_phase",
                value=moon,
                label="Moon Phase",
                icon="moon",
                width=100,
            ),
            ddk.DataCard(
                id=date + "_high_temp",
                value=high,
                label="High Temperature",
                icon="temperature-high",
                width=100,
            ),
            ddk.DataCard(
                id=date + "_low_temp",
                value=low,
                label="Low Temperature",
                icon="temperature-low",
                width=100,
            ),
        ],
    )
    rain_fig = ddk.Card(
        children=[
            ddk.CardHeader(id="test", title="Hourly Chance of Rain"),
            ddk.Graph(figure=fig),
        ]
    )
    weather_comp_fig = ddk.Card(
        children=[
            ddk.CardHeader(title="Temperature Comparison"),
            ddk.Graph(figure=fig2),
        ]
    )

    return sky_block, rain_fig, weather_comp_fig


# This function incorporates all of the above functions to geocode the address, make API request, filter data, clean it,
# make vizualizations, and create cards for the app layout
# This function will be called within 2 callbacks.
def get_weather(address, year):
    # Geocoding the address
    location = locator.geocode(address)
    # Grabbing the latitude and longitude
    lat = location.latitude
    lon = location.longitude
    # Making the api request for the current weather.
    current_weather = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={lat},{lon}&days=7&aqi=no&alerts=no"
    ).json()
    # Getting today's date to be used in the ids of the ddk.DataCards
    today = current_weather["location"]["localtime"][:10]
    # Using the astro func defined in api_utils.py to get the sunrise, sunset, and moon phase
    sunrise = astro(current_weather, "sunrise")
    sunset = astro(current_weather, "sunset")
    moon_phase = astro(current_weather, "moon_phase")
    high_temp, low_temp = high_low(current_weather)

    # filtering the current weather to create a df of the chance_of_rain

    precip = cw_filter(current_weather, "Rain Chance", "chance_of_rain")
    # Creating a bar graph for the Rain Chance:
    rain_today = px.bar(precip, x="Hour", y="Rain Chance")

    # Establishing the start and end date for the historical weather api request
    start_date, end_date = start_end(year)
    title_today = calendar.month_name[int(start_date[5:7])]

    # Historical weather

    hist_weather = requests.get(
        f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto&temperature_unit=fahrenheit&windspeed_unit=mph&precipitation_unit=inch"
    ).json()

    data = {
        "Hour": [x for x in hist_weather["hourly"]["time"]],
        "Temperature": [y for y in hist_weather["hourly"]["temperature_2m"]],
    }

    hw_df = pd.DataFrame(data)

    clean_hw = weather_clean(hw_df, "T", "Temperature")

    clean_cw = cw_filter(current_weather, "Temperature", "temp_f")

    weather_together = pd.concat([clean_hw, clean_cw])
    weather_together[["Year", "Day"]] = weather_together["Date"].str.split(
        "-", n=1, expand=True
    )
    weather_together.drop(columns=["Date"], inplace=True)
    weather_together.reset_index()

    temp_comp = px.line(
        weather_together,
        x="Hour",
        y="Temperature",
        color="Year",
        title=f"Historical and Present Temperature for {title_today} {start_date[8:]}",
        labels={"Hour": "Hour of the Day", "Temperature": "Temperature (°F)"},
    )

    # Using the weather_card() to create the cards for the dash app:
    weather_today = weather_card(
        today, sunrise, sunset, moon_phase, high_temp, low_temp, rain_today, temp_comp
    )
    return weather_today
