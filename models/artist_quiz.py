"""
Yue Yu
CS 5001, Fall 2023
Final Project -- models.artist_quiz

This program contains a class ArtistQuiz that generates questions and options for the quiz.

Methods: generate_false_answers, generate_question_default_mode, generate_question_personal_mode
"""

import random
from models.random_mode_artists import random_mode_artists
from models.artist_info import ArtistInfo


class ArtistQuiz:
    """
    This ArtistQuiz class represents a controller for generating quiz questions.

    Attributes:
    - BASE_URL (str): The base URL for MusicBrainz API.

    Methods:
    - __init__(self, base_url=BASE_URL): Constructor method.
    - generate_false_answers(self, current_artist): Generate false answers for a quiz question.
    - get_remaining_artists(self, current_artist: str): Get a list of artists that doesn't contain the current artist.
    - choose_false_artists(self, remaining_artists, k=2): Choose a specified number of false artists from the remaining artists.
    - get_false_artists_works(self, false_artists): Get works for each false artist.
    - generate_question_random_mode(self): Generate a quiz question in random mode.
    - generate_question_personal_mode(self, current_artist): Generate a quiz question in personal mode.
    - __eq__(self, other): Compares two ArtistQuiz instances for equality.
    - __str__(self): Returns a string representation of the ArtistQuiz instance.
    """

    BASE_URL = 'https://beta.musicbrainz.org/ws/2/'

    def __init__(self, base_url=BASE_URL):
        """
        Constructor method.

        Parameters:
        - base_url (str): The base URL for MusicBrainz API.
        """
        self.base_url = base_url

    def generate_false_answers(self, current_artist: str):
        """
        Generate false answers for a quiz question.

        Parameters:
        - current_artist (str): The current artist for the quiz question.

        Returns:
        - list: List of false answers.
        """
        remaining_artists = self.get_remaining_artists(current_artist)
        false_artists = self.choose_false_artists(remaining_artists, k=2)
        false_artists_works_options = self.get_false_artists_works(false_artists)

        return false_artists_works_options

    def get_remaining_artists(self, current_artist: str):
        """
        Get a list of artists that doesn't contain the current artist.

        Parameters:
        - current_artist (str): The current artist for the quiz question.

        Returns:
        - list: List of remaining artists.
        """
        remaining_artists = random_mode_artists.copy()
        # If random mode, current artist is in random_mode_artists
        if current_artist in remaining_artists:
            remaining_artists.remove(current_artist)

        return remaining_artists

    def choose_false_artists(self, remaining_artists, k=2):
        """
        Choose a specified number of false artists from the remaining artists.

        Parameters:
        - remaining_artists (list): List of remaining artists.
        - k (int): Number of false artists to choose.

        Returns:
        - list: List of false artists.
        """
        return random.sample(remaining_artists, k)

    def get_false_artists_works(self, false_artists):
        """
        Get works for each false artist.

        Parameters:
        - false_artists (list): List of false artists.

        Returns:
        - list: List of works for false artists.
        """
        artist_info = ArtistInfo()
        false_artists_works_options = []

        for false_artist in false_artists:
            false_artist_id = artist_info.fetch_artist_id(false_artist)
            if false_artist_id is not None:
                false_artist_works = artist_info.fetch_artist_works(false_artist_id)
                if false_artist_works:
                    false_work = random.choice(false_artist_works)
                    false_artists_works_options.append(false_work)

        return false_artists_works_options

    def generate_question_random_mode(self):
        """
        Generate a quiz question in random mode.

        Returns:
        - list: List containing current artist, options, and correct work for the question.
        """
        artist_info = ArtistInfo()
        current_artist_works = None

        # Generate correct work
        while not current_artist_works:
            current_artist = artist_info.choose_current_artist()
            current_artist_id = artist_info.fetch_artist_id(current_artist)
            current_artist_works = artist_info.fetch_artist_works(current_artist_id)

        correct_work = random.choice(current_artist_works)

        # Generate false works
        false_works = []
        # Ensure two false options
        while len(false_works) < 2:
            false_works = self.generate_false_answers(current_artist)

        # Genrate three options
        options = [correct_work] + false_works
        random.shuffle(options)

        return [current_artist, options, correct_work]

    def generate_question_personal_mode(self, current_artist: str):
        """
        Generate a quiz question in personal mode.

        Parameters:
        - current_artist (str): The current artist for the quiz question.

        Returns:
        - list: List containing options and correct work for the question.
        """
        artist_info = ArtistInfo()

        # In personal mode, the current artist is provided as parameter
        # Generate correct option
        current_artist_id = artist_info.fetch_artist_id(current_artist)
        current_artist_works = artist_info.fetch_artist_works(current_artist_id)
        correct_work = random.choice(current_artist_works)

        # Generate 2 false options
        false_works = []
        while len(false_works) < 2:
            false_works = self.generate_false_answers(current_artist)

        # Generate three options
        options = [correct_work] + false_works
        random.shuffle(options)

        return [options, correct_work]

    def __eq__(self, other):
        """
        Compares two ArtistQuiz instances for equality.

        Parameters:
        - other (object): The object to compare with.

        Returns:
        - bool: True if the instances are equal, False otherwise.
        """
        if isinstance(other, ArtistQuiz):
            return self.base_url == other.base_url
        return False

    def __str__(self):
        """
        Returns a string representation of the ArtistQuiz instance.

        Returns:
        - str: String representation of the instance.
        """
        return f"ArtistQuiz(base_url={self.base_url})"
