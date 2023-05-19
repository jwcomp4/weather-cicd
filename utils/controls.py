# This file holds all of the controls for the dash application

import dash_design_kit as ddk
from dash import dcc, html

controls = [
    ddk.ControlItem(
        dcc.Input(id="address_value1", placeholder="Type initial address here"),
        label="Initial Address",
    ),
    ddk.ControlItem(
        dcc.Dropdown(
            id="historical_year",
            options=[
                {"label": "1990", "value": "1990"},
                {"label": "1980", "value": "1980"},
                {"label": "1970", "value": "1970"},
            ],
            value="1980",
        ),
        label="Choose a historical year",
    ),
    ddk.ControlItem(
        dcc.RadioItems(
            id="second_address_q",
            options=[{"label": "Yes", "value": "y"}, {"label": "No", "value": "n"}],
            value="n",
        ),
        label="Do you wish to view a second location's weather?",
    ),
    ddk.ControlItem(
        id="second_address",
        children=dcc.Input(
            id="address_value2",
            placeholder="Select Yes to add 2nd Address",
        ),
        label="Second Address",
    ),
    html.Button("Get Weather", id="weather_button"),
]
