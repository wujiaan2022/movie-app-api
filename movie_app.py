import random
import difflib
from datetime import datetime

from user_input import (get_valid_movie_name, choose_add_or_not, get_valid_movie_infos, get_valid_partial_name,
                        get_valid_int, get_valid_filter_rating, get_valid_filter_year)
from utils import display_sequence_movies, average, median, best_worst, close_matches_dict

from web_generate_from_api import generate_html


class MovieApp:
    def __init__(self, storage):
        """Initialize the instance variable storage which is an instance object of StorageJson class."""
        self.storage = storage

    def display_list_movies(self):
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

    def add_rest_infos(self, movie_name):
        """Helper method to add additional movie information (year, rating, poster)."""
        success = False  # Flag to track if the movie was added successfully

        while not success:
            try:
                year, rating = get_valid_movie_infos()
                if str(year).lower() == "q" or str(rating).lower() == "q":
                    break  # Exit if the user wants to quit
                else:
                    poster = input("Please enter the poster address (or press enter to skip): ").strip()
                    if not poster:
                        poster = "No poster available"
                    self.storage.storage_add_movie(movie_name, year, rating, poster)
                    print(f"Movie {movie_name} with year of release {year} and rating {rating}\n"
                          f"has been added successfully.")
                    success = True  # Set success to True after adding the movie

            except ValueError as ve:
                print(f"An error occurred while adding movie details: {ve}")
            except Exception as e:
                print(f"An unexpected error occurred while adding movie details: {e}")

        return success  # Return whether the movie was added successfully

    def add_movie(self):

        movies = self.storage.storage_get_movies()

        if not movies:
            print("No movies found")
            return

        while True:
            try:
                movie_name = get_valid_movie_name()
                if movie_name == "q":
                    break

                # check name existence by checking close matches in the movie list
                close_matches = difflib.get_close_matches(movie_name, movies.keys(), n=len(movies), cutoff=0.7)

                if close_matches:
                    print(f"There are {len(close_matches)} close matches to the move name you entered:")
                    for match in close_matches:
                        print(f"- {match}")

                    answer = choose_add_or_not()

                    if answer == "m":
                        break  # go back to memu
                    elif answer == "n":
                        continue  # add a new movie name

                # Call add_rest_infos and only continue if the movie was added successfully
                if self.add_rest_infos(movie_name):
                    # Ask the user if they want to add another movie
                    answer = input("Press any key to add another movie, 'q' for quit: ").strip().lower()
                    if answer == "q":
                        break

            except Exception as e:
                print(f"An error occurred in add_movie: {e}")

    def delete_movie(self):
        movies = self.storage.storage_get_movies()

        if not movies:
            print("No movies found")
            return

        while True:
            try:
                partial_name = get_valid_partial_name()

                if partial_name.lower() == "q":
                    break

                partial_matches = close_matches_dict(partial_name, movies)
                if not partial_matches:
                    print("The movie name does not exist. Please try again.")
                else:
                    print(f"There are {len(partial_matches)} close matches:")
                    display_sequence_movies(partial_matches)
                    print("Enter the number of the movie to delete.")
                    selected_index = int(get_valid_int(partial_matches))

                    if selected_index == 0:
                        break

                    movie_name = list(partial_matches.keys())[selected_index - 1]
                    confirmation = input(f"Are you sure you want to delete '{movie_name}'? (y/n): ").strip().lower()
                    if confirmation == 'y':
                        self.storage.storage_delete_movie(movie_name)
                        print(f"Movie '{movie_name}' has been deleted successfully!")

                continue_deleting  = input("Press any key to delete another movie, or 'q' for quit: ").strip().lower()
                if continue_deleting  == "q":
                    break

            except ValueError as ve:
                print(f"Value error occurred in delete_movie: {ve}")
            except Exception as e:
                print(f"An error occurred in delete_movie: {e}")