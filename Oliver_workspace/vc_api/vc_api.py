import pandas as pd
import requests
import json
import re
from datetime import datetime, date, timedelta
from IPython.display import JSON

# functions for turning airport codes and dates into requests

# load airport lat-long data
apt_coords = pd.read_csv('airport_coordinates.csv').rename(columns={"Unnamed: 0": "code"}).set_index('code')

def get_coords(code): # returns coordinates for airport code
    latlong = apt_coords.loc[code].lat_long.split(",")
    lat = latlong[0].strip()
    long = latlong[1].strip()
    return lat, long

def check_date_format(date): # makes sure the date is correctly formatted
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if re.search(pattern, date):
        return True
    else:
        return False

def request_url(apt_code, date, api_key): # returns url for request
    base = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
    try:
        lat, long = get_coords(apt_code)
    except KeyError:
        print(f"The airport code {apt_code} wasn't found.")
        return "https://www.google.com/ajnkajsdnflasdf"
    full_url = f"{base}{lat}%2C%20{long}/{date}/{date}?unitGroup=metric&key={api_key}&include=obs%2Chistfcst"
    return full_url

def get_data(code, date, api_key):
    if not check_date_format(date):
        print("Date not correctly formatted!")
    else:
        url = request_url(code, date, api_key)
        res = requests.get(url)
        return res.json(), res.status_code

def save_data(json_, apt_code, date):
    with open(f'weather-data/{apt_code}_{date}.json', 'w') as f:
        json.dump(json_, f)
        
def get_save(apt_code, date, api_key):
    global status_code
    data, status_code = get_data(apt_code, date, api_key)

    if status_code != 200:
        print(f"Bad status code: {status_code}")
    else:
        save_data(data, apt_code, date)
    return status_code
        
def generate_dates(start, end):
    """Returns a list of properly-formatted dates between the input start and end dates, inclusive.
    Dates must be formatted as 'YYYY-MM-DD' """
    if check_date_format(start) and check_date_format(end):
        day = datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.strptime(end, "%Y-%m-%d")
        lst = []
        while day <= end_dt:
            lst.append(datetime.strftime(day, format="%Y-%m-%d"))
            day += timedelta(days=1)
        return lst   
    else:
        print("Dates not correctly formatted")