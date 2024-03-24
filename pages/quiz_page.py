'''
Yue Yu
CS 5001, Fall 2023
Final Project -- pages.quiz_page

This program represents the quiz page of MusicMustard web application.
It contains a key feature: Music Quiz.
'''


import streamlit as st
import random
from models.artist_info import ArtistInfo
from models.artist_quiz import ArtistQuiz
from helpers import display_header, display_animation, display_page_title, redirect_link_with_data, display_link


# 1. Initialize the Page:
def initialize_quiz_page():
    """
    Initialize the quiz page with header, animation, page title and session state.
    """
    display_header(page_title="Take Quiz", page_icon="😎")
    display_animation(lottie_url="https://lottie.host/b83a5bf4-8424-4a66-8597-8191627d4c5c/8BiLp5fksW.json", animation_height=300, lottie_key="quiz")
    display_page_title(title_text="Quiz Time 😎")

    # Initialize session state if not present
    if "quiz_started" not in st.session_state:
        st.session_state.quiz_started = False
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "user_answers" not in st.session_state:
        st.session_state.user_answers = [None] * 3  # only display 3 questions


# 2. Key Feature: Music Quiz
def take_music_quiz():
    """
    Key feature to take the music quiz with user input and selected mode.
    """
    quiz_mode = st.radio("✅Select Quiz Mode:", ["🤔 Random Mode", "🥰 Personal Mode"])

    if not st.session_state.quiz_started:
        start_quiz(quiz_mode)

    if st.session_state.quiz_started:
        display_quiz_questions()


# (1) Before quiz starts
def start_quiz(quiz_mode: str):
    """
    Start the quiz based on the selected mode.

    Parameters:
    - quiz_mode (str): The quiz mode chosen by the user.
    """
    if quiz_mode == "🤔 Random Mode":
        start_random_mode_quiz()

    elif quiz_mode == "🥰 Personal Mode":
        start_personal_mode_quiz()


# Random mode quiz initialization
def start_random_mode_quiz():
    """
    Start the quiz in random mode.
    """
    if st.button("💪 I am ready!"):
        st.caption("Please wait a sec. Generating Quiz...")
        st.session_state.quiz_started = True

        for _ in range(3):
            artist_quiz = ArtistQuiz()
            current_artist, options, correct_answer = artist_quiz.generate_question_random_mode()
            st.session_state.questions.append({"artist": current_artist, "options": options, "correct_answer": correct_answer})


# Personal mode quiz initialization
def start_personal_mode_quiz():
    """
    Start the quiz in personal mode.
    """
    user_artists_input = st.text_input("Enter at most three artists separated by commas:", key="user_artists_input")
    st.caption("Example 1: Radiohead")
    st.caption("Example 2: Radiohead, Oasis")
    st.caption("Example 3: Radiohead, Oasis, Catatonia")

    if st.button("🚀 Start"):
        st.caption("Please wait a sec. Generating Quiz...")

        cleaned_artists = [artist.strip() for artist in user_artists_input.split(",")]
        user_artists = cleaned_artists

        chosen_artists = choose_personal_mode_artists(user_artists)
        generate_quiz_questions(chosen_artists)


# Personal mode artist selection
def choose_personal_mode_artists(user_artists: list):
    """
    Choose artists for personal mode quiz.

    Parameters:
    - user_artists (list): A list of artists input from the user.
    """
    if len(user_artists) == 3:
        chosen_artists = user_artists
    elif len(user_artists) == 2:
        third_artist = random.choice(user_artists)
        chosen_artists = user_artists + [third_artist]
    elif len(user_artists) == 1:
        chosen_artists = user_artists * 3
    elif len(user_artists) > 3:
        st.warning("Please enter at most three artists.")
    elif len(user_artists) < 1:
        st.warning("Please enter at least one artist.")

    return chosen_artists


# Generate quiz questions for personal mode
def generate_quiz_questions(chosen_artists: list):
    """
    Generate quiz questions based on chosen artists.

    Parameters:
    - chosen_artists (list): A list of artists input chosen for the quiz.
    """
    artist_info = ArtistInfo()
    artist_quiz = ArtistQuiz()

    for artist in chosen_artists:
        artist_id = artist_info.fetch_artist_id(artist)
        artist_works = artist_info.fetch_artist_works(artist_id)

        if artist_id and artist_works:
            options, correct_answer = artist_quiz.generate_question_personal_mode(artist)
            st.session_state.questions.append({"artist": artist, "options": options, "correct_answer": correct_answer})
            st.session_state.quiz_started = True

        else:
            st.warning("Invalid Artist's Name Detected! Please Try Again!")
            st.session_state.quiz_started = False
            break


# (2) After quiz starts, display questions
def display_quiz_questions():
    """
    Display quiz questions after the quiz has started.
    """
    for i, question in enumerate(st.session_state.questions, start=1):
        display_question(i, question)

    if st.button("🤫Cheatsheet"):
        display_cheatsheet()

    if st.button("🎈Submit"):
        submit_quiz()


# Display individual quiz question
def display_question(question_number: int, question: dict):
    """
    Display an individual quiz question.

    Parameters:
    - question_number (int): The number of the question.
    - question (dict): Dictionary containing question details (artist, options, correct_answer).
    """
    st.header(f"Question {question_number}")
    st.subheader(f"{question['artist']} released:")

    for j, option in enumerate(question['options'], start=1):
        if j == 1:
            j = "A. "
        elif j == 2:
            j = "B. "
        elif j == 3:
            j = "C. "
        st.write(f"{j}{option}")

    user_answer = st.radio(f"Your choice for Question {question_number}:", question['options'], format_func=lambda x: str(x), key=f"question_{question_number}")  # ensures that options are all converted to strings before being displayed as radio button labels
    st.session_state.user_answers[question_number - 1] = user_answer  # e.g. the first question's answer would be at index 0


# Display the cheatsheet
def display_cheatsheet():
    """
    Display the cheatsheet with correct answers.
    """
    st.title("Hush! This is a cheatsheet 😃")
    for i, question in enumerate(st.session_state.questions, start=1):
        st.write(f"Question {i}")
        st.caption(f"Correct Answer: {question['correct_answer']}")
        st.write("---")


# Submit the quiz and calculate score
def submit_quiz():
    """
    Submit the quiz and calculate the score.
    """
    st.balloons()
    st.session_state.page = "quiz_result"

    answer_question_pairs = zip(st.session_state.user_answers, st.session_state.questions)

    total_score = 0
    for user_answer, question in answer_question_pairs:
        if user_answer == question['correct_answer']:
            total_score += 1

    next_page_url = "/quiz_result"
    link_text = "🥳 Quiz Result"
    data_to_pass = {"score": total_score}
    redirect_link_with_data(next_page_url, link_text, data_to_pass)


# 3. Navigate to Other Pages
def navigate_to_other_pages():
    """
    Navigate to other pages with links to the quiz.
    """
    st.markdown("---")
    st.markdown("### ↩️")
    display_link("/app", "🎸 Explore Music")


# MusicMustard quiz page
def quiz_page():
    """
    This is the main function of quiz_page.
    """
    initialize_quiz_page()
    take_music_quiz()
    navigate_to_other_pages()


quiz_page()
