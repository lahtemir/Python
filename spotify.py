from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


SPOTIPY_CLIENT_ID = os.environ.get("CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("CLIENT_SECRET")


# Getting top 100 songs from billboard on wanted date

URL = "https://www.billboard.com/charts/hot-100/"

date = input("Which year you would like to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(URL + date)
billboard = response.text
soup = BeautifulSoup(billboard, "html.parser")
results = soup.find("div", class_="chart-results-list")
rows = results.find_all(class_="o-chart-results-list-row-container")

song_names = [((row.find("h3", id="title-of-a-story", class_="c-title")).getText()).strip() for row in rows]

year = date.split("-")[0]
print(year)


# Getting the songs from Spotify

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]

song_uris=[]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


# CREATE PLAYLIST
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

# ADD TO PLAYLIST
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
