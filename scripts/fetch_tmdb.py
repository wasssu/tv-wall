import os
import json
from datetime import datetime, timezone

import requests

API_KEY = os.getenv("TMDB_API_KEY")

if not API_KEY:
    raise RuntimeError("TMDB_API_KEY secret is missing.")

BASE_URL = "https://api.themoviedb.org/3"

IMAGE_BASE = "https://image.tmdb.org/t/p/w500"


def get(endpoint):
    r = requests.get(
        f"{BASE_URL}/{endpoint}",
        params={"api_key": API_KEY},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["results"]


def convert(items):
    result = []

    for item in items:
        result.append({
            "id": item["id"],
            "title": item.get("name") or item.get("title"),
            "rating": item["vote_average"],
            "overview": item["overview"],
            "poster": IMAGE_BASE + item["poster_path"] if item["poster_path"] else None,
            "backdrop": IMAGE_BASE + item["backdrop_path"] if item["backdrop_path"] else None,
            "release": item.get("first_air_date") or item.get("release_date")
        })

    return result


data = {
    "updated": datetime.now(timezone.utc).isoformat(),
    "trending": convert(get("trending/tv/week")),
    "popular": convert(get("tv/popular")),
    "top_rated": convert(get("tv/top_rated")),
    "airing_today": convert(get("tv/airing_today"))
}

os.makedirs("data", exist_ok=True)

with open("data/tmdb.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("tmdb.json updated.")
