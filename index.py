import dash
from dash import Dash, dcc, html, Input, Output, State, ctx
import os
import requests
import dash_design_kit as ddk
from utils.cleaning_utils import get_weather, get_lat_lon
from utils.controls import controls
import redis
from flask_caching import Cache
import geopy
from geopy.geocoders import GoogleV3
from app import app

server = app.server

# Creating the Layout
app.layout = ddk.App(
    [
        dcc.Geolocation(id="geolocation"),
        ddk.Header(
            [
                ddk.Logo(src=app.get_asset_url("/logo.svg")),
                ddk.Title("A Simple Weather Dashboard!"),
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
    State("geolocation", "position"),
    State("address_value1", "value"),
    State("historical_year", "value"),
    prevent_initial_call=True,
)
 
def weather_request(n_clicks, pos, address, year):
    # This callback makes API calls and creates our visualizations.
    # This weather is for the first address and outputs to the first row
    # @cache.memoize(timeout=120)
    lat, lon = get_lat_lon(address)
    
    weather_today = get_weather(lat, lon, year)
    # weather_title = html.Div(f"Weather for {address}")
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
    # This weather is for the second address (if given) and outputs to the second row
    if address == None:
        return dash.no_update
    else:
        lat, lon = get_lat_lon(address)
        second_weather = get_weather(lat, lon, year)
        return second_weather


if __name__ == "__main__":
    app.run(debug=True)