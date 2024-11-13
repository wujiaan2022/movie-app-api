import random

from common import display_menu, exit_panel

from user_input import (get_valid_full_name, get_valid_partial_or_full_name, choose_add_or_not, get_valid_movie_infos,
                        get_valid_int, get_valid_filter_rating, get_valid_filter_year)
from utils import (display_sequence_movies, average, median, best_worst, display_close_matches_dict,
                   display_partial_matches)

from web_generate_from_api import generate_html

from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()


class MovieApp:
    def __init__(self, storage):
        """
        Initialize the MovieApp with a storage object.

        Args:
            storage: An instance of the StorageJson class that handles storing and
                     retrieving movie data.
        """
        self.storage = storage
        self.api_key = os.getenv("API_KEY")
        self.base_url = os.getenv("BASE_URL")

    def _display_list_movies(self):
        """
                Display the list of movies stored in the storage.

                Fetches all movies from the storage and displays them in a formatted sequence.
                If no movies are found, prints an appropriate message.
                """
        try:
            # get dictionary of movies from storage object,it is an instance object from class StorageJson,
            # which allows direct access to all the class methods inside the class StorageJson
            movies = self.storage.storage_get_movies()

            if movies:
                print(f"\n{len(movies)} movies in total\n")
                # Enumerate through the movies and start counting from 1
                display_sequence_movies(movies)
            else:
                print("No movies found.")
        except ValueError as ve:
            print(f"An error occurred in display_list_movie:{ve}")
        except KeyError as ke:
            print(f"An error occurred in display_list_movie:{ke}")
        except Exception as e:
            print(f"An unexpected error occurred in display_list_movie:{e}")

    def get_rest_save_all(self, movie_name, key_word):
        """
        Helper method to add additional movie information (year, rating, poster).

        Args:
            movie_name: The name of the movie being saved.
            key_word: Either 'added' or 'updated', used in the success message.
        """

        while True:
            try:
                year, rating, poster = get_valid_movie_infos()
                if str(year).lower() == "q" or str(rating).lower() == "q":
                    return False  # Exit and return failure if user quits

                # Save the movie and exit the loop
                self.storage.storage_add_or_update_movie(movie_name, year, rating, poster)
                print(f"Movie {movie_name} with year of release {year} and rating {rating}\n"
                      f"has been {key_word} successfully.")
                return True  # Return success after saving

            except ValueError as ve:
                print(f"An error occurred while adding movie details: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred while adding movie details: {e}")

    def _add_movie(self):
        """
                Add a new movie to the storage by prompting the user for the movie's name and details.

                This method checks if the movie already exists by searching for close matches in the
                movie list. If no matches are found, it proceeds to add the new movie.
                """

        movies = self.storage.storage_get_movies()

        if not movies:
            print("No movies found")
            return

        while True:
            try:
                movie_name = get_valid_partial_or_full_name()
                if movie_name == "q":
                    break

                # check name existence by checking close matches in the movie list
                close_matches = display_close_matches_dict(movie_name, movies)
                if close_matches:
                    answer = choose_add_or_not()

                    if answer == "m":
                        break  # go back to memu
                    elif answer == "n":
                        continue  # add a new movie name

                # any other key except for m and n meaning continue adding this movie
                self.get_rest_save_all(movie_name, "added")

                # Ask the user if they want to add another movie
                answer = input("Press any key to add another movie, 'q' for quit: ").strip().lower()
                if answer == "q":
                    break

            except Exception as e:
                print(f"An error occurred in add_movie: {e}")

    def _update_movie(self):
        """
                Update an existing movie in the storage by prompting the user to select a movie and modify its details.

                The user is shown close matches for the entered movie name and can select one to update.
                """

        movies = self.storage.storage_get_movies()

        while True:
            try:
                movie_name = get_valid_partial_or_full_name()

                if movie_name.lower() == "q":
                    break

                close_matches = display_close_matches_dict(movie_name, movies)

                print("Enter the sequence number of the movie to update.")
                selected_index = int(get_valid_int(close_matches))

                if selected_index == 0:
                    break

                movie_name = list(close_matches.keys())[selected_index - 1]

                self.get_rest_save_all(movie_name, "updated")

                # Ask the user if they want to add another movie
                continue_updating = input("Press any key to update another movie, 'q' for quit: ").strip().lower()
                if continue_updating == "q":
                    break

            except ValueError as ve:
                print(f"Value error occurred in update_movie: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred in update_movie: {e}")

    def _delete_movie(self):
        """
                Delete a movie from the storage by prompting the user to select a movie and confirm the deletion.

                The user is shown close matches for the entered movie name and can select one to delete.
                """
        movies = self.storage.storage_get_movies()

        if not movies:
            print("No movies found")
            return

        while True:
            try:
                movie_name = get_valid_partial_or_full_name()

                if movie_name.lower() == "q":
                    break

                close_matches = display_close_matches_dict(movie_name, movies)

                print("Enter the number of the movie to delete.")
                selected_index = int(get_valid_int(close_matches))

                if selected_index == 0:
                    break

                movie_name = list(close_matches.keys())[selected_index - 1]
                confirmation = input(f"Are you sure you want to delete '{movie_name}'? (y/n): ").strip().lower()
                if confirmation == 'y':
                    self.storage.storage_delete_movie(movie_name)
                    print(f"Movie '{movie_name}' has been deleted successfully!")

                continue_deleting = input("Press any key to delete another movie, or 'q' for quit: ").strip().lower()
                if continue_deleting == "q":
                    break

            except ValueError as ve:
                print(f"Value error occurred in delete_movie: {ve}")
            except Exception as e:
                print(f"An error occurred in delete_movie: {e}")

    def _show_status(self):
        """
                Display statistics about the movies, including average, median, and best/worst rated movies.
                """
        movies = self.storage.storage_get_movies()
        if not movies:
            print("No movies found")
            return
        try:
            average(movies)
            median(movies)
            best_worst(movies)
        except Exception as e:
            print(f"An error occurred in show_status: {e}")

    def _get_random_movie(self):
        """
                Select and display a random movie from the storage.
                """
        movies = self.storage.storage_get_movies()
        while True:
            try:
                random_movie = random.choice(list(movies.items()))
                print(f"The random movie is {random_movie[0]} with a rating of {random_movie[1]}")

                answer = input("Press any key to get another random movie, 'q' to quit: ").strip().lower()
                if answer == "q":
                    break

            except Exception as e:
                print(f"An error occurred in get_random_movie: {e}")

    def _search_movie(self):
        """
                Search for movies in the storage based on a partial or full name entered by the user.
                """
        movies = self.storage.storage_get_movies()
        while True:
            try:
                movie_name = get_valid_partial_or_full_name()

                if movie_name.lower() == "q":
                    break

                display_close_matches_dict(movie_name, movies)

                answer = input("Press any key to search another movie, 'q' to quit: ").strip().lower()
                if answer == "q":
                    break

            except Exception as e:
                print(f"An error occurred in search_movie: {e}")

    def _sort_rating(self):
        """
                Sort and display the movies based on their IMDb rating in descending order.
                """
        movies = self.storage.storage_get_movies()
        try:
            sorted_movies = sorted(movies.items(), key=lambda item: float(item[1]["Rating"]), reverse=True)
            print("Movies sorted by rating (highest to lowest):")
            sorted_dict = dict(sorted_movies)
            display_sequence_movies(sorted_dict)

        except ValueError as ve:
            print(f"Value error occurred in sort_ration: {ve}")
        except IndexError as ie:
            print(f"Index error occurred in sort_ration: {ie}")
        except KeyError as ke:
            print(f"Key error occurred in sort_ration: {ke}")
        except Exception as e:
            print(f"An error occurred in sort_rating: {e}")

    def _sort_year(self):
        """
                Sort and display the movies based on their year of release in descending order.
                """
        movies = self.storage.storage_get_movies()
        try:
            sorted_movies = sorted(movies.items(), key=lambda item: float(item[1]["Year of release"]), reverse=True)
            print("Movies sorted by year of release (highest to lowest):")
            sorted_dict = dict(sorted_movies)
            display_sequence_movies(sorted_dict)

        except ValueError as ve:
            print(f"Value error occurred in sort_year: {ve}")
        except IndexError as ie:
            print(f"Index error occurred in sort_year: {ie}")
        except KeyError as ke:
            print(f"Key error occurred in sort_year: {ke}")
        except Exception as e:
            print(f"An error occurred in sort_year: {e}")

    def _filter_movie(self):
        """
                Filter the movies based on a given rating, start year, and end year entered by the user.
                """
        movies = self.storage.storage_get_movies()
        while True:
            try:
                filter_rating = get_valid_filter_rating()

                if str(filter_rating).lower() == "q":
                    break

                if filter_rating is None:
                    rating_matches = movies

                else:
                    rating_matches = {movie: infos for movie, infos in movies.items()
                                      if float(infos["Rating"]) >= float(filter_rating)}

                print("\nEnter start year (leave blank for no start year).")
                filter_start_year = get_valid_filter_year()

                if str(filter_start_year).lower() == "q":
                    break

                if filter_start_year is None:
                    start_year_matches = rating_matches
                else:
                    start_year_matches = {movie: infos for movie, infos in rating_matches.items()
                                          if int(infos["Year of release"]) >= int(filter_start_year)}

                print("\nEnter end year (leave blank for no end year).")
                filter_end_year = get_valid_filter_year()

                if str(filter_end_year).lower() == "q":
                    break

                if filter_end_year is None:
                    end_year_matches = start_year_matches
                else:
                    end_year_matches = {movie: infos for movie, infos in start_year_matches.items()
                                        if int(infos["Year of release"]) <= int(filter_end_year)}

                display_sequence_movies(end_year_matches)

                answer = input("\nPress any key to filter other movies, or 'q' to quit: ").strip().lower()
                if answer == "q":
                    break

            except ValueError as ve:
                print(f"Type error occurred in filter_movie: {ve}.")
            except TypeError as te:
                print(f"Type error occurred in filter_movie: {te}.")
                break
            except KeyError as ke:
                print(f"Key error occurred in filter_movie: {ke}")
            except Exception as e:
                print(f"An error occurred in filter_movie: {e}")

    def _count_movies_by_year(self):
        """
                Count the number of movies released in a specified year.

                Returns:
                    num: The total number of movies released in the given year.
                """

        movies = self.storage.storage_get_movies()

        # prompt the user to enter the year of release
        year = input("Please enter the year of release: ")

        # create a dict of movies of the given year
        movies_year = {name: infos for name, infos in movies.items() if str(infos["Year of release"]) == year}

        # count the movies
        num = len(movies_year)

        return num

    def _add_movie_from_api(self):
        """
        Internal method to add a movie to the storage by fetching data from the OMDb API.
        """
        while True:
            try:
                # Get movie name from user input
                movie_name = get_valid_full_name()

                # Construct the API request URL using environment variables
                url = f"{self.base_url}?apikey={self.api_key}&t={movie_name}"
                response = requests.get(url, timeout=10)

                # Parse response
                if response.status_code == 200:
                    parsed = response.json()

                    if not parsed or parsed.get("Response") == "False":
                        answer = input("Movie not found. Press any key to try again, or 'q' to quit: ")
                        if answer.lower().strip() == "q":
                            break
                        continue

                    # Extract the relevant information from the API response
                    title = parsed.get("Title", "Unknown Title")
                    year = parsed.get("Year", "Unknown year")
                    rating = parsed.get("imdbRating", "Unknown rating")
                    poster = parsed.get("Poster", "Unknown poster")

                    # Call the storage method to add or update the movie
                    self.storage.storage_add_or_update_movie(title, year, rating, poster)
                    print(f"Movie '{movie_name}' added or updated successfully.")
                    answer = input("Press any key to add another movie, 'q' for quit: ").strip().lower()
                    if answer == "q":
                        break

                else:
                    print(f"Error fetching movie data: {response.status_code}. Please try again.")

            except requests.ConnectionError:
                print("Network error: Unable to reach the API. Please check your internet connection.")
                retry = input("Press any key to retry, or 'q' to quit: ").strip().lower()
                if retry == "q":
                    break

            except requests.Timeout:
                print("The request timed out. The server might be too slow or unresponsive.")
                retry = input("Press any key to retry, or 'q' to quit: ").strip().lower()
                if retry == "q":
                    break

            except Exception as e:
                print(f"An unexpected error occurred in add_movie_from_api: {e}")

    @staticmethod
    def _generate_website():
        """
                Generate a static website based on the stored movies.
                """
        print("Generating website...")
        generate_html()  # Call the function that generates the website

    def run(self):
        """
                Run the main program loop to interact with the user, display the menu, and perform actions.
                """
        menu = {
            '0': exit_panel,
            '1': self._display_list_movies,
            '2': self._add_movie_from_api,
            '3': self._delete_movie,
            '4': self._update_movie,
            '5': self._show_status,
            '6': self._get_random_movie,
            '7': self._search_movie,
            '8': self._sort_rating,
            '9': self._sort_year,
            '10': self._filter_movie,
            '11': self._generate_website
        }

        while True:
            display_menu()
            print()
            num_str = str(get_valid_int(menu, include_exit=True))

            if num_str == "0":
                menu[num_str]()
                break
            else:
                menu[num_str]()

