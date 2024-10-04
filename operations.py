import sys
import random
import difflib
from datetime import datetime

from user_input import (get_valid_movie_name, choose_add_or_not, get_valid_movie_infos, get_valid_partial_name,
                        get_valid_int, get_valid_filter_rating, get_valid_filter_year)
from utils import assign_sequence_to_movies, display_sequence_movies, average, median, best_worst, close_matches_dict

from movie_storage import storage_get_movies, storage_add_movie, storage_delete_movie, storage_update_movie

from web_generate_from_api import generate_html


# function to display the movie list from database
def display_list_movie():
    movies = storage_get_movies()
    try:
        sequence_movies = assign_sequence_to_movies(movies)
        display_sequence_movies(sequence_movies)
    except Exception as e:
        print(f"An error occurred in display_list_movie: {e}")


# Function to add a movie
def add_movie():

    movies = storage_get_movies()

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
                    break
                elif answer == "n":
                    continue

                elif answer == "a":

                    result = get_valid_movie_infos()

                    if result[0] == "q":
                        break

                    else:
                        year, rating = result
                        movies[movie_name] = {"Year of release": year, "Rating": rating}
                        storage_add_movie(movie_name, year, rating)
                        print(f"Movie {movie_name} with release of year {year} and rating {rating}\n"
                              f"has been added successfully.")

            else:
                year, rating = get_valid_movie_infos()
                if str(year).lower() == "q" or str(rating).lower() == "q":
                    break
                else:
                    storage_add_movie(movie_name, year, rating)
                    print(f"Movie {movie_name} with year of release {year} and rating {rating}\n"
                          f"has been added successfully.")

            answer = input("Press any key to add another movie, 'q' for quit: ").strip().lower()
            if answer == "q":
                break

        except KeyError as ke:
            print(f"Key error in add_movie: {ke}")
        except Exception as e:
            print(f"An error occurred in add_movie: {e}")


def delete_movie():
    movies = storage_get_movies()
    while True:
        try:
            partial_name = get_valid_partial_name()

            if partial_name.lower() == "q":
                break

            partial_matches = close_matches_dict(partial_name, movies)
            if partial_matches:

                sequence_movies = assign_sequence_to_movies(partial_matches)
                display_sequence_movies(sequence_movies)
                print("Enter the number of the movie to delete.")
                i = str(get_valid_int(sequence_movies))

                if i == "0":
                    break

                if i in sequence_movies:
                    movie = sequence_movies[i]
                    movie_name = list(movie.keys())[0]
                    answer = input("Press any key to confirm deleting, or 'q' for quit: ").strip().lower()
                    if answer == "q":
                        break
                    else:
                        storage_delete_movie(movie_name)
                        print(f"Movie {movie_name} has been deleted successfully!")

                    answer = input("Press any key to delete another movie, or 'q' for quit: ").strip().lower()
                    if answer == "q":
                        break

                else:
                    print("Invalid movie number. Please try again.")
            else:
                print("Cannot find any matching movie. Please try again.")

        except ValueError as ve:
            print(f"Value error occurred in delete_movie: {ve}")
        except IndexError as ie:
            print(f"Index error occurred in delete_movie: {ie}")
        except KeyError as ke:
            print(f"Key error occurred in delete_movie: {ke}")
        except Exception as e:
            print(f"An error occurred in delete_movie: {e}")


# Function to update a movie rating
def update_movie():
    movies = storage_get_movies()
    while True:
        try:
            partial_name = get_valid_partial_name()

            if partial_name.lower() == "q":
                break

            partial_matches = {name: infos for name, infos in movies.items() if partial_name.lower() in name.lower()}
            if partial_matches:
                sequence_movies = assign_sequence_to_movies(partial_matches)
                display_sequence_movies(sequence_movies)
                print("Enter the sequence number of the movie to update.")
                i = str(get_valid_int(sequence_movies))

                if i == "0":
                    break

                movie = sequence_movies[i]
                movie_name = list(movie.keys())[0]

                result = get_valid_movie_infos()
                if result[0] == "q":
                    break
                else:
                    year, rating = result

                    storage_update_movie(movie_name, year, rating)
                    print(f"Movie {movie_name} with release of year {year} and rating {rating}\n"
                          f"has been updated successfully.")

            else:
                print("Cannot find any match movie. Please try again.")

            answer = input("Press any key to update another movie, 'q' to quit: " ).strip().lower()
            if answer == "q":
                break

        except Exception as e:
            print(f"An error occurred in update_movie: {e}")


