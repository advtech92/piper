# SHM_Spotify.py (Spotify Plugin)
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI

client_id = SPOTIPY_CLIENT_ID
client_secret = SPOTIPY_CLIENT_SECRET
redirect_uri = SPOTIPY_REDIRECT_URI

# Authentication with Spotify
def spotify_authenticate():
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='user-read-playback-state,user-modify-playback-state,playlist-read-private'
    )
    return spotipy.Spotify(auth_manager=sp_oauth)

# Function to handle Spotify commands
def handle_spotify_command(command_text, sp):
    command_text = command_text.lower()  # Convert to lowercase to simplify matching

    if "play music by" in command_text:
        artist_name = command_text.split("play music by")[-1].strip()
        results = sp.search(q=f'artist:{artist_name}', type='artist')
        if results['artists']['items']:
            artist_id = results['artists']['items'][0]['id']
            sp.start_playback(context_uri=f'spotify:artist:{artist_id}')
            print(f"Playing music by {artist_name}")
        else:
            print(f"Couldn't find artist: {artist_name}")
    elif "play the song" in command_text:
        song_name = command_text.split("play the song")[-1].strip()
        results = sp.search(q=f'track:{song_name}', type='track', limit=1)
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['uri']
            sp.start_playback(uris=[track_id])
            print(f"Playing the song {song_name}")
        else:
            print(f"Couldn't find the song: {song_name}")
    elif "play my playlist" in command_text:
        playlist_name = command_text.split("play my playlist")[-1].strip()
        playlists = sp.current_user_playlists(limit=50)  # Adjust limit as needed
        for playlist in playlists['items']:
            if playlist['name'].lower() == playlist_name.lower():
                sp.start_playback(context_uri=playlist['uri'])
                print(f"Playing your playlist {playlist_name}")
                break
        else:
            print(f"Couldn't find the playlist: {playlist_name}")
    elif "pause" in command_text:
        # Pause Spotify playback
        sp.pause_playback()
        print("Spotify playback paused.")
    elif "resume" in command_text or "play" in command_text and "song" not in command_text and "music by" not in command_text:
        # Resume Spotify playback
        sp.start_playback()  # This resumes playback if no context is provided
        print("Spotify playback resumed.")
    elif "next song" in command_text or "skip" in command_text:
        sp.next_track()
        print("Skipped to the next song.")
    elif "previous song" in command_text or "go back" in command_text:
        sp.previous_track()
        print("Went back to the previous song.")
    elif "set volume to" in command_text:
        volume_level = [int(s) for s in command_text.split() if s.isdigit()]
        if volume_level:
            sp.volume(volume_level[0])
            print(f"Volume set to {volume_level[0]}%.")
        else:
            print("Sorry, I couldn't understand the volume level.")
    elif "shuffle" in command_text:
        state = "true" if "on" in command_text else "false" if "off" in command_text else None
        if state is not None:
            sp.shuffle(state=state)
            print(f"Shuffle turned {'on' if state == 'true' else 'off'}.")
        else:
            print("Sorry, I couldn't understand the shuffle command.")
    elif "repeat" in command_text:
        state = "context" if "playlist" in command_text else "track" if "song" in command_text else "off"
        sp.repeat(state=state)
        print(f"Repeat mode set to {state}.")
