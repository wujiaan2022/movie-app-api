# from movie_app import MovieApp
# from storage.storage_json import StorageJson
#
# storage = StorageJson('data.json')
# movie_app = MovieApp(storage)
# movie_app.run()
#
# from movie_app import MovieApp
# from storage.storage_csv import StorageCsv
#
# storage = StorageCsv('data.csv')
# movie_app = MovieApp(storage)
# movie_app.run()

from movie_app import MovieApp
from storage.storage_json import StorageJson
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")
# print(f"API Key: {api_key}")

base_url = "http://www.omdbapi.com/"

url = f"{base_url}?apikey={api_key}&t={"Titanic"}"
# print(f"Fetching from URL: {url}")

base_url = "http://www.omdbapi.com/"

storage = StorageJson('data_from_api.json')
movie_app = MovieApp(storage)
storage = StorageJson('data_from_api.json')
movie_app.add_movie_from_api(base_url, api_key)