def show_status():

    try:
        average()
        median()
        best_worst()
    except Exception as e:
        print(f"An error occurred in show_status: {e}")


# Function to pick a random movie
def get_random_movie():
    movies = storage_get_movies()
    while True:
        try:
            random_movie = random.choice(list(movies.items()))
            print(f"The random movie is {random_movie[0]} with a rating of {random_movie[1]}")

            answer = input("Press any key to get another random movie, 'q' to quit: ").strip().lower()
            if answer == "q":
                break

        except Exception as e:
            print(f"An error occurred in get_random_movie: {e}")


# Function to search for movies by partial name
def search_movie():
    movies = storage_get_movies()
    while True:
        try:
            partial_name = get_valid_partial_name()

            if partial_name.lower() == "q":
                break

            partial_matches = {name: infos for name, infos in movies.items() if partial_name.lower() in name.lower()}
            if partial_matches:
                sequence_movies = assign_sequence_to_movies(partial_matches)
                display_sequence_movies(sequence_movies)

            else:
                print("No match found.")

            answer = input("Press any key to search another movie, 'q' to quit: ").strip().lower()
            if answer == "q":
                break

        except Exception as e:
            print(f"An error occurred in search_movie: {e}")


# Function to display movies sorted by rating
def sort_rating():
    movies = storage_get_movies()
    try:
        sorted_movies = sorted(movies.items(), key=lambda item: float(item[1]["Rating"]), reverse=True)
        print("Movies sorted by rating (highest to lowest):")
        sorted_dict = dict(sorted_movies)
        sequence_movies = assign_sequence_to_movies(sorted_dict)
        display_sequence_movies(sequence_movies)

    except ValueError as ve:
        print(f"Value error occurred in sort_ration: {ve}")
    except IndexError as ie:
        print(f"Index error occurred in sort_ration: {ie}")
    except KeyError as ke:
        print(f"Key error occurred in sort_ration: {ke}")
    except Exception as e:
        print(f"An error occurred in sort_rating: {e}")


def sort_year():
    movies = storage_get_movies()
    try:
        sorted_movies = sorted(movies.items(), key=lambda item: float(item[1]["Year of release"]), reverse=True)
        print("Movies sorted by year of release (highest to lowest):")
        sorted_dict = dict(sorted_movies)
        sequence_movies = assign_sequence_to_movies(sorted_dict)
        display_sequence_movies(sequence_movies)

    except ValueError as ve:
        print(f"Value error occurred in sort_year: {ve}")
    except IndexError as ie:
        print(f"Index error occurred in sort_year: {ie}")
    except KeyError as ke:
        print(f"Key error occurred in sort_year: {ke}")
    except Exception as e:
        print(f"An error occurred in sort_year: {e}")


def filter_movie():
    movies = storage_get_movies()
    while True:
        try:
            filter_rating = get_valid_filter_rating()

            if str(filter_rating).lower() == "q":
                break

            if filter_rating is None:
                rating_matches = movies

            else:
                rating_matches = {movie: infos for movie, infos in movies.items()
                                  if float(infos["Rating"]) >= float(filter_rating) }

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

            sequence_movies = assign_sequence_to_movies(end_year_matches)
            display_sequence_movies(sequence_movies)

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


# def count_movies_by_year():
#
#     movies = storage_get_movies()
#
#     # prompt the user to enter the year of release
#     year = input("Please enter the year of release: ")
#
#     # create a dict of movies of the given year
#     movies_year = {name: infos for name, infos in movies.items() if infos["Year of release"] == year}
#
#     # count the movies
#     num = len(movies_year)
#
#     return num
#
#
# print(count_movies_by_year())


def generate_website():
    print("Generating website...")
    generate_html()  # Call the function that generates the website
