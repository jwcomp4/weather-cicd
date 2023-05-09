# This file holds all of the controls for the dash application

import dash_design_kit as ddk
from dash import dcc, html

controls = [
    ddk.ControlItem(
        dcc.Input(id="address_value1", placeholder="Type initial address here")
    ),
    ddk.ControlItem(
        dcc.Dropdown(
            id="historical_year",
            options=[
                {"label": "1980", "value": "1980"},
                {"label": "1960", "value": "1960"},
                {"label": "1960", "value": "1960"},
            ],
            value="1980",
        ),
        label="Choose a historical year",
    ),
    ddk.ControlItem(
        dcc.RadioItems(
            id="second_address_q",
            options=[{"label": "Yes", "value": "y"}, {"label": "No", "value": "n"}],
            value="y",
        ),
        label="Do you wish to view a second location's weather?",
    ),
]

second_address = ddk.ControlItem(
    dcc.Input(
        id="address_value2",
        placeholder="Type a second address here",
    )
)
