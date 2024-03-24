'''
Yue Yu
CS 5001, Fall 2023
Final Project -- pages.quiz_result

This program represents the result page of MusicMustard web application.
It contains a key feature: Quiz Result.
'''

import streamlit as st
from helpers import display_header, display_animation, display_page_title, display_link


# 1. Initialize the Page:
def initialize_result_page():
    """
    Initialize the result page with header, animation, and page title.
    """
    display_header(page_title="Quiz Result", page_icon="🥳")
    display_animation(lottie_url="https://lottie.host/89fc8e61-60dc-4a50-ae62-a63c182c6e86/r2frCUxYuE.json", animation_height=300, lottie_key="result")
    display_page_title(title_text="Here's Your Quiz Result 🥳")


# 2. Key Feature: Quiz Result
def display_quiz_result():
    """
    Display the quiz result based on the score retrieved from the URL parameters.
    """
    params = st.experimental_get_query_params()

    if "score" in params:

        score = int(params["score"][0])

        if score != 0:
            st.success(f"Congratulations! You were correct in {score}/3 questions!")
        st.subheader(f"Your latest score is {score}!")

    else:
        st.warning("You haven't taken the quiz yet. Take a quiz to see your result.")


# 3. Navigate to Other Pages
def navigate_to_other_pages():
    """
    Navigate to other pages with links to the quiz.
    """
    st.markdown("---")
    st.markdown("### ↩️")
    display_link("/quiz_page", "😎 Take Quiz")
    display_link("/app", "🎸 Explore Music")


def result_page():
    """
    This is the main function of quiz_result.
    """
    initialize_result_page()
    display_quiz_result()
    navigate_to_other_pages()


result_page()
