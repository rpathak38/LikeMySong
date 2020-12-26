# import statements
import base64
import datetime
from urllib.parse import urlencode
import requests
import json
import csv


# Spotify API Client Object (SAPICO) definition
# Spotify API Developer Reference: https://developer.spotify.com/documentation/web-api/reference/
class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string (not bytes)
        """
        client_id = self.client_id
        client_secret = self.client_secret
        if client_secret == None or client_id == None:
            raise Exception("You must set client_id and client_secret")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())

        return client_creds_b64.decode()

    def get_token_headers(self):

        client_creds_b64 = self.get_client_credentials()
        return {
            "Authorization": f"Basic {client_creds_b64}"  # <base64 encoded client_id:client_secret>
        }

    def get_token_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def perform_auth(self):
        token_url = self.token_url
        token_data = self.get_token_data()
        token_headers = self.get_token_headers()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
            # return False
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.access_token_did_expire = expires < now
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def get_resource(self, lookup_id, resource_type='albums', version='v1'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_genre_seeds(self, version='v1', resource_type='recommendations', lookup_id='available-genre-seeds'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{lookup_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def get_genre_properties(self, genre, version='v1', resource_type='recommendations'):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}?seed_genres={genre}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    # Accessed Spotify Endpoint: albums (https://developer.spotify.com/documentation/web-api/reference/albums/)

    def get_album_data(self, _id):
        return self.get_resource(_id, resource_type='albums')

    # Accessed Spotify Endpoint: artists (https://developer.spotify.com/documentation/web-api/reference/artists/)

    def get_artist_data(self, _id):
        return self.get_resource(_id, resource_type='artists')

    # Spotify API reference link: https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/

    def get_artist_specific_data(self, _id, specific_artist_data='name'):
        return self.get_artist_data(_id)[specific_artist_data]

    # Accessed Spotify Endpoint: tracks (https://developer.spotify.com/documentation/web-api/reference/tracks/)

    def get_track_data(self, _id):
        return self.get_resource(_id, resource_type='tracks')

    # Spotify API reference link: https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/

    def get_track_specific_data(self, _id, specific_track_data='name'):
        return self.get_track_data(_id)[specific_track_data]

    def get_track_artists_id(self, _id):
        artists_id_arr = []
        artists_arr = self.get_track_specific_data(_id, specific_track_data='artists')
        for artist in range(0, len(artists_arr)):
            artists_id_arr.append(artists_arr[artist]['id'])
        return artists_id_arr

    # Spotify API reference link: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

    def get_track_audio_features(self, _id):
        return self.get_resource(_id, resource_type='audio-features')

    def get_track_specific_audio_feature(self, _id, specific_audio_feature='tempo'):
        return self.get_track_audio_features(_id)[specific_audio_feature]

    # Accessed Spotify Endpoint: search (https://developer.spotify.com/documentation/web-api/reference/search/search/)

    def base_search(self, query_params):  # type
        headers = self.get_resource_header()
        endpoint = "https://api.spotify.com/v1/search"
        lookup_url = f"{endpoint}?{query_params}"
        r = requests.get(lookup_url, headers=headers)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query=None, operator=None, operator_query=None, search_type='artist'):
        if query == None:
            raise Exception("A query is required")
        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k, v in query.items()])
        # OR or NOT are two operators
        if operator != None and operator_query != None:
            if operator.lower() == "or" or operator.lower() == "not":
                operator = operator.upper()
                if isinstance(operator_query, str):
                    query = f"{query} {operator} {operator_query}"
        query_params = urlencode({"q": query, "type": search_type.lower()})
        print(query_params)
        return self.base_search(query_params)

    # SPECIALIZED METHODS

    def specialized_distinct_artists_genres_from_track_id(self, _id):
        artists_id_arr = self.get_track_artists_id(_id)
        artists_genre_arr = []
        single_artist_genre_arr = []
        for artist in range(0, len(artists_id_arr)):
            single_artist_genre_arr = self.get_artist_specific_data(artists_id_arr[artist],
                                                                    specific_artist_data='genres')
            for genre in single_artist_genre_arr:
                if (genre not in artists_genre_arr):
                    artists_genre_arr.append(genre)
        return artists_genre_arr
        # alternatively
        # for genre in single_artist_genre_arr:
        #     artists_genre_arr.append(genre)
        # return list(set(artists_genre_arr))

    def specialized_compile_unique_genres(self, genres_master_arr=[], track_id=''):
        artists_genre_arr = self.specialized_distinct_artists_genres_from_track_id(track_id)
        for x in range(0, len(artists_genre_arr)):
            if (artists_genre_arr[x] not in genres_master_arr):
                genres_master_arr.append(artists_genre_arr[x])

    def specialized_compile_track_ids_from_training_set(self):
        genres_master_arr = []
        '''with open("/tmp/data.csv", 'r') as music_file:
            music_reader  = csv.reader(music_file, delimiter = ",")
            headingRow = next(music_reader)
            for row in music_reader:
                self.specialized_compile_unique_genres(genres_master_arr = genres_master_arr, track_id=row[8])'''
        # x = ["1RUubW9fHtIYwjl588PrhZ", "5Ohxk2dO5COHF1krpoPigN"]
        x = []
        with open("/tmp/data.csv", 'r') as music_file:
            music_reader = csv.reader(music_file, delimiter=",")
            headingRow = next(music_reader)
            for i in range(0, 100):
                x.append(str(next(music_reader)[8]))
        for item in range(0, len(x)):
            self.specialized_compile_unique_genres(genres_master_arr=genres_master_arr, track_id=x[item])
        return genres_master_arr

    def write_to_csv(self, read_from_file_csv, write_to_file_csv_name, num_rows=10, version="v1"):
        """
        Note:  write_to_file_csv_name should not contain .csv extensions
        """
        headings = None
        master_data_with_genres = []

        try:
            with open(read_from_file_csv) as data_file:
                reader = csv.reader(data_file, delimiter=",")
                headings = next(data_file).split(',')

                line_count = 0
                for row in reader:
                    data = dict(zip(headings, row))
                    unique_track_genres_from_artists = spotify.specialized_distinct_artists_genres_from_track_id(
                        data['id'])

                    # adding genres data
                    data['genres'] = unique_track_genres_from_artists
                    master_data_with_genres.append(data)
                    line_count += 1

                    if line_count == num_rows:
                        break
        except:
            raise Exception(read_from_file_csv + " not in directory.")

        with open(write_to_file_csv_name + "_" + str(version) + ".csv", "w") as write_file:
            writer = csv.DictWriter(write_file, fieldnames=headings + ['genres'])
            writer.writeheader()
            writer.writerows(master_data_with_genres)
