import dash
from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import os
import requests
import json
import plotly
import plotly.express as px
import dash_design_kit as ddk
from utils.api_utils import start_end, locator, astro
from utils.cleaning_utils import weather_clean, cw_filter, high_low
from utils.controls import controls
from utils.weather_cards import weather_card
from config import key

app = dash.Dash(__name__)
server = app.server

# Creating the Layout
app.layout = ddk.App(
    [
        ddk.Header(
            [
                ddk.Logo(src=app.get_asset_url("/assets/logo.svg")),
                ddk.Title("A Simple Weather Dashboard"),
            ]
        ),
        ddk.Row(
            ddk.Block(
                id="control_block",
                children=ddk.ControlCard(
                    id="api_params",
                    children=controls,
                    orientation="horizontal",
                ),
            )
        ),
        ddk.Row(id="weather1_row"),
        ddk.Row(id="weather2_row"),
    ]
)


# Callbacks
@app.callback(
    Output("second_address", "style"),
    Output("address_value2", "placeholder"),
    Input("second_address_q", "value"),
)
def add_second_address(value):
    # This callback determines whether or not the user can input a second address.
    # Targets the style prop of the ControlCard
    if value == "y":
        return {"display": True}, "Type a second address here"
    if value == "n":
        return {"display": "None"}, dash.no_update


@app.callback(
    Output("weather1_row", "children"),
    Input("weather_button", "n_clicks"),
    State("address_value1", "value"),
    State("historical_year", "value"),
    prevent_initial_call=True,
)
def weather_request(n_clicks, address, year):
    # This callback makes API calls and creates our visualizations.

    # Geocoding the address and creating the locator object
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

    precip = cw_filter(current_weather, "Rain Chance", "chance_of_rain")
    rain_today = px.bar(precip, x="Hour", y="Rain Chance")

    # Establishing the start and end date for the historical weather api request
    start_date, end_date = start_end(year)

    weather_today = weather_card(
        today, sunrise, sunset, moon_phase, high_temp, low_temp, rain_today
    )
    return weather_today


@app.callback(
    Output("weather2_row", "children"),
    Input("weather_button", "n_clicks"),
    State("address_value2", "value"),
    State("historical_year", "value"),
    prevent_initial_call=True,
)
def weather2_request(n_clicks, address, year):
    # This callback makes API calls and creates our visualizations.

    # Geocoding the address and creating the locator object
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

    precip = cw_filter(current_weather, "Rain Chance", "chance_of_rain")
    rain_today = px.bar(precip, x="Hour", y="Rain Chance")

    # Establishing the start and end date for the historical weather api request
    start_date, end_date = start_end(year)

    weather_today = weather_card(
        today, sunrise, sunset, moon_phase, high_temp, low_temp, rain_today
    )
    return weather_today


if __name__ == "__main__":
    app.run(debug=True)
