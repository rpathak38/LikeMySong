from typing import List
from spotify_client import SpotifyAPI


class Song(object):
    client_id = 'bbd7a9b053844b45b1bbe801383e8b2b'  # '' = your client_id
    client_secret = '7d8cd9c307434f48b49264348e5c3d00'  # '' = your client_secret
    spotify = SpotifyAPI(client_id, client_secret)

    def __init__(self, _id):
        self._id = _id
        # self._artist = Song.spotify.get_track_artists(_id)
        self._genres = Song.spotify.specialized_distinct_artists_genres_from_track_id(_id)
        self._similarity = 0

    @property
    def genres(self):
        return self._genres

    @property
    def similarity(self):
        return self._similarity
