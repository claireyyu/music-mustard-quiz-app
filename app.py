'''
Yue Yu
CS 5001, Fall 2023
Final Project -- app

This program represents the home page of MusicMustard web application.
It contains a key feature: Explore Artists.
'''

import streamlit as st
from helpers import display_header, display_animation, display_page_title, redirect_link_button, display_link


# 1. Initialize the Page:
def initialize_page():
    """
    Initialize the MusicMustard home page with header, animation, and page title.
    """
    display_header(page_title="MusicMustard", page_icon="🎸")
    display_animation(lottie_url="https://lottie.host/f3a74b44-f2c7-41da-8171-8f716f1ce0c0/JKhG2YIzuU.json", animation_height=300, lottie_key="music")
    display_page_title(title_text="MusicMustard 🎸")


# 2. Key Feature: Explore Artists
def explore_artists():
    """
    Key feature to explore artists with user input and selected filters.
    """
    st.markdown("### 🎵 Explore Artist Here")
    artist_name = st.text_input("Enter Artist's Name:")
    st.caption('Try: The Beatles')

    available_filters = ["Profile", "Works", "Genre", "Events"]
    selected_filters = st.multiselect("Select Artist's Info:", available_filters)

    if st.button("🌟Explore"):
        explore_artist_links(artist_name, selected_filters)


def explore_artist_links(artist_name: str, selected_filters: list):
    """
    Redirect to links based on the selected filters.

    Parameters:
    - artist_name (str): The name of the artist to explore.
    - selected_filters (list): List of selected filters.
    """
    if artist_name:
        for search_content in selected_filters:
            search_content_lower = search_content.lower()
            redirect_link_button(artist_name, search_content_lower)
    else:
        st.warning("Please enter the artist's name.")


# 3. Navigate to Other Pages
def navigate_to_other_pages():
    """
    Navigate to other pages with links to the quiz.
    """
    st.write("---")
    st.markdown("### Start Your Quiz Here ✊")
    display_link("/quiz_page", "😎 Take Quiz")
    display_link("/quiz_result", "🥳 Quiz Result")


# MusicMustard home page
def app():
    """
    This is the main function of app.
    """
    initialize_page()
    explore_artists()
    navigate_to_other_pages()


app()
