import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup
import requests

# Spotify API credentials
SPOTIFY_CLIENT_ID = 'YOUR_SPOTIFY_CLIENT_ID'
SPOTIFY_CLIENT_SECRET = 'YOUR_SPOTIFY_CLIENT_SECRET'
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/callback'

# Authenticate with Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri=SPOTIFY_REDIRECT_URI,
                                               scope="playlist-read-private"))

# Spotify playlist URL
playlist_url = 'SPOTIFY_PLAYLIST_URL'

# Extract song names from the Spotify playlist
def get_song_names(playlist_url):
    playlist_id = playlist_url.split('/')[-1]
    results = sp.playlist_tracks(playlist_id)
    song_names = [item['track']['name'] for item in results['items']]
    return song_names

# Search for YouTube URLs for each song using Beautiful Soup
def search_youtube_urls(song_names):
    youtube_urls = []
    for song_name in song_names:
        query = '+'.join(song_name.split())
        search_url = f"https://www.youtube.com/results?search_query={query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href.startswith('/watch'):
                youtube_urls.append(href)
                break  # Only take the first search result
    return youtube_urls

# Generate full YouTube URLs
def generate_full_youtube_urls(youtube_urls):
    full_youtube_urls = ['https://www.youtube.com' + url for url in youtube_urls]
    return full_youtube_urls

def main():
    song_names = get_song_names(playlist_url)
    youtube_urls = search_youtube_urls(song_names)
    full_youtube_urls = generate_full_youtube_urls(youtube_urls)
    
    for url in full_youtube_urls:
        print(url)

if __name__ == "__main__":
    main()
