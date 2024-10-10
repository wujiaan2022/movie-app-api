from storage.storage_json import StorageJson

from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")
# print(f"API Key: {api_key}")

base_url = "http://www.omdbapi.com/"

url = f"{base_url}?apikey={api_key}&t={"Titanic"}"
# print(f"Fetching from URL: {url}")
response = requests.get(url)

if response.status_code == 200:
    # print(f"API response: {response.text}")  # Add this line to see the raw API response
    parsed = response.json()
    # print(parsed)

    title = parsed.get("Title", "Unknown Title")
    year = parsed.get("Year", "Unknown Year")
    rating = parsed.get("imdbRating", "Unknown Rating")
    poster = parsed.get("Poster", "Unknown Poster")

    storage = StorageJson('data_from_api.json')
    storage.storage_add_or_update_movie(title, year, rating, poster)
    print(f"Movie '{title}' added or updated successfully.")

else:
    print(f"Error fetching movie: {response.status_code}")
