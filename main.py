# for whatever reason it works when you run it twice
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
import math
import time
import spotipy.util as util

username = "*"
client_id = '*'
client_secret = '*'
redirect_uri = 'http://localhost:8080'

scope = "playlist-modify-public"
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

if token:
    sp = spotipy.Spotify(auth=token)
else:
    print("Can't get token for", username)
playlists = (sp.current_user_playlists())

playlist_names = []
playlist_ids = []
for i in range(len(playlists['items'])):
    playlist_names.append(playlists["items"][i]["name"])
    playlist_ids.append(playlists["items"][i]["id"])

# from each playlist, need to get name (for human simplicity) + the id, which we can use to add to the final playlist
playlist_info = []
for i in range(len(playlist_names)):
    playlist_info.append(sp.playlist(playlist_ids[i]))

playlist_tracks = []
track_ids = []

for i in range(len(playlist_info)):
    for j in range(len(playlist_info[i]["tracks"]["items"])):
        playlist_tracks.append(playlist_info[i]["tracks"]["items"][j]["track"]["name"])
        track_ids.append(playlist_info[i]["tracks"]["items"][j]["track"]["id"])

playlist_tracks = list(dict.fromkeys(playlist_tracks))

track_ids = list(dict.fromkeys(track_ids))
title = "All Tracks"

split_up_tracks = {}
for i in range(math.ceil((len(track_ids) / 100))):
    try:
        split_up_tracks[i] = track_ids[i * 100:i * 100 + 100]
    except:
        split_up_tracks[i] = track_ids[i * 100:]

if title in playlist_names:
    index = playlist_names.index(title)
    sp.user_playlist_replace_tracks(username, playlist_ids[index], split_up_tracks[0])
    for i in range(math.ceil((len(track_ids) / 100))-1):
        sp.user_playlist_add_tracks(username, playlist_ids[0], split_up_tracks[i+1], position=None)


else:
    sp.user_playlist_create(username, title, public=True)

    playlists = sp.current_user_playlists()
    for i in range(len(playlists['items'])):
        playlist_names.append(playlists["items"][i]["name"])
        playlist_ids.append(playlists["items"][i]["id"])

    for i in range(math.ceil((len(track_ids) / 100))):
        sp.user_playlist_add_tracks(username, playlist_ids[0], split_up_tracks[i], position=None)


