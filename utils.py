import sys
import random
import difflib
from datetime import datetime
import user_input


# assign each movie to a sequence number for better readability and user experience
def assign_sequence_to_movies(movies):
    try:
        sequence_movies = {}
        i = 1
        for name, infos in movies.items():
            year = infos["Year of release"]
            rating = infos["Rating"]
            sequence_movies[str(i)] = {name: {"Year of release": year, "Rating": rating}}
            i += 1
        return sequence_movies
    except Exception as e:
        print(f"An error occurred in assign_sequence_to_movies: {e}")


# Function to display a list of movies with a sequence number for better readability and user experience
def display_sequence_movies(sequence_movies):
    try:
        print(f"{len(sequence_movies)} movies in total\n")

        for i, movie in sequence_movies.items():
            name = list(movie.keys())[0]
            year = movie[name]["Year of release"]
            rating = movie[name]["Rating"]
            print(f"{i}. {name} ({year}): {rating}")

    except ValueError as ve:
        print(f"Value error occurred in display_sequence_movies: {ve}")
    except IndexError as ie:
        print(f"Index error occurred in display_sequence_movies: {ie}")
    except KeyError as ke:
        print(f"Key error occurred in display_sequence_movies: {ke}")
    except Exception as e:
        print(f"An error occurred in display_sequence_movies: {e}")


# display partial matches with sequence number after user enter part of movie name
def display_partial_matches(partial_name, movies):
    try:
        partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
        sequence_movies = assign_sequence_to_movies(partial_matches)
        display_sequence_movies(sequence_movies)
    except KeyError as ve:
        print(f"Key error in display_partial_matches: {ve}")
    except Exception as e:
        print(f"An error occurred in display_partial_matches: {e}")


# Function to calculate average rating
def average(movies):
    try:
        total_sum = sum(movies.values())
        average_rating = total_sum / len(movies)
        print(f"Average rating: {average_rating:.2f}")
    except Exception as e:
        print(f"An error occurred in average: {e}")


# Function to calculate median rating
def median(movies):
    try:
        ratings = sorted(movies.values())
        mid = len(ratings) // 2
        median_rating = (ratings[mid - 1] + ratings[mid]) / 2 if len(ratings) % 2 == 0 else ratings[mid]
        print(f"Median rating: {median_rating:.2f}")
    except Exception as e:
        print(f"An error occurred in median: {e}")


# Function to find the best and worst rated movies
def best_worst(movies):
    try:
        sorted_movies = sorted(movies.items(), key=lambda item: item[1])
        print(f"The best movie is {sorted_movies[-1][0]} with a rating of {sorted_movies[-1][1]}")
        print(f"The worst movie is {sorted_movies[0][0]} with a rating of {sorted_movies[0][1]}")
    except Exception as e:
        print(f"An error occurred in best_worst: {e}")