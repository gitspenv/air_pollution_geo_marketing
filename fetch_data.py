### script to fetch data from aqicn.org ###

# imports
import requests
import pandas as pd
import json
from collections import defaultdict

# api params
token = "3eaef13118527b85b6704ccaeb132c742352b61d"
city = "Shanghai"

# make api request
r = requests.get(f"http://api.waqi.info/feed/{city}/?token={token}")

# put response to string and decode
json_string = r.text
decoder = json.JSONDecoder()

# convert to dict
response_dict = decoder.decode(json_string)

# dump json to file
file_path = "data.json"
with open (file_path, "w") as f:
    json.dump(response_dict, f)

# extract relevant variables
air_quality = response_dict["data"]["aqi"]
coordinates = response_dict["data"]["city"]["geo"]
time_iso = response_dict["data"]["time"]["iso"]
pollutants_dict = response_dict["data"]["iaqi"] = {k: v["v"] for k, v in response_dict["data"]["iaqi"].items()}

# extract forecasts and create daily dict with each pollutant avg for day
daily_data = response_dict["data"]["forecast"]["daily"]
pollutants_forecasts_dict = defaultdict(dict)
for pollutant, readings in daily_data.items():
    for entry in readings:
        day = entry["day"]
        avg = entry ["avg"]
        pollutants_forecasts_dict[day][pollutant] = avg

print (pollutants_forecasts_dict)