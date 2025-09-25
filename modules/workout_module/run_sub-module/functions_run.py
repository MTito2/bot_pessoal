import sys
from pathlib import Path
from geopy.geocoders import Nominatim

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

import requests
import json
from keys import STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET
from config import FILES_RUN_SUB_MODULE_PATH
from general_functions import export_json

REFRESH_TOKEN_FILE = FILES_RUN_SUB_MODULE_PATH / "refresh_token.json"

def refresh_access_token():
    with open(REFRESH_TOKEN_FILE, "r") as f:
        refresh_token = json.load(f)["refresh_token"]

    res = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        }
    )
    data = res.json()
    with open(REFRESH_TOKEN_FILE, "w") as f:
        json.dump({"refresh_token": data["refresh_token"]}, f)
    return data["access_token"]

def get_all_activities(per_page=200):
    access_token = refresh_access_token()
    activities = []
    page = 1
    while True:
        res = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers={"Authorization": f"Bearer {access_token}"},
            params={"page": page, "per_page": per_page}
        )
        data = res.json()
        if not data:
            break
        
        activities.extend(data)
        page += 1
    return activities

def local_street(coordinates: list):
    geolocator = Nominatim(user_agent="meu_app")

    latitude = coordinates[0]
    longitude = coordinates[1]
    location = geolocator.reverse((latitude, longitude), language='pt')

    address = location.address.split(",")
    address = f"{address[0]}, {address[1]}, {address[2]}"

    return address
