from flask import Flask, request, render_template_string, send_from_directory
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Setup
app = Flask(__name__)

# Spotify setup (replace with your actual credentials)
client_id = "4c9cab2dc7b042c6abfa1480a9a53ceb"
client_secret = "2cfb4c67f2e84373b5cb03c1f7b1b5ff"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))

# Download sentiment analyzer
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()

# Read HTML file as template string
def get_html():
    with open("index.html", "r", encoding="utf-8") as file:
        return file.read()

# Sentiment to mood
def detect_mood(text):
    score = sid.polarity_scores(text)["compound"]
    if score >= 0.05:
        return "happy"
    elif score <= -0.05:
        return "sad"
    else:
        return "relaxing"

# Get songs from Spotify
def get_songs(mood):
    results = sp.search(q=f"{mood} music", type="track", limit=5)
    tracks = results['tracks']['items']
    return [track['external_urls']['spotify'] for track in tracks]
    return [f"https://open.spotify.com/embed/track/{track['id']}" for track in tracks]

# Route for CSS
@app.route("/style.css")
def serve_css():
    return send_from_directory(".", "style.css")

# Main page
@app.route("/", methods=["GET", "POST"])
def index():
    song_links = []
    if request.method == "POST":
        mood_input = request.form.get("mood", "")
        mood = detect_mood(mood_input)
        song_links = get_songs(mood)

    return render_template_string(get_html(), song_links=song_links)

if __name__ == "__main__":
    app.run(debug=True)
