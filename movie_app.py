import random
import difflib
from datetime import datetime

from user_input import (get_valid_partial_or_full_name, choose_add_or_not, get_valid_movie_infos,
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

    def get_rest_save_all(self, movie_name, key_word):
        """Helper method to add additional movie information (year, rating, poster)."""

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

    def add_movie(self):

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

                # any other key except for m and n meaning continue adding this movie
                self.get_rest_save_all(movie_name, "added")

                # Ask the user if they want to add another movie
                answer = input("Press any key to add another movie, 'q' for quit: ").strip().lower()
                if answer == "q":
                    break

            except Exception as e:
                print(f"An error occurred in add_movie: {e}")

    def update_movie(self):

        movies = self.storage.storage_get_movies()

        while True:
            try:
                movie_name = get_valid_partial_or_full_name()

                if movie_name.lower() == "q":
                    break

                close_matches = {name: infos for name, infos in movies.items() if movie_name.lower() in name.lower()}

                if not close_matches:
                    print("Cannot find any match movie. Please try again.")
                    continue

                display_sequence_movies(close_matches)
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

    def delete_movie(self):
        movies = self.storage.storage_get_movies()

        if not movies:
            print("No movies found")
            return

        while True:
            try:
                movie_name = get_valid_partial_or_full_name()

                if movie_name.lower() == "q":
                    break

                close_matches = close_matches_dict(movie_name, movies)
                if not close_matches:
                    print("The movie name does not exist. Please try again.")
                else:
                    print(f"There are {len(close_matches)} close matches:")
                    display_sequence_movies(close_matches)
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

