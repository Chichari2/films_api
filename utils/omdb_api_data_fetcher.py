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
NO_MATCH = "No movie matched the query, try modifying or try another."


def bail_protocol(err_mess: str) -> None:
    """Flash an error message and return None."""
    flash(err_mess, "info")
    return None


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
        return bail_protocol("Error accessing API, timeout.")
    if response.status_code != 200:
        return bail_protocol(f"API error, status code: {response.status_code}")

    data = response.text
    response_dict = json.loads(data)
    if response_dict.get("Response") == "False":
        return bail_protocol(f"Movie '{movie_title}' not found!")

    name = response_dict.get("Title")
    director = response_dict.get("Director")
    year = response_dict.get("Year")
    rating = response_dict.get("imdbRating")
    poster = response_dict.get("Poster")

    # manual rectifications
    if ',' in name:  # csv precaution: remove any ',' in movie title
        name = name.translate(str.maketrans('', '', ','))
    if year == 'N/A' or year is None:
        year = '0'
    if rating == 'N/A' or year is None:
        rating = '0.0'

    if None in [name, director, year, rating, poster]:
        return bail_protocol(f"Corrupt entry for '{movie_title}', abort.")

    try:  # int() and round()
        year = year.translate(str.maketrans('', '', '-–_'))
        year = int(year)
        rating = rating.translate(str.maketrans('', '', '-–_'))
        rating = round(float(rating), 1)
    except ValueError:
        return bail_protocol(f"Corrupt entry for '{movie_title}', abort.")
    return name, director, year, rating, poster
