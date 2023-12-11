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
   all_artists = soup.select(selector="li ul li span")
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

'''
with open("website.html") as file:
    contents = file.read()

soup = BeautifulSoup(contents, "html.parser")
# print(soup.title)
# print(soup.title.name) # -> title ( html tag name )
# print(soup.title.string) # -> Angela's Personal Site
# print(soup.prettify()) # -> prettify html
# print(soup.p) # -> first p tag
all_anchor_tags = soup.findAll(name="a")  # -> find all anchor "a" tags
# for tag in all_anchor_tags:
# print(tag.getText()) # -> all text in <a> tag
# print(tag.get("href")) # -> all href`s in <a> tag

# heading = soup.find(name="h1", id="name") # -> find FIRST <h1> tag with id=name
# print(heading)

section_heading = soup.find(name="h3", class_="heading")
# print(section_heading.getText()) # -> getText is method to get text inside tag
# print(section_heading.get("class")) # -> with get() method we can get tag class name
# print(section_heading.name)
# print(section_heading.string) # -> same as getText
company_url = soup.select_one(selector="p a")  # -> to select specify tag, we use as in CSS
print(company_url)
name = soup.select_one(selector="#name")  # -> using selectors id # like in CSS
print(name)
headings = soup.select(".heading")  # -> using selectors class . like in CSS
print(headings)'''
