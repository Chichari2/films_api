"""The purpose of this file is to remove out of sight the technical details
which regard API interaction, in order to increase legibility of other parts
of the program."""

import os
import sys
import json
import requests
from flask import flash
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

NO_MATCH = "No movie matched the query, try modifying or try another."


def fetch_omdb_data(movie_title: str) \
        -> Optional[Tuple[str, str, int, float, str]]:
    """
    Fetches the movie data for 'movie_title'.
    After multiple iterations, I decided it made the most sense for the
    appropriate errors to be flashed here, even though data fetcher should
    work unrelated to Flask, or at least that was the idea.
    """
    req_url = API_BASE_URL + API_KEY + f"&t={movie_title}"
    try:
        response = requests.get(req_url, timeout=4)
    except (requests.ConnectionError, requests.ReadTimeout, requests.Timeout):
        flash("Error accessing API, timeout.", "info")
        return None
    if response.status_code != 200:
        flash(f"API conn error, status code: {response.status_code}", "info")
        return None
    data = response.text
    response_dict = json.loads(data)
    if response_dict.get("Response") == "False":
        flash(f"Movie '{movie_title}' not found!", "info")
        return None
    try:  # only meant to catch any errors for int() and round()
        name = response_dict.get("Title")
        if ',' in name:  # csv precaution: remove any ',' in movie title
            name = name.translate(str.maketrans('', '', ','))
        director = response_dict.get("Director")
        year = response_dict.get("Year")
        if year == 'N/A':
            year = 1850
        else:
            year = year.translate(str.maketrans('', '', '-–_'))
            year = int(year)
        rating = response_dict.get("imdbRating")
        print(rating)
        if rating == 'N/A':
            rating = 0.0
        else:
            rating = rating.translate(str.maketrans('', '', '-–_'))
            rating = round(float(rating), 1)
        poster = response_dict.get("Poster")
    except ValueError as e:
        flash(f"Incomplete movie entry for '{movie_title}', abort.", "info")
        return None
    return name, director, year, rating, poster
