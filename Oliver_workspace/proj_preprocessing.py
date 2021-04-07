import pandas as pd
import numpy as np

def flights_preclean(df):
    """
    Input: Raw dataframe of Flights table.
    Output: Cleaned flights table:
        - Remove cancelled rows, made available in new dataframe "df_can"
        - Drop columns ['Unnamed: 0', 'branded_code_share',
           'mkt_carrier', 'cancelled', 'cancellation_code', 'flights', 'air_time',
            'first_dep_time', 'total_add_gtime', 'longest_add_gtime', 'no_name']
        - Fill null values in delay columns
        - Drop remaining null values
    
    """
    global df_can
    df_can = df[df.cancelled == 1].copy()
    print("Removed cancelled flights - now available in dataframe 'df_can'")
    df = df[df.cancelled == 0]
    df = df.drop(columns=['Unnamed: 0', 'branded_code_share',
           'mkt_carrier', 'cancelled', 'cancellation_code', 'flights', 'air_time',
            'first_dep_time', 'total_add_gtime', 'longest_add_gtime', 'no_name'])
    for col in ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']:
        df[col] = df[col].fillna(value=0)
    df = df.dropna()
    return df