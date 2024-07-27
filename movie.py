import sys
import random
import difflib
from datetime import datetime


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


def get_valid_int(dic):
    while True:
        try:
            choice = int(input(f"Enter choice (1-{len(dic)}): ").strip())
            if 1 <= choice <= len(dic):
                return choice
            else:
                print(f"Input error! Please enter a number between 1-{len(dic)}.")
        except ValueError:
            print("Input error! Please enter an integer.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")


def exit_panel():
    print("Bye!")
    sys.exit()


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


# Function to display a list of movies
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


def display_list_movie(movies):
    try:
        sequence_movies = assign_sequence_to_movies(movies)
        display_sequence_movies(sequence_movies)
    except Exception as e:
        print(f"An error occurred in display_list_movie: {e}")


def get_valid_movie_name():
    while True:
        try:
            movie_name = input("Please enter the movie name you want to add: ").strip().title()
            if not movie_name:
                print("Movie name cannot be empty. Please try again.")
            elif not movie_name.replace(" ", "").isalnum():
                print("Movie name should only contain alphanumeric characters and spaces. Please try again.")
            else:
                return movie_name
        except Exception as e:
            print(f"An error occurred in get_valid_movie_name: {e}")


# after user entered the movie name,  display all the close matches,  prompt user to choose how to continue
def choose_add_or_not():
    try:
        while True:
            answer = input("Enter 'm' to go back to menu;\n"
                           "'n' to add a new movie name;\n"
                           "'a' to add this name anyway: ")
            if not answer:
                print("Your input can not be empty")
                continue
            elif answer not in ["m", "n", "a"]:
                print("Input error! Please enter m, n, or a")
                continue
            else:
                return answer
    except Exception as e:
        print(f"An error occurred in choose_add_or_not. {e}")


# prompt user for year and rating
def get_valid_movie_infos():
    while True:
        try:
            movie_year = int(input("Please enter the year of release:" ))

            if movie_year < 1888 or movie_year > datetime.now().year:
                print("Input error! Movie year cannot be earlier than 1888 or later than the current year.")
                continue

            while True:
                try:
                    movie_rating = float(input("Please enter the rating (0-10): "))

                    if movie_rating < 0 or movie_rating > 10:
                        print("Input error! you must enter a number between 0-10")
                        continue

                    break

                except ValueError:
                    print("Input error! Please enter a valid number for the rating.")

            converted_year = str(movie_year)
            rounded_rating = round(movie_rating, 1)
            return converted_year, rounded_rating

        except ValueError:
            print("Input error! Please enter a valid number for the year of release.")
        except Exception as e:
            print(f"An error occurred in get_valid_movie_infos: {e}")


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


def get_valid_partial_name():
    while True:
        try:
            partial_name = input("Please enter part of the movie name: ").strip()
            if not partial_name:
                print("Movie name cannot be empty. Please try again.")
            elif not partial_name.replace(" ", "").isalnum():
                print("Movie name should only contain alphanumeric characters and spaces. Please try again.")
            else:
                return partial_name
        except Exception as e:
            print(f"An error occurred in get_valid_partial_name: {e}")


def display_partial_matches(partial_name, movies):
    try:
        partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
        sequence_movies = assign_sequence_to_movies(partial_matches)
        display_sequence_movies(sequence_movies)
    except KeyError as ve:
        print(f"Key error in display_partial_matches: {ve}")
    except Exception as e:
        print(f"An error occurred in display_partial_matches: {e}")


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
def update_movie_infos(movies):
    while True:
        try:
            partial_name = get_valid_partial_name()
            partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
            if partial_matches:
                sequence_movies = assign_sequence_to_movies(partial_matches)
                display_sequence_movies(sequence_movies)
                print("Enter the number of the movie to update.")
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


# Main function to drive the program
def main():
    movies = {
        "In the Name of the Father": {"Year of release": "1993", "Rating": "8.1"},
        "Titanic": {"Year of release": "1993", "Rating": "8.1"},
        "The Shawshank Redemption": {"Year of release": "1994", "Rating": "9.3"},
        "The Godfather": {"Year of release": "1972", "Rating": "9.2"},
        "The Dark Knight": {"Year of release": "2008", "Rating": "9.0"},
        "Schindler's List": {"Year of release": "1993", "Rating": "8.1"},
        "Forrest Gump": {"Year of release": "1994", "Rating": "8.8"},
        "Pulp Fiction": {"Year of release": "1994", "Rating": "8.9"},
        "The Matrix": {"Year of release": "1999", "Rating": "1.0"},
        "Fight Club": {"Year of release": "1999", "Rating": "8.8"}
    }
    menu = {
        '1': "exit_panel",
        '2': "list_movies",
        '3': "add_movie",
        '4': "delete_movie",
        '5': "update_movie",
        '6': "show_status",
        '7': "random_choice",
        '8': "search_movie",
        '9': "sort_rating",
        '10': "sort_year",
        '11': "filter_movies"
    }




if __name__ == "__main__":
    main()

