import os

from dotenv import load_dotenv
from instagrapi import Client


load_dotenv()
cl = Client()
username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

# Login to Instagram
cl.login(username, password)


def fetch_notes():
    for note in cl.get_notes():
        if is_music_note(note):
            song_name, artist_name, other_text = extract_music_note_details(note)
            print(f"Song: {song_name}")
            print(f"Artist: {artist_name}")
            print(f"Other Text: {other_text}")


def is_music_note(note):
    if note.text.startswith("🎵"):
        return True


def extract_music_note_details(note):
    note_text = note.text
    note_text = note_text.replace("🎵", "")
    note_text = note_text.strip()

    song_artist_note = note_text.split("\n")

    other_text = song_artist_note[1]

    song_artist = song_artist_note[0].split(" · ")
    artist_name = song_artist[1]
    song_name = song_artist[0]

    return song_name, artist_name, other_text


fetch_notes()
