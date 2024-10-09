import sys
import random
import difflib
from datetime import datetime
import user_input

from movie_storage import storage_get_movies, storage_add_movie, storage_delete_movie, storage_update_movie


# Function to display a list of movies with a sequence number for better readability and user experience
def display_sequence_movies(movies_dict):
    try:
        if movies_dict:
            # Enumerate through the movies and start counting from 1
            for i, (name, details) in enumerate(movies_dict.items(), start=1):
                year = details.get("Year of release", "Unknown year")
                rating = details.get("Rating", "Unknown rating")
                print(f"{i}. {name}, {year}, {rating}")

    except ValueError as ve:
        print(f"Value error occurred in display_sequence_movies: {ve}")
    except Exception as e:
        print(f"An error occurred in display_sequence_movies: {e}")


def display_close_matches_dict(partial, movies):

    try:

        # for key in movies: This loops through all the keys (movie titles) in the movies dictionary.
        movies_lower = {key.lower(): key for key in movies}

        close_matches = difflib.get_close_matches(partial.lower(), movies_lower, n=len(movies), cutoff=0.6)

        closed_dict = {movies_lower[match]: movies[movies_lower[match]] for match in close_matches}
        if not closed_dict:
            print("Cannot find any match movie.")
        else:
            print(f"There are {len(closed_dict)} close matches to the move name you entered:")
            display_sequence_movies(closed_dict)
            return closed_dict
    except KeyError as ve:
        print(f"Key error in display_partial_matches: {ve}")
    except Exception as e:
        print(f"An error occurred in display_partial_matches: {e}")


# display partial matches with sequence number after user enter part of movie name
def display_partial_matches(partial_name, movies):
    try:
        partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
        if not partial_matches:
            print("Cannot find any match movie. Please try again.")
        else:
            print(f"There are {len(partial_matches)} close matches to the move name you entered:")
            display_sequence_movies(partial_matches)
    except KeyError as ve:
        print(f"Key error in display_partial_matches: {ve}")
    except Exception as e:
        print(f"An error occurred in display_partial_matches: {e}")


# Function to calculate average rating
def average(movies):

    try:
        list_rating = []
        for infos in movies.values():
            rating = float(infos["Rating"])
            list_rating.append(rating)

        total_sum = sum(list_rating)
        average_rating = total_sum / len(movies)
        print(f"Average rating: {average_rating:.2f}")
    except Exception as e:
        print(f"An error occurred in average: {e}")


# Function to calculate median rating
def median(movies):

    try:
        list_ratings = []
        for infos in movies.values():
            rating = float(infos["Rating"])
            list_ratings.append(rating)

        sort_ratings = sorted(list_ratings)
        mid = len(sort_ratings) // 2

        if len(sort_ratings)%2 == 0:
            median_rating = (sort_ratings[mid - 1] + sort_ratings[mid]) / 2
        else:
            median_rating = sort_ratings[mid]
        print(f"Median rating: {median_rating:.2f}")
    except Exception as e:
        print(f"An error occurred in median: {e}")


# Function to find the best and worst rated movies
def best_worst(movies):

    try:
        sorted_movies = sorted(movies.items(), key=lambda item: float(item[1]["Rating"]))
        print(f"The best movie is {sorted_movies[-1][0]} with a rating of {sorted_movies[-1][1]["Rating"]}")
        print(f"The worst movie is {sorted_movies[0][0]} with a rating of {sorted_movies[0][1]["Rating"]}")
    except Exception as e:
        print(f"An error occurred in best_worst: {e}")




