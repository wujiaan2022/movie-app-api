import json
from interface_storage import InterfaceStorage


class StorageJson(InterfaceStorage):
    def __init__(self, file_path):
        """
        Initialize the StorageJson with a file path.
        """
        self.file_path = file_path

    def storage_get_movies(self):
        """
        Load and return movies from the JSON file.

        Returns:
        --------
        dict:
            A dictionary of movies from the JSON file.
        """
        try:
            with open(self.file_path, "r") as file:
                movies = json.load(file)
            return movies
        except FileNotFoundError:
            # Return an empty dictionary if the file does not exist
            return {}

    def storage_save_movies(self, movies):
        """
        Save the updated movie data back to the JSON file.

        Parameters:
        -----------
        movies : dict
            The movie data to be saved.
        """
        try:
            with open(self.file_path, "w") as file:
                json.dump(movies, file, indent=4)  # Save the updated movies
        except IOError as e:
            print(f"An error occurred while saving the movies: {e}")

    def storage_add_or_update_movie(self, title, year, rating, poster):
        """
        Add or update a new movie to the storage.

        Parameters:
        -----------
        title : str
            The title of the movie.
        year : int
            The year the movie was released.
        rating : float
            The movie's rating.
        poster : str
            The URL or path to the movie's poster.
        """
        movies = self.storage_get_movies()
        movies[title] = {
            "Year of release": year,
            "Rating": rating,
            "Poster": poster
        }
        self.storage_save_movies(movies)  # Save the updated movies

    def storage_delete_movie(self, title):
        """
        Deletes a movie from the storage.

        Parameters:
        -----------
        title : str
            The title of the movie to delete.
        """
        movies = self.storage_get_movies()

        if title in movies:
            del movies[title]
            self.storage_save_movies(movies)
            print(f"Movie '{title}' has been deleted.")
        else:
            print(f"Movie '{title}' does not exist. No changes made.")


# storage = StorageJson('data.json')
# print(storage.storage_get_movies())
