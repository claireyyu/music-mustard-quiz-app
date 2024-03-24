'''
Yue Yu
CS 5001, Fall 2023
Final Project -- helpers

This program contains helper functions that help implement the webapp.
'''

import streamlit as st
import streamlit_lottie as st_lottie
import requests
import webbrowser
from models.artist_info import ArtistInfo


def display_header(page_title: str, page_icon: str):
    """
    Display the header configuration for the Streamlit page.

    Parameters:
    - page_title (str): The title of the page.
    - page_icon (str): The icon for the page.
    """
    st.set_page_config(page_title, page_icon, initial_sidebar_state="collapsed")


def load_lottieurl(url: str):
    """
    Load Lottie animation JSON data from a given URL.

    Parameters:
    - url (str): The URL to fetch the Lottie animation JSON.

    Returns:
    - dict or None: The Lottie animation JSON data if successful, None otherwise.
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def display_animation(lottie_url: str, animation_height: int, lottie_key: str):
    """
    Display a Lottie animation.

    Parameters:
    - lottie_url (str): The URL of the Lottie animation.
    - animation_height (int): The height of the animation.
    - lottie_key (str): The key for the Lottie animation.
    """
    lottie_json = load_lottieurl(lottie_url)
    st_lottie.st_lottie(lottie_json, height=animation_height, key=lottie_key)


def display_page_title(title_text: str):
    """
    Display a centered page title.

    Parameters:
    - title_text (str): The text for the page title.
    """
    st.markdown(f"<h1 style='text-align: center; color: black;'>{title_text}</h1>", unsafe_allow_html=True)
    st.write("---")


def redirect_link_button(artist_name: str, search_content: str):
    """
    Redirect to a link based on the selected search content.

    Parameters:
    - artist_name (str): The name of the artist.
    - search_content (str): The type of information to search for (profile, works, genre, events).
    """
    artist_info = ArtistInfo()
    artist_id = artist_info.fetch_artist_id(artist_name)

    if artist_id:
        musicbrainz_link = artist_info.generate_artist_link(artist_name, search_content)

        if musicbrainz_link:
            webbrowser.open(musicbrainz_link)
        else:
            st.error(f"Unable to fetch information for the artist: {artist_name}. Please check your spelling and retry with a valid artist name.")
    else:
        st.error(f"Unable to fetch information for the artist: {artist_name}. Please retry with a valid artist name.")


def display_link(url: str, text: str):
    """
    Display a hyperlink.

    Parameters:
    - url (str): The URL for the hyperlink.
    - text (str): The text to display for the hyperlink.
    """
    st.markdown(f"<a href='{url}' target='_self'>{text}</a>", unsafe_allow_html=True)


def redirect_link_with_data(url: str, link_text: str, data: dict):
    """
    Redirect to a link with additional data in the query parameters.

    Parameters:
    - url (str): The base URL for redirection.
    - link_text (str): The text to display for the hyperlink.
    - data (dict): Additional data to include in the query parameters.
    """
    key_value_pairs = []
    for key, value in data.items():
        key_value_string = f"{key}={value}"
        key_value_pairs.append(key_value_string)
    query_params = "&".join(key_value_pairs)

    link_html = f"<a href='{url}?{query_params}' target='_self'>{link_text}</a>"

    st.markdown(link_html, unsafe_allow_html=True)
