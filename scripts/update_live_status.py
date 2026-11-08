import json
import os
import requests

API_KEY = os.environ["YOUTUBE_API_KEY"]
CHANNEL_ID = os.environ["YOUTUBE_CHANNEL_ID"]

url = (
    "https://www.googleapis.com/youtube/v3/search"
    "?part=snippet"
    f"&channelId={CHANNEL_ID}"
    "&eventType=live"
    "&type=video"
    f"&key={API_KEY}"
)

response = requests.get(url)
data = response.json()

feed = {
    "networkName": "The Convergence Network",
    "isLive": False
}

if data.get("items"):
    video = data["items"][0]

    feed = {
        "networkName": "The Convergence Network",
        "isLive": True,
        "title": video["snippet"]["title"],
        "videoId": video["id"]["videoId"]
    }

with open("live.json", "w") as f:
    json.dump(feed, f, indent=2)

print("live.json updated")
