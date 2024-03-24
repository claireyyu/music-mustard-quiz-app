"""
Yue Yu
CS 5001, Fall 2023
Final Project -- models.artist_info

This program contains a class ArtistInfo that fetches artists' information from MusicBrainz API. MusicBrainz is an open music encyclopedia that collects music metadata
"""

import requests
import random
from models.random_mode_artists import random_mode_artists


class ArtistInfo:
    """
    This ArtistInfo class represents a controller to fetch data from MusicBrainz.

    Attributes:
    - base_url (str): The base URL for MusicBrainz API.

    Methods:
    - __init__(self, base_url=BASE_URL): Constructor method.
    - choose_current_artist(self) -> str: Chooses a random artist from the list of random_mode_artists.
    - fetch_artist_id(self, artist_name) -> str or None: Fetch a given artist's id from MusicBrainz API.
    - fetch_artist_works(self, artist_id) -> list or None: Fetch a given artist's works from MusicBrainz API.
    - generate_artist_link(self, artist_name, search_content) -> str or None: Generate the MusicBrainz link to the artist's search content.
    - __eq__(self, other): Compares two ArtistInfo instances for equality.
    - __str__(self): Returns a string representation of the ArtistInfo instance.
    """

    BASE_URL = 'https://beta.musicbrainz.org/ws/2/'

    def __init__(self, base_url=BASE_URL):
        """
        Constructor method.

        Parameters:
        - base_url (str): The base URL for MusicBrainz API.
        """
        self.base_url = base_url

    def choose_current_artist(self) -> str:
        """
        Chooses a random artist from the list of random_mode_artists.

        Returns:
        - str: The selected artist's name.
        """
        return random.choice(random_mode_artists)

    def fetch_artist_id(self, artist_name: str) -> str or None:
        """
        Fetch a given artist's id from MusicBrainz API.

        Parameters:
        - artist_name (str): The artist's name for fetching id.

        Returns:
        - str: The given artist's id.
        - None: In the case of an error.
        """
        endpoint = "artist"
        query = f"?query=artist:\"{artist_name}\"&limit=1&fmt=json"
        url = f"{self.BASE_URL}{endpoint}/{query}"

        try:
            # Sends an HTTP GET request to the URL using the requests library
            # Stores the information about the HTTP response
            response = requests.get(url)
            # Converts the JSON-formatted content into a Python dictionary
            data = response.json()
            # e.g. {"artists": [{"id": "095b2041-4975-4ba3-a92e-53fa3459107f"}]}
            artist_id = data.get('artists', [])[0].get('id', None)
            return artist_id
        except (requests.exceptions.ConnectionError, IndexError, KeyError):
            # Handle connection error, index error, or key error
            return None

    def fetch_artist_works(self, artist_id: str) -> list or None:
        """
        Fetch a given artist's works from MusicBrainz API.

        Parameters:
        - artist_id (str): The artist's id for fetching works.

        Returns:
        - list: List of artist's works.
        - None: In the case of an error.
        """
        endpoint = "work"
        query = f"?artist={artist_id}&fmt=json"
        url = f"{self.BASE_URL}{endpoint}/{query}"

        try:
            # Sends an HTTP GET request to the URL using the requests library
            # Stores the information about the HTTP response
            response = requests.get(url)
            # Converts the JSON-formatted content into a Python dictionary
            # e.g. {'works': [{'title': 'Song 1'}, {'title': 'Song 2'}]}
            data = response.json()

            # Check if 'works' key exists in the data
            if 'works' in data:
                # If 'works' key exists, create a list of works
                works_list = []
                for work in data["works"]:
                    works_list.append(work["title"])

                # Return the list of works
                return works_list
            else:
                # If 'works' key does not exist, return None
                return None

        except requests.exceptions.ConnectionError:
            # Handle connection error
            return None

    def generate_artist_link(self, artist_name: str, search_content: str) -> str or None:
        """
        Generate the MusicBrainz link to the artist's search content.

        Parameters:
        - artist_name (str): The artist's name for generating links.
        - search_content (str): Can be one of these: profile, works, genre, events.

        Returns:
        - str: MusicBrainz link to the artist's search content.
        - None: In the case of an error.
        """
        artist_id = self.fetch_artist_id(artist_name)
        endpoint = "artist"

        if artist_id:
            link_endpoints = {
                "profile": "",
                "works": "/works",
                "genre": "/tags",
                "events": "/events"
            }

            link_endpoint = link_endpoints.get(search_content)
            if endpoint:
                musicbrainz_link = f"https://beta.musicbrainz.org/{endpoint}/{artist_id}{link_endpoint}"
                return musicbrainz_link

        return None

    def __eq__(self, other):
        """
        Compares two ArtistInfo instances for equality.

        Parameters:
        - other (object): The object to compare with.

        Returns:
        - bool: True if the instances are equal, False otherwise.
        """
        if isinstance(other, ArtistInfo):
            return self.base_url == other.base_url
        return False

    def __str__(self):
        """
        Returns a string representation of the ArtistInfo instance.

        Returns:
        - str: String representation of the instance.
        """
        return f"ArtistInfo(base_url={self.base_url})"
