from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import os
BILLBOARD_HOT_URL = "https://www.billboard.com/charts/hot-100"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
def main():
   date_range = input("Which year do you want to travel to? Type date in this format YYYY-MM-DD ")
   response = requests.get(f"{BILLBOARD_HOT_URL}/{date_range}")
   soup = BeautifulSoup(response.text,"html.parser")
   all_songs = soup.select(selector="li ul li h3")
   top_songs = [song.getText().strip() for song in all_songs]
   print(top_songs)
   #Spotipy
   sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                                  client_secret=CLIENT_SECRET,
                                                  redirect_uri="http://example.com",
                                                  scope="playlist-modify-private"))
   result = sp.current_user()
   USER_ID=result["id"]
   uris = [sp.search(song)['tracks']['items'][0]['uri'] for song in top_songs]
   playlist_id = sp.user_playlist_create(user=USER_ID,name=f"{date_range}-Billboard 100",public=False,description="100DaysOfCode")["id"]
   sp.playlist_add_items(playlist_id=playlist_id,items=uris)
main()

