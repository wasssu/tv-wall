import os
import json
import requests

API_KEY = os.getenv("TMDB_API_KEY")

url = f"https://api.themoviedb.org/3/trending/tv/week?api_key={API_KEY}"

response = requests.get(url)
response.raise_for_status()

shows = response.json()["results"]

result = []

for show in shows[:10]:
    result.append({
        "title": show["name"],
        "rating": show["vote_average"],
        "poster": show["poster_path"],
        "overview": show["overview"]
    })

with open("data/tmdb.json", "w") as f:
    json.dump(result, f, indent=2)
