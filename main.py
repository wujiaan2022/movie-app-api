from storage import storage_json
import movie_app
import requests
from dotenv import load_dotenv
import os
import json


# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")


# Main function to drive the program
def main():
    """
        Initializes the storage and movie app, then runs the application.

        This function creates an instance of the StorageJson class using
        the specified JSON file for storing movie data. It then creates
        an instance of the MovieApp class and calls its run method to
        start the program.
        """
    storage_json_1 = storage_json.StorageJson("data.json")
    movie_app_1 = movie_app.MovieApp(storage_json_1)
    movie_app_1.run()


if __name__ == "__main__":
    main()
