import json
import os
import requests
from datetime import datetime, timezone

# ==================================================
# Network Information
# ==================================================

NETWORK_NAME = "The Convergence Network"

MINISTRY_NAME = (
    "Christ the King Redemptive Ministries"
)

NETWORK_DESCRIPTION = (
    "A ministry broadcasting worship, biblical "
    "teaching, leadership development, and "
    "prophetic ministry programming."
)

WEBSITE_URL = "https://live.ctkrm.org"

MINISTRY_URL = "https://ctkrm.org"

SUPPORT_URL = "https://ctkrm.org"

# ==================================================
# YouTube Settings
# ==================================================

API_KEY = os.environ["YOUTUBE_API_KEY"]
CHANNEL_ID = os.environ["YOUTUBE_CHANNEL_ID"]

# ==================================================
# Default Offline Feed
# ==================================================

feed = {
    "networkName": NETWORK_NAME,
    "ministryName": MINISTRY_NAME,
    "networkDescription": NETWORK_DESCRIPTION,
    "website": WEBSITE_URL,
    "ministryWebsite": MINISTRY_URL,
    "supportWebsite": SUPPORT_URL,
    "isLive": False,
    "schedule": [
        {
            "title": "Live Worship",
            "time": "Sundays at 9:00 AM Eastern"
        },
        {
            "title": "Convergence Bible Institute",
            "time": "Tuesdays at 7:00 PM Eastern"
        },
        {
            "title": (
                "The J.A.M.M. "
                "(Jesus and Me Ministry)"
            ),
            "time": "Fridays at 7:00 PM Eastern"
        },
        {
            "title": (
                "Women of Prophetic Destiny "
                "Fellowship"
            ),
            "time": (
                "Every 2nd Friday "
                "at 7:00 PM Eastern"
            )
        },
        {
            "title": (
                "Women of Prophetic Destiny "
                "Fellowship"
            ),
            "time": (
                "Every 2nd Saturday "
                "at 7:00 PM Eastern"
            )
        },
        {
            "title": (
                "Women of Prophetic Destiny "
                "Fellowship"
            ),
            "time": (
                "Every 2nd Sunday "
                "at 4:00 PM Eastern"
            )
        }
    ],
    "lastUpdated": (
        datetime.now(timezone.utc).isoformat()
    )
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

    response = requests.get(
        url,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    # ----------------------------------------------
    # Channel is LIVE
    # ----------------------------------------------

    if data.get("items"):

        video = data["items"][0]

        video_id = video["id"]["videoId"]

        feed = {
            "networkName": NETWORK_NAME,
            "ministryName": MINISTRY_NAME,
            "networkDescription":
                NETWORK_DESCRIPTION,
            "website": WEBSITE_URL,
            "ministryWebsite": MINISTRY_URL,
            "supportWebsite": SUPPORT_URL,
            "isLive": True,
            "title":
                video["snippet"]["title"],
            "videoId": video_id,
            "youtubeWatchUrl":
                f"https://www.youtube.com/watch?v={video_id}",
            "lastUpdated":
                datetime.now(
                    timezone.utc
                ).isoformat()
        }

except Exception as e:

    feed["error"] = str(e)

# ==================================================
# Write Feed File
# ==================================================

with open("live.json", "w") as file:

    json.dump(
        feed,
        file,
        indent=2
    )

print("================================")
print("The Convergence Network Updated")
print("================================")
print(json.dumps(feed, indent=2))
