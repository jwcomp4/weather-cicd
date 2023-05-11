import dash_design_kit as ddk


def weather_card(date, rise, set, moon, high, low, fig):
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
        children=[ddk.CardHeader(title="Hourly Chance of Rain"), ddk.Graph(figure=fig)]
    )

    return sky_block, rain_fig
