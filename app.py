import dash
from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import os
import requests
import json
import plotly
import plotly.express as px
import dash_design_kit as ddk
from utils.api_utils import start_end
from utils.cleaning_utils import weather_clean
from utils.controls import controls, second_address

app = dash.Dash(__name__)
server = app.server


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
                    id="api_params", children=controls, orientation="horizontal"
                ),
            )
        ),
        ddk.Row(id="weather1_row"),
    ]
)


@app.callback(
    Output("api_params", "children"),
    Input("second_address_q", "value"),
    prevent_initial_call=True,
)
def add_second_address(value):
    if value == "y":
        controls.append(second_address)
    if value == "n":
        dash.no_update
    return controls


if __name__ == "__main__":
    app.run(debug=True)
