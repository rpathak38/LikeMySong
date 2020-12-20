import requests

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
    return requests.get(BASE_URL + 'audio-features/' + track_id, headers=headers)

def get_artist_data(artist_id):
    return requests.get(BASE_URL + 'artists/' + artist_id, headers = headers)
