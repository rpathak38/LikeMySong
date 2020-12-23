#!/usr/bin/env python
# coding: utf-8

#import statements
from spotify_client import *
import numpy as np

#instantiate Spotify API Client Object (SAPICO)
client_id = 'bbd7a9b053844b45b1bbe801383e8b2b' # '' = your client_id
client_secret = '7d8cd9c307434f48b49264348e5c3d00' # '' = your client_secret
spotify = SpotifyAPI(client_id, client_secret)

#run methods on the SAPICO object (spotify)
user = '2Fxmhks0bxGSBdJ92vM42m'
client = spotify.get_track_audio_features(user)
features = ['valence', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'speechiness', 'tempo']
input_data = []
for feature in features:
    input_data.append(client[feature])
input_data = np.array(input_data)
print(input_data)