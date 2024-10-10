import csv
from storage.interface_storage import InterfaceStorage


class StorageCsv(InterfaceStorage):
    def __init__(self, file_path):
        """
        Initialize the StorageCsv with a file path.
        """
        self.file_path = file_path

    def storage_get_movies(self):
        """
        Load and return movies from the CSV file.

        Returns:
        --------
        dict:
            A dictionary where movie names are keys and their details (Year of release, Rating, Poster) are values.
        """
        movies: dict[str, dict[str, str]] = {}  # Declare the dictionary explicitly
        try:
            with open(self.file_path, "r") as file:
                reader = csv.DictReader(file)  # Ensure reader is seen as returning dictionaries
                for row in reader:
                    # Cast row as dictionary explicitly to avoid "unresolved attribute" errors
                    row: dict[str, str] = dict(row)

                    movie_name = row.get('../movie')  # Safely access movie name
                    if not movie_name:
                        continue  # Skip if the movie name is missing

                    # Safely access and handle missing data
                    year_of_release = row.get('Year of release', '')
                    rating = row.get('Rating', '')
                    poster = row.get('Poster', '')

                    # Only add the movie if we have valid data
                    if movie_name and year_of_release and rating:
                        movies[movie_name] = {
                            "Year of release": year_of_release,
                            "Rating": rating,
                            "Poster": poster
                        }
            return movies
        except FileNotFoundError:
            # Return an empty dictionary if the file does not exist
            return {}
        except IOError as e:
            print(f"An error occurred while reading the movies: {e}")
            return {}

    def storage_save_movies(self, movies):
        """
        Save the updated movie data back to the CSV file.

        Parameters:
        -----------
        movies : dict
            The movie data to be saved. The structure should be {movie_name: {infos...}}.
        """
        try:
            with open(self.file_path, "w", newline='') as file:
                fieldnames = ['Movie', 'Year of release', 'Rating', 'Poster']
                writer = csv.DictWriter(file, fieldnames=fieldnames)

                writer.writeheader()  # Write the CSV header (column names)
                for movie_name, movie_data in movies.items():
                    writer.writerow({
                        'Movie': movie_name,
                        'Year of release': movie_data.get('Year of release', ''),
                        'Rating': movie_data.get('Rating', ''),
                        'Poster': movie_data.get('Poster', '')
                    })
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


# storage = StorageCsv('data.csv')
# print(storage.storage_get_movies())
