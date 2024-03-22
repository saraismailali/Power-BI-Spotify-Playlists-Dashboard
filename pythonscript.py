import requests
import pandas as pd

def get_spotify_token(client_id, client_secret):
    try:
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        })
        auth_data = auth_response.json()
        if 'access_token' in auth_data:
            return auth_data['access_token']
        else:
            print("Error: Access token not found. Authentication failed.")
            return None
    except Exception as e:
        print(f"Error in get_spotify_token: {e}")
        return None

def search_track(track_name, artist_name, token):
    try:
        query = f"{track_name} artist:{artist_name}"
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(url, headers={
            'Authorization': f'Bearer {token}'
        })
        if response.status_code != 200:
            print(f"Failed to search track: {response.status_code} - {response.text}")
            return None
        json_data = response.json()
        first_result = json_data.get('tracks', {}).get('items', [])[0]
        if first_result:
            track_id = first_result.get('id')
            return track_id
        else:
            print("No track found.")
            return None
    except Exception as e:
        print(f"Error in search_track: {e}")
        return None

def get_track_details(track_id, token):
    try:
        url = f"https://api.spotify.com/v1/tracks/{track_id}"
        response = requests.get(url, headers={
            'Authorization': f'Bearer {token}'
        })
        if response.status_code != 200:
            print(f"Failed to get track details: {response.status_code} - {response.text}")
            return None
        json_data = response.json()
        image_url = json_data.get('album', {}).get('images', [])[0].get('url')
        return image_url
    except Exception as e:
        print(f"Error in get_track_details: {e}")
        return None

# Replace 'your_client_id' and 'your_client_secret' with your actual client ID and secret
client_id = 'a27866714d8c42179ec22b5618a5dcd0'
client_secret = 'ff49da87ffb945e9a954c4abde309d5c'

access_token = get_spotify_token(client_id, client_secret)
if not access_token:
    print("Failed to get Spotify access token. Exiting.")
    exit()

# Read the CSV file containing track names and artist names
try:
    df_spotify = pd.read_csv('spotify.csv', encoding='ISO-8859-1')
except Exception as e:
    print(f"Error reading CSV file: {e}")
    exit()

# Iterate over each row in the DataFrame
def search_track(track_name, artist_name, token):
    try:
        query = f"{track_name} artist:{artist_name}"
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(url, headers={
            'Authorization': f'Bearer {token}'
        })
        if response.status_code != 200:
            print(f"Failed to search track: {response.status_code} - {response.text}")
            return None
        json_data = response.json()
        items = json_data.get('tracks', {}).get('items', [])
        if not items:
            print("No track found.")
            return None
        first_result = items[0]
        track_id = first_result.get('id')
        return track_id
    except Exception as e:
        print(f"Error in search_track: {e}")
        return None


# Save the updated DataFrame to a CSV file
try:
    df_spotify.to_csv('updated_file.csv', index=False)
    print("CSV file updated successfully.")
except Exception as e:
    print(f"Error saving CSV file: {e}")

