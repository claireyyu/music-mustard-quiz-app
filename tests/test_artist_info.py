'''
Yue Yu
CS 5001, Fall 2023
Final Project -- test.test_artist_info

This program contains pytest for models.artist_info.
'''

import pytest
import requests
from models.artist_info import ArtistInfo
from models.random_mode_artists import random_mode_artists
from unittest.mock import patch


@pytest.fixture
def ai():
    return ArtistInfo()


def test_artist_info_init(ai):
    assert ai.base_url == 'https://beta.musicbrainz.org/ws/2/'


def test_choose_current_artist(ai):
    current_artist = ai.choose_current_artist()
    assert current_artist in random_mode_artists


def test_fetch_artist_id_success(ai):
    artist_name = "TestArtist"
    with patch('models.artist_info.requests.get') as mock_get:
        # return a mock JSON response
        mock_get.return_value.json.return_value = {'artists': [{'id': '123'}]}
        artist_id = ai.fetch_artist_id(artist_name)
        assert artist_id == "123"


def test_fetch_artist_id_empty_result(ai):
    artist_name = "NonExistentArtist"
    with patch('models.artist_info.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'artists': []}
        artist_id = ai.fetch_artist_id(artist_name)
        assert artist_id is None


def test_fetch_artist_id_no_artists_key(ai):
    artist_name = "NonExistentArtist"
    with patch('models.artist_info.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {}
        artist_id = ai.fetch_artist_id(artist_name)
        assert artist_id is None


def test_fetch_artist_id_exception(ai):
    artist_name = "TestArtist"
    with patch('models.artist_info.requests.get') as mock_get:
        # Configures the mock get method to raise a requests.exceptions.ConnectionError when it is called
        mock_get.side_effect = requests.exceptions.ConnectionError
        artist_id = ai.fetch_artist_id(artist_name)
        assert artist_id is None


def test_fetch_artist_works_success(ai):
    artist_id = '123'
    with patch('models.artist_info.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'works': [{'title': 'Song 1'}, {'title': 'Song 2'}]}
        artist_works = ai.fetch_artist_works(artist_id)
        assert artist_works == ['Song 1', 'Song 2']


def test_fetch_artist_works_empty_result(ai):
    artist_id = '123'
    with patch('models.artist_info.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'works': []}
        artist_works = ai.fetch_artist_works(artist_id)
        assert artist_works == []


def test_fetch_artist_works_no_works_key(ai):
    artist_id = '123'
    with patch('models.artist_info.requests.get') as mock_get:
        mock_get.return_value.json.return_value = {}
        artist_works = ai.fetch_artist_works(artist_id)
        assert artist_works is None


def test_fetch_artist_works_exception(ai):
    artist_id = '123'
    with patch('models.artist_info.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.ConnectionError
        artist_works = ai.fetch_artist_works(artist_id)
        assert artist_works is None


def test_generate_artist_link_valid_search_content(ai):
    artist_name = "TestArtist"
    search_content = "profile"
    # Uses the patch context manager from the unittest.mock module to temporarily replace the fetch_artist_id method in the ArtistInfo class with a mock object
    # This is done to control and simulate the behavior of the fetch_artist_id method during the test
    with patch('models.artist_info.ArtistInfo.fetch_artist_id') as mock_fetch_artist_id:
        mock_fetch_artist_id.return_value = "123"
        musicbrainz_link = ai.generate_artist_link(artist_name, search_content)
        expected_link = "https://beta.musicbrainz.org/artist/123"
        assert musicbrainz_link == expected_link


def test_generate_artist_link_fetch_id_none(ai):
    artist_name = "NonExistentArtist"
    search_content = "profile"
    with patch('models.artist_info.ArtistInfo.fetch_artist_id') as mock_fetch_artist_id:
        mock_fetch_artist_id.return_value = None
        musicbrainz_link = ai.generate_artist_link(artist_name, search_content)
        assert musicbrainz_link is None


def test_eq_method_same_instance(ai):
    assert ai == ai


def test_eq_method_different_instance():
    ai1 = ArtistInfo()
    ai2 = ArtistInfo()
    assert ai1 == ai2


def test_eq_method_different_instance_type(ai):
    assert ai != "Not an ArtistInfo instance"


def test_str_method(ai):
    str_representation = str(ai)
    assert str_representation == "ArtistInfo(base_url=https://beta.musicbrainz.org/ws/2/)"
