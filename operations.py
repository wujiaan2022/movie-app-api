import sys
import random
import difflib
from datetime import datetime
from user_input import get_valid_movie_name, choose_add_or_not, get_valid_movie_infos, get_valid_partial_name, get_valid_int
from utils import assign_sequence_to_movies, display_sequence_movies, average, median, best_worst


# display the main menu
def display_menu():
    print("\n" + "*" * 7 + " My Movies Database " + "*" * 7)
    menu = {
        '1': "Exit the movie panel",
        '2': "Show list of the movies",
        '3': "Add movies",
        '4': "Delete movies",
        '5': "Update movies",
        '6': "Show stats (average and median rating, best and worst rating)",
        '7': "Get a random movie",
        '8': "Search movies",
        '9': "Movies sorted by rating",
        '10': "Movies sorted by year",
        '11': "Filter movies"
    }
    for key, value in menu.items():
        print(f"{key}. {value}")


# function to exit the movie panel
def exit_panel():
    print("Bye!")
    sys.exit()


# function to display the movie list from database
def display_list_movie(movies):
    try:
        sequence_movies = assign_sequence_to_movies(movies)
        display_sequence_movies(sequence_movies)
    except Exception as e:
        print(f"An error occurred in display_list_movie: {e}")


# Function to add a movie
def add_movie(movies):
    while True:
        try:
            movie_name = get_valid_movie_name()

            # check name existence by checking close matches in the movie list
            close_matches = difflib.get_close_matches(movie_name, movies.keys(), n=len(movies), cutoff=0.8)

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
                    year, rating = get_valid_movie_infos()
                    movies[movie_name] = {"Year of release": year, "Rating": rating}
                    print(f"Movie {movie_name} with release of year {year} and rating {rating}\n"
                          f"has been added successfully.")
            else:
                year, rating = get_valid_movie_infos()
                movies[movie_name] = {"Year of release": year, "Rating": rating}
                print(f"Movie {movie_name} with release of year {year} and rating {rating}\n"
                      f"has been added successfully.")
        except KeyError as ke:
            print(f"Key error in add_movie: {ke}")
        except Exception as e:
            print(f"An error occurred in add_movie: {e}")


# Function to delete a movie
def delete_movie(movies):
    while True:
        try:
            partial_name = get_valid_partial_name()
            partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
            if partial_matches:
                sequence_movies = assign_sequence_to_movies(partial_matches)
                display_sequence_movies(sequence_movies)
                print("Enter the number of the movie to delete.")
                i = str(get_valid_int(sequence_movies))
                movie = sequence_movies[i]
                movie_name = list(movie.keys())[0]
                del movies[movie_name]
                print(f"Movie {movie_name} has been deleted successfully!")
            else:
                print("Cannot find any match movie. Please try again.")

            answer = input("Press any key to delete another movie, 'n' to exit: ").strip().lower()
            if answer == "n":
                break

        except Exception as e:
            print(f"An error occurred in delete_movie: {e}")


# Function to update a movie rating
def update_movie(movies):
    while True:
        try:
            partial_name = get_valid_partial_name()
            partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
            if partial_matches:
                sequence_movies = assign_sequence_to_movies(partial_matches)
                display_sequence_movies(sequence_movies)
                print("Enter the sequence number of the movie to update.")
                i = str(get_valid_int(sequence_movies))
                movie = sequence_movies[i]
                movie_name = list(movie.keys())[0]
                year, rating = get_valid_movie_infos()
                movies[movie_name] = {"Year of release": year, "Rating": rating}
                print(f"Movie {movie_name} with release of year {year} and rating {rating}\n"
                      f"has been updated successfully.")

            else:
                print("Cannot find any match movie. Please try again.")

            answer = input("Press any key to update another movie, 'n' to exit: " ).strip().lower()
            if answer == "n":
                break

        except Exception as e:
            print(f"An error occurred in update_movie_infos: {e}")


def show_status(movies):
    try:
        average(movies)
        median(movies)
        best_worst(movies)
    except Exception as e:
        print(f"An error occurred in show_status: {e}")


# Function to pick a random movie
def get_random_movie(movies):
    while True:
        try:
            random_movie = random.choice(list(movies.items()))
            print(f"The random movie is {random_movie[0]} with a rating of {random_movie[1]}")

            answer = input("Press any key to get another random movie, 'n' to exit: ").strip().lower()
            if answer == "n":
                break

        except Exception as e:
            print(f"An error occurred in get_random_movie: {e}")


# Function to search for movies by partial name
def search_movie(movies):
    while True:
        try:
            partial_name = get_valid_partial_name()
            partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
            if partial_matches:
                sequence_movies = assign_sequence_to_movies(partial_matches)
                display_sequence_movies(sequence_movies)

            else:
                print("No match found.")

            answer = input("Press any key to search another movie, 'n' to exit: ").strip().lower()
            if answer == "n":
                break

        except Exception as e:
            print(f"An error occurred in search_movie: {e}")


# Function to display movies sorted by rating
def sort_rating(movies):
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


def sort_year(movies):
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



