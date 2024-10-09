import random
import difflib
from datetime import datetime

from user_input import (get_valid_partial_or_full_name, choose_add_or_not, get_valid_movie_infos,
                        get_valid_int, get_valid_filter_rating, get_valid_filter_year)
from utils import (display_sequence_movies, average, median, best_worst, display_close_matches_dict,
                   display_partial_matches)

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

    def update_movie(self):

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

    def show_status(self):
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

    def get_random_movie(self):
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

    def search_movie(self):
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

    def sort_rating(self):
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

    def sort_year(self):
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

    def filter_movie(self):
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

    def count_movies_by_year(self):

        movies = self.storage.storage_get_movies()

        # prompt the user to enter the year of release
        year = input("Please enter the year of release: ")

        # create a dict of movies of the given year
        movies_year = {name: infos for name, infos in movies.items() if str(infos["Year of release"]) == year}

        # count the movies
        num = len(movies_year)

        return num

    @staticmethod
    def generate_website():
        print("Generating website...")
        generate_html()  # Call the function that generates the website
