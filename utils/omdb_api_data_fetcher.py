"""The purpose of this file is to remove out of sight the technical details
which regard API interaction, in order to increase legibility of other parts
of the program."""

import os
import sys
import json
import requests
from typing import Optional, Tuple
from dotenv import load_dotenv, find_dotenv
if not find_dotenv():
    print("Error: .env file not found. Consult README.md")
    sys.exit(1)
load_dotenv()

API_KEY = os.getenv('API_KEY')
API_BASE_URL = "http://www.omdbapi.com/?apikey="
POSTER_BASE_URL = "http://img.omdbapi.com/?apikey="

"""
{
    "Response": "False",
    "Error": "Movie not found!"
}
"""


def fetch_omdb_data(movie_title: str) \
        -> Optional[Tuple[str, str, int, float, str]]:
    """Fetches the movie data for 'movie_title'."""
    req_url = API_BASE_URL + API_KEY + f"&t={movie_title}"
    try:
        response = requests.get(req_url, timeout=3)
    except (requests.ConnectionError, requests.ReadTimeout, requests.Timeout):
        print("Error connecting to the API.")
        return None
    if response.status_code != 200:
        print(f"Error accessing API, status code {response.status_code}")
        return None
    data = response.text
    response_dict = json.loads(data)
    if response_dict.get("Response") == "False":
        print(f"Movie '{movie_title}' not found!")
        return None
    try:  # only meant to catch any errors for int() and round()
        name = response_dict.get("Title")
        if ',' in name:  # csv precaution: remove any ',' in movie title
            name = name.translate(str.maketrans('', '', ','))
        director = response_dict.get("Director")
        year = int(response_dict.get("Year"))
        rating = round(float(response_dict.get("imdbRating")), 1)
        poster = response_dict.get("Poster")
    except ValueError as e:
        print(e)
        return None
    return name, director, year, rating, poster
