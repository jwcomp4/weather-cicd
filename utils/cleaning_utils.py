import pandas as pd

# Functions and other utilities for cleaning data.


# This function cleans data pulled from API requests for better graphing
# Run this function after converting the API response to a pandas dataframe
# The function takes the dataframe and the character on which a column needs to be split
# For the historical weather data, the splitter is "T"
# For the current weather data, the splitter is " "
# Function call will likely happen in a callback function.


def weather_clean(df, splitter, column):
    df1 = df["Hour"].str.split(splitter, expand=True)
    df1[column] = df[column]
    df1.rename(columns={0: "Date", 1: "Hour"}, inplace=True)
    return df1


def cw_filter(weather, col, weather_var):
    data = {
        "Hour": [x["time"] for x in weather["forecast"]["forecastday"][0]["hour"]],
        col: [y[weather_var] for y in weather["forecast"]["forecastday"][0]["hour"]],
    }
    df = pd.DataFrame(data)
    clean_df = weather_clean(df, " ", col)
    return clean_df


def high_low(weather):
    high = weather["forecast"]["forecastday"][0]["day"]["maxtemp_f"]
    low = weather["forecast"]["forecastday"][0]["day"]["mintemp_f"]
    return high, low
