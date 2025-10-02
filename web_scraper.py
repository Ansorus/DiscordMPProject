import urllib.parse
from datetime import datetime, timedelta, timezone
import pytz
import requests


token = "AIzaSyDqbv_dtuGWizpUIgvafUbPZBtqn6cnGnw"

encoded = urllib.parse.quote("uti479jsh2khqt45rnu4l87oik@group.calendar.google.com")

ex = "2020-06-03T10:00:00-07:00"

formatted = datetime.now(pytz.utc).isoformat()
max_time = (datetime.now(pytz.utc) + timedelta(days=14)).isoformat()

data = {
    "timeMin": formatted,
    "timeMax": max_time,
    "orderBy": "startTime",
    "singleEvents": True
}

def get_events():
    response = requests.get(url="https://www.googleapis.com/calendar/v3/calendars/" + encoded + "/events?key=AIzaSyDqbv_dtuGWizpUIgvafUbPZBtqn6cnGnw", params=data)
    mess = response.json()
    events = []
    for item in mess["items"]:
        name = item["summary"]
        start_str = item['start']['date'] if 'date' in item['start'] else item['start']['dateTime']
        start = datetime.fromisoformat(start_str)
        end_str = item['end']['date'] if 'date' in item['end'] else item['end']['dateTime']
        end = datetime.fromisoformat(end_str)
        events.append({"name": name, "start": start, "end": end})
    return events