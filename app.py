from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Initialize Flask app
app = Flask(_name_)

# Initialize Spotipy (Spotify API client)
client_id = "4c9cab2dc7b042c6abfa1480a9a53ceb"  # Replace with your Spotify Client ID
client_secret = "2cfb4c67f2e84373b5cb03c1f7b1b5ff"  # Replace with your Spotify Client Secret
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Initialize NLTK sentiment analyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

def analyze_sentiment(text):
    sentiment = sid.polarity_scores(text)
    print(f"Sentiment Analysis Result: {sentiment}")  # Debug: Print sentiment result
    return sentiment

def search_spotify(query):
    # Search Spotify for the mood
    results = sp.search(q=query, limit=5, type='track')
    print(f"Search Results: {results}")  # Debug: Print raw search results
    tracks = results['tracks']['items']
    song_links = [f"https://open.spotify.com/track/{track['id']}" for track in tracks]
    return song_links

@app.route("/", methods=["GET", "POST"])
def index():
    song_links = []
    if request.method == "POST":
        mood = request.form['mood']
        sentiment = analyze_sentiment(mood)

        if sentiment['compound'] >= 0.05:
            query = "happy"
        elif sentiment['compound'] <= -0.05:
            query = "sad"
        else:
            query = "neutral"

        song_links = search_spotify(query)

    return render_template("index.html", song_links=song_links)


if _name_ == "__main__":
    app.run(debug=True)
