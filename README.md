# Music Mustard - A Fun Quiz Web App

## 1. Application Summary

The MusicMustard web application provides a platform for music lovers to explore music metadata, assess their knowledge about random or personalized artists through fun quizzes, and check their quiz results. Users can also discover new songs and expand their music playlists when enjoying the quiz.


### The three key features are:

**(1) Explore Artists**

Users can input an artist's name, use a multi-select filter to choose search content, and get redirected to MusicBrainz pages of artist's profile, works, genre and events.


**(2) Music Quiz**

Users can take a three-question quiz on artists and their musical works. Two modes are provided: random mode and personal mode. 

In random mode, users get questions generated using a predefined list of artists; In personal mode, users firstly enter at most three artists separated by commas, and then get questions generated using the input artists.

During the quiz, sers can refer to a cheatsheet. After the quiz, the result will be passed to the next page.


**(3) Quiz Result**

After completing a quiz, users can view their latest score. If they haven't taken any quiz, they will see navigation to the quiz.


## 2. REST API: MusicBrainz

**(1) URL:** https://musicbrainz.org/ws/2/

**(2) Documentation:** https://beta.musicbrainz.org/doc/MusicBrainz_API

**(3) Description:** The MusicBrainz REST API can be used to fetch data of artist's ID and musical works,which can be used to generate quiz questions.

**(4) Endpoints:**
- `/ws/2/artist/?query=artist:\"<artist_name>\"&limit=1&fmt=json` - Retrieve a given artist's detailed information (including artist's ID)
- `/ws/2/work/?artist=<artist_id>&fmt=json` - Retrieve a given artist's list of works


## 3. List of Features

### (1) Explore Artists

**i. Description:** Users can input an artist's name, use a multi-select filter to choose search content, and get redirected to pages of the artist's profile, works, genre and events.

**ii. Data Class:**
- `artist_info`

**iii. MusicBrainz URL Endpoint:**
- `artist/<artist_id>` - Retrieve a given artist's profile
- `artist/<artist_id>/works` - Retrieve a given artist's works
- `artist/<artist_id>/tags` - Retrieve a given artist's genre
- `artist/<artist_id>/events` - Retrieve a given artist's events

**iv. Pages:**
- `app.py`

### (2) Music Quiz

**i. Description:** Users can take a three-question quiz on artists and their musical works. Two modes are provided: random mode and personal mode.

**ii. Data Class:**
- `artist_info`
- `artist_quiz`

**iii. REST API Endpoint:**
- `/ws/2/artist/?query=artist:\"<artist_name>\"&limit=1&fmt=json` - Retrieve a given artist's detailed information (including artist's ID)
- `/ws/2/work/?artist=<artist_id>&fmt=json` - Retrieve a given artist's list of works

**iv. Pages:**
- `quiz_page.py`


### (3) Quiz Result

**i. Description:** If users just finish a quiz, they can see their latest score; if users haven't taken any quiz, they can see navigation to the quiz.

**ii. Data Class:**
- N/A

**iii. REST API Endpoint:**
- N/A

**iv. Pages:**
- `quiz_result.py`

## 4. References

- [MusicBrainz API](https://beta.musicbrainz.org/doc/MusicBrainz_API)
- [Streamit API reference](https://docs.streamlit.io/library/api-reference)
  
## 5. Code highlights
```
    # models.artist_info.py

    def fetch_artist_id(self, artist_name: str) -> str or None:
        endpoint = "artist"
        query = f"?query=artist:\"{artist_name}\"&limit=1&fmt=json"
        url = f"{self.BASE_URL}{endpoint}/{query}"

        try:
            response = requests.get(url)
            data = response.json()
            artist_id = data.get('artists', [])[0].get('id', None)
            return artist_id
        
        ...
```

```
    # models.artist_quiz.py

    def generate_question_personal_mode(self, current_artist: str):
        artist_info = ArtistInfo()

        # Generate correct option
        current_artist_id = artist_info.fetch_artist_id(current_artist)
        current_artist_works = artist_info.fetch_artist_works(current_artist_id)
        correct_work = random.choice(current_artist_works)

        ...
```

```
    # helper.py

    def redirect_link_with_data(url: str, link_text: str, data: dict):
        key_value_pairs = []
        for key, value in data.items():
            key_value_string = f"{key}={value}"
            key_value_pairs.append(key_value_string)
        query_params = "&".join(key_value_pairs)
        
        ...
```

## 6. Next steps
- Pass questions and answers from quiz page to result page, and display the result as a table, with each correct answer (song) along with a link to its MusicBrainz page.
- Implement a user authentication system to track individual quiz scores and visualize score history.
- Add more personalized quiz mode options, such as timed quiz mode or collaborative quiz mode.
- Enhance the user interface for a more comfortable experience.


## 7. Reflection
In this project, I gained hands-on experience on how to use a framework to connect backend algorithms with frontend display, and how to apply object-oriented programming principles in a practical context. The most challenging part was to understand the structure of the fetched data and extract valuable information from it. Creating the music quiz feature was the most rewarding part, because I enjoy it a lot as a music fan. In the future, I would focus on passing complex data between different web pages and extracting information from passed data for visualization.
