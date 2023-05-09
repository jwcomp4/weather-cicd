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
                ddk.Logo(src=app.get_relative_path("/assets/wi-wind-deg.svg")),
                ddk.Title("A Simple Weather Dashboard"),
            ]
        )
    ]
)
