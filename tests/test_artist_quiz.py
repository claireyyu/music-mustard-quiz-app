'''
Yue Yu
CS 5001, Fall 2023
Final Project -- test.test_artist_quiz

This program contains pytest for models.artist_quiz.
'''

from unittest.mock import patch
import pytest
from models.random_mode_artists import random_mode_artists
from models.artist_info import ArtistInfo
from models.artist_quiz import ArtistQuiz


@pytest.fixture
def aq():
    return ArtistQuiz()


def test_artist_quiz_init(aq):
    assert aq.base_url == 'https://beta.musicbrainz.org/ws/2/'


def test_generate_false_answers(aq):
    current_artist = "TestArtist"
    #  Temporarily replace two methods in the ArtistInfo class (fetch_artist_id and fetch_artist_works) with mock objects. 
    with patch.object(ArtistInfo, 'fetch_artist_id', return_value='123'), \
            patch.object(ArtistInfo, 'fetch_artist_works', return_value=['Song 1', 'Song 2']):
        false_answers = aq.generate_false_answers(current_artist)
        assert len(false_answers) == 2


def test_generate_false_answers_remove_artist(aq):
    current_artist = "Oasis"  # "Oasis" is in random_mode_artists
    remaining_artists = random_mode_artists.copy()
    remaining_artists.remove(current_artist)
    with patch.object(ArtistInfo, 'fetch_artist_id', return_value='123'), \
            patch.object(ArtistInfo, 'fetch_artist_works', return_value=['Song 1', 'Song 2']):
        false_answers = aq.generate_false_answers(current_artist)
        assert len(false_answers) == 2
        assert current_artist not in remaining_artists


def test_generate_question_random_mode(aq):
    with patch.object(ArtistInfo, 'choose_current_artist', return_value='TestArtist'), \
            patch.object(ArtistInfo, 'fetch_artist_id', return_value='123'), \
            patch.object(ArtistInfo, 'fetch_artist_works', return_value=['Song 1', 'Song 2']):
        question = aq.generate_question_random_mode()
        current_artist, options, correct_work = question
        assert current_artist == 'TestArtist'
        assert len(options) == 3
        assert correct_work in options


def test_generate_question_personal_mode(aq):
    current_artist = "TestArtist"
    with patch.object(ArtistInfo, 'fetch_artist_id', return_value='123'), \
            patch.object(ArtistInfo, 'fetch_artist_works', return_value=['Song 1', 'Song 2']):
        question = aq.generate_question_personal_mode(current_artist)
        options, correct_work = question
        assert len(options) == 3
        assert correct_work in options


def test_eq_method_same_instance(aq):
    assert aq == aq


def test_eq_method_different_instance_type(aq):
    assert aq != "Not an ArtistQuiz instance"


def test_str_method(aq):
    str_representation = str(aq)
    assert str_representation.startswith("ArtistQuiz(base_url=")
