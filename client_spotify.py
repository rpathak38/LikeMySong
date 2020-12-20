### ADD CLIENT_SECRET FIELD FROM GOOGLE DOC ###

import requests
import json
import csv

# spotify developer account credentials ->  Google Docs

CLIENT_ID = "bbd7a9b053844b45b1bbe801383e8b2b"
CLIENT_SECRET = ""  # Google Docs 

AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

# Request header
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# base URL of all spotify endpoints
BASE_URL = 'https://api.spotify.com/v1/'


def get_track_data(track_id):
    return requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers).json()

def get_artist_data(artist_id):
    return requests.get(BASE_URL + 'artists/' + artist_id, headers = headers).json()

# returns a list of genres associated with artist
def get_artist_genre(artist_id):
    return get_artist_data(artist_id)['genres']

def print_json(x):
    print(json.dumps(x, indent=4))

# WILL IMPLEMENT
def get_artist_id(artist_name):
    pass

def genres_to_csv(csv_file):
    pass




### INCOMPLETE ###

def get_artist_id(artist_name, track_name):
    pass

def genres_to_csv(csv_directory):
    with open(csv_directory) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 1
        
        for row in csv_reader:
            for i in row:
                print(i)

            if line_count == 21:
                break
            
            line_count += 1
            print()
            
# replace whitespaces by %20
def get_query_string(string):
    return '%20'.join(string.split(' '))

### --- ###


# Tests
track_name = "Last Dance - Radio Edit"
artists = ["['Avicii']"]

# genres_to_csv("./names_classified_sorted-clusters.csv")
type = 'track'
limit = 1
query = "?q=" + get_query_string(track_name) + '&type=' + type + '&limit=' + str(limit)
result = requests.get(BASE_URL + 'search' + query, headers = headers).json()
artist_obj = result['tracks']['items'][0]['artists'][0]  ## may be multiple artists. Will need to iterate over list in that case.

artist_id = artist_obj['id'] 
artist_name = artist_obj['name']
artist_genres = get_artist_genre(artist_id)

print("id: ", artist_id)
print("name: ", artist_name)
print("genres: ", artist_genres)


#print(get_query_string("The Last Dancer"))

"""
# tests
id = '1gij27s31tFKcTHa8f1u4g'
x = get_track_data(id)
print_json(x)

cp_id = '4gzpq5DPGxSnKTe4SA8HAU'
y = get_artist_data(cp_id)
print_json(y)
"""