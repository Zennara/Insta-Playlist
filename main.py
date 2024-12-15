import os
import time

from dotenv import load_dotenv
from instagrapi import Client
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Load environment variables
load_dotenv()

# Instagram credentials
instagram_username = os.getenv("IG_USERNAME")
instagram_password = os.getenv("IG_PASSWORD")

# Spotify credentials
spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
spotify_redirect_uri = os.getenv("SPOTIFY_REDIRECT_URI")
spotify_playlist_id = os.getenv("SPOTIFY_PLAYLIST_ID")  # Playlist ID to add songs to

tracked_users = os.getenv("TRACKED_USERS").split(",")  # List of Instagram usernames to track

# Initialize Instagram client
cl = Client()
cl.login(instagram_username, instagram_password)

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret,
    redirect_uri=spotify_redirect_uri,
    scope="playlist-modify-private"
))


def event_loop():
    while True:
        fetch_notes()
        time.sleep(3600) # Fetch notes every hour


def fetch_notes():
    """Fetch Instagram Notes and add songs to a Spotify playlist."""
    for note in cl.get_notes():
        if not is_tracked_user(note.user.username):
            continue

        if is_music_note(note):
            print(note)
            song_name, artist_name, other_text = extract_music_note_details(note)
            print(f"Song: {song_name}")
            print(f"Artist: {artist_name}")
            print(f"Other Text: {other_text}")

            # Add the song to the Spotify playlist
            add_song_to_spotify(song_name, artist_name)


def is_music_note(note):
    """Check if the note is a music note."""
    if note.text.startswith("🎵"):
        return True


def extract_music_note_details(note):
    """Extract song and artist details from the note."""
    note_text = note.text
    note_text = note_text.replace("🎵", "")
    note_text = note_text.strip()

    song_artist_note = note_text.split("\n")

    other_text = song_artist_note[1] if len(song_artist_note) > 1 else ""

    song_artist = song_artist_note[0].split(" · ")
    song_name = song_artist[1] if len(song_artist) > 1 else ""
    artist_name = song_artist[0]

    return song_name, artist_name, other_text


def add_song_to_spotify(song_name, artist_name):
    """Search for a song on Spotify and add it to the playlist."""
    query = f"{song_name} {artist_name}"
    results = sp.search(q=query, type="track", limit=1)

    if results["tracks"]["items"]:
        track_id = results["tracks"]["items"][0]["id"]
        track_name = results["tracks"]["items"][0]["name"]
        print(f"Adding '{track_name}' to Spotify playlist.")
        sp.playlist_add_items(spotify_playlist_id, [track_id])
    else:
        print(f"Song '{song_name}' by '{artist_name}' not found on Spotify.")


def is_tracked_user(username):
    """Check if the user is in the tracked users list."""
    return username in tracked_users


# Run the script
event_loop()
