# Functions and other utilities for cleaning data.


# This function cleans data pulled from API requests for better graphing
# Run this function after converting the API response to a pandas dataframe
# The function takes the dataframe and the character on which a column needs to be split
# For the historical weather data, the splitter is "T"
# For the current weather data, the splitter is " "
# Function call will likely happen in a callback function.


def weather_clean(df, splitter):
    df1 = df["Hour"].str.split(splitter, expand=True)
    df1["Temperature"] = df["Temperature"]
    df1.rename(columns={0: "Date", 1: "Hour"}, inplace=True)
    return df1
