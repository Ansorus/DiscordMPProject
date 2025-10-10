import os
from datetime import datetime, timezone

import requests

api_key = os.environ["WEATHERKEY"]
url = "https://api.openweathermap.org/data/2.5/forecast"

params = {
    "lat": 37.34700356380359,
    "lon": -121.80657349405061,
    "appid": api_key,
}

weekday_to_str = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def get_weather():
    response = requests.get(url=url, params=params)
    response.raise_for_status()
    hourly = response.json()['list']
    for hour in hourly:
        if hour['weather'][0]['main'] == "Rain" or hour['weather'][0]['main'] == "Drizzle":
            dt = float(hour['dt'])
            when_rain = datetime.fromtimestamp(dt, tz=timezone.utc)
            return weekday_to_str[when_rain.weekday()]
    return None