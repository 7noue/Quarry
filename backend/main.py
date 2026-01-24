import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import json
import requests
import time

load_dotenv()
scope = "user-read-recently-played user-top-read user-library-read"

# CONFIG
CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    print("❌ Error: Missing .env variables.")
    exit(1)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=scope,
    open_browser=False
))

user = sp.current_user()
print(f"Connected as: {user['display_name']}")


def get_apple_preview(artist, track):
    """Public iTunes Search API - No Token Needed"""
    try:
        query = f"{artist} {track}"
        url = f"https://itunes.apple.com/search?term={query}&media=music&entity=song&limit=1&country=PH"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            results = res.json().get('results', [])
            return results[0].get('previewUrl') if results else None
    except: return None
    return None


def fetch_hybrid_deck_range(time_range='short_term', limit=50):
    print("🟢 Fetching Spotify Top Tracks...")
    results = sp.current_user_top_tracks(limit=limit, time_range=time_range)
    
    deck = []
    for item in results['items']:
        name, artist = item['name'], item['artists'][0]['name']
        print(f"🔍 Finding Audio: {artist} - {name}...", end=" ")

        preview = get_apple_preview(artist, name)
        
        if preview:
            deck.append({
                "id": item['id'],
                "title": name,
                "artist": artist,
                "album": item['album']['name'],
                "previewUrl": preview,
                "provider": "apple-itunes"
            })
            print("✅")
        else:
            print("❌ (No Audio Found)")
        
        if len(deck) >= 10: break
        time.sleep(0.2) # Avoid aggressive rate limiting
    return deck

if __name__ == "__main__":
   data = fetch_hybrid_deck_range()
if data:
    out = os.path.join(os.path.dirname(__file__), "../web/src/lib/data/starting_pack.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as f: json.dump(data, f, indent=2)
    print(f"\n🚀 SHIP IT: {len(data)} tracks ready in {out}")