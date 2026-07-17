# Handles all communication with the TMDB API

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


class TMDBClient:
    """Wraps TMDB API calls for searching movies/shows and fetching details."""

    def __init__(self, api_key=API_KEY):
        if not api_key:
            raise ValueError("TMDB_API_KEY not found. Check your .env file.")
        self.api_key = api_key

    def search(self, query, media_type="multi"):
        """
        Search TMDB for a movie or TV show by title.
        media_type: 'movie', 'tv', or 'multi' (searches both)
        Returns a list of simplified result dicts.
        """
        url = f"{BASE_URL}/search/{media_type}"
        params = {"api_key": self.api_key, "query": query}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        results = []
        for item in data.get("results", []):
            item_type = item.get("media_type", media_type)
            if item_type not in ("movie", "tv"):
                continue  # skip 'person' results from multi-search
            title = item.get("title") or item.get("name")
            release_date = item.get("release_date") or item.get("first_air_date")
            results.append({
                "tmdb_id": item["id"],
                "media_type": item_type,
                "title": title,
                "poster_path": item.get("poster_path"),
                "overview": item.get("overview", ""),
                "release_date": release_date,
            })
        return results

    def get_tv_details(self, tmdb_id):
        """Fetch full season list for a TV show (used after adding a show)."""
        url = f"{BASE_URL}/tv/{tmdb_id}"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        seasons = []
        for s in data.get("seasons", []):
            # Skip "Specials" (season_number 0) by default
            if s["season_number"] == 0:
                continue
            seasons.append({
                "season_number": s["season_number"],
                "episode_count": s["episode_count"],
                "overview": s.get("overview", ""),
            })
        return seasons

    def get_season_episodes(self, tmdb_id, season_number):
        """Fetch episode list for a specific season."""
        url = f"{BASE_URL}/tv/{tmdb_id}/season/{season_number}"
        params = {"api_key": self.api_key}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        episodes = []
        for ep in data.get("episodes", []):
            episodes.append({
                "episode_number": ep["episode_number"],
                "title": ep.get("name", ""),
                "air_date": ep.get("air_date"),
            })
        return episodes