import json
import os
import requests
from datetime import datetime, timezone

# ==================================================
# Configuration
# ==================================================

NETWORK_NAME = "The Convergence Network"
WEBSITE_URL = "https://live.ctkrm.org"

API_KEY = os.environ["YOUTUBE_API_KEY"]
CHANNEL_ID = os.environ["YOUTUBE_CHANNEL_ID"]

# ==================================================
# Default Offline Feed
# ==================================================

feed = {
    "networkName": NETWORK_NAME,
    "isLive": False,
    "website": WEBSITE_URL,
    "schedule": [
        {
            "title": "Sunday Worship Service",
            "time": "Sunday 10:00 AM Eastern"
        },
        {
            "title": "Tuesday Leadership Training",
            "time": "Tuesday 7:00 PM Eastern"
        },
        {
            "title": "Wednesday Bible Study",
            "time": "Wednesday 7:00 PM Eastern"
        },
        {
            "title": "Friday Prayer Gathering",
            "time": "Friday 7:00 PM Eastern"
        }
    ],
    "lastUpdated": datetime.now(timezone.utc).isoformat()
}

# ==================================================
# Check YouTube Live Status
# ==================================================

try:

    url = (
        "https://www.googleapis.com/youtube/v3/search"
        "?part=snippet"
        f"&channelId={CHANNEL_ID}"
        "&eventType=live"
        "&type=video"
        f"&key={API_KEY}"
    )

    response = requests.get(url, timeout=30)

    response.raise_for_status()

    data = response.json()

    # ------------------------------------------------
    # Channel is LIVE
    # ------------------------------------------------

    if data.get("items"):

        video = data["items"][0]

        video_id = video["id"]["videoId"]

        feed = {
            "networkName": NETWORK_NAME,
            "isLive": True,
            "title": video["snippet"]["title"],
            "videoId": video_id,
            "youtubeWatchUrl": (
                f"https://www.youtube.com/watch?v={video_id}"
            ),
            "website": WEBSITE_URL,
            "lastUpdated": datetime.now(
                timezone.utc
            ).isoformat()
        }

# ==================================================
# Error Handling
# ==================================================

except Exception as e:

    feed["error"] = str(e)

# ==================================================
# Write Feed File
# ==================================================

with open("live.json", "w") as file:

    json.dump(feed, file, indent=2)

print("======================================")
print("The Convergence Network Feed Updated")
print("======================================")
print(json.dumps(feed, indent=2))
