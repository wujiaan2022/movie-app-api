import sys
import random
import difflib
from datetime import datetime


def display_menu():
    print("\n" + "*" * 7 + " My Movies Database " + "*" * 7)
    menu = {
        '1': "Exit",
        '2': "List movies",
        '3': "Add movie",
        '4': "Delete movie",
        '5': "Update movie",
        '6': "Stats",
        '7': "Random movie",
        '8': "Search movie",
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


def index_movie(movies):
    try:
        index_movies = {}
        for i in range(1, len(movies)):
            for name, infos in movies.items():
                year = infos["Year of release"]
                rating = infos["Rating"]
                index_movies[str(i)] = {name: {"Year of release": year, "Rating": rating}}
        return index_movies
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


# Function to display a list of movies
def display_index_movies(index_movies):
    try:
        print(f"{len(index_movies)} movies in total")

        for i, movie in index_movies:
            name = movie.key
            year = movie[name]["Release of year"]
            rating = movie[name]["Rating"]
            print(f"{i}. {name} ({year}): {rating}")

    except Exception as e:
        print(f"Unexpected error occurred: {e}")


def display_list_movie(movies):
    try:
        index_movies = index_movie(movies)
        display_index_movies(index_movies)
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
            print(f"Unexpected error occurred: {e}")


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
        print(f"Error occurred. {e}")


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
            print(f"Unexpected error: {e}")


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
                    choose_from_menu()
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
            print(f"Key error: {ke}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")


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
            print(f"Unexpected error occurred: {e}")


def display_partial_matches(partial_name, movies):
    try:
        partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
        index_movies = index_movie(partial_matches)
        display_index_movies(index_movies)
    except KeyError as ve:
        print(f"Key error: {ve}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


# Function to delete a movie
def delete_movie(movies):
    while True:
        try:
            partial_name = get_valid_partial_name()
            partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
            if partial_matches:
                index_movies = index_movie(partial_matches)
                display_index_movies(index_movies)
                print("Enter the number of the movie to delete.")
                i = str(get_valid_int(index_movies))
                movie = index_movies[i]
                movie_name = list(movie.keys())[0]
                del movies[movie_name]
                print(f"Movie {movie_name} has been deleted successfully!")
            else:
                print("Cannot find any match movie. Please try again.")

            answer = input("Press any key to delete another movie, 'n' to exit: ").strip().lower()
            if answer == "n":
                break

        except Exception as e:
            print(f"Unexpected error occurred: {e}")


# Function to update a movie rating
def update_movie_infos(movies):
    while True:
        try:
            partial_name = get_valid_partial_name()
            partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
            if partial_matches:
                index_movies = index_movie(partial_matches)
                display_index_movies(index_movies)
                print("Enter the number of the movie to update.")
                i = str(get_valid_int(index_movies))
                movie = index_movies[i]
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
            print(f"Unexpected error occurred: {e}")


# Function to calculate average rating
def average(movies):
    try:
        total_sum = sum(movies.values())
        average_rating = total_sum / len(movies)
        print(f"Average rating: {average_rating:.2f}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


# Function to calculate median rating
def median(movies):
    try:
        ratings = sorted(movies.values())
        mid = len(ratings) // 2
        median_rating = (ratings[mid - 1] + ratings[mid]) / 2 if len(ratings) % 2 == 0 else ratings[mid]
        print(f"Median rating: {median_rating:.2f}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


# Function to find the best and worst rated movies
def best_worst(movies):
    try:
        sorted_movies = sorted(movies.items(), key=lambda item: item[1])
        print(f"The best movie is {sorted_movies[-1][0]} with a rating of {sorted_movies[-1][1]}")
        print(f"The worst movie is {sorted_movies[0][0]} with a rating of {sorted_movies[0][1]}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


def show_status(movies):
    try:
        average(movies)
        median(movies)
        best_worst(movies)
    except Exception as e:
        print(f"An error occurred in show_status: {e}")


# Function to pick a random movie
def random_choice(movies):
    try:
        random_movie = random.choice(list(movies.items()))
        print(f"The random movie is {random_movie[0]} with a rating of {random_movie[1]}")
    except Exception as e:
        print(f"An error occurred in random_choice: {e}")


# Function to search for movies by partial name
def search_movie(movies):
    while True:
        try:
            partial_name = get_valid_partial_name()
            partial_matches = {name: infos for name, infos in movies.item() if partial_name.lower() in name.lower()}
            if partial_matches:
                index_movies = index_movie(partial_matches)
                display_index_movies(index_movies)

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
        sorted_movies = sorted(movies.items(), key=lambda item: item[1], reverse=True)
        print("Movies sorted by rating (highest to lowest):")
        for name, rating in sorted_movies:
            print(f"{name}: {rating}")
    except Exception as e:
        print(f"An error occurred in sort_rating: {e}")


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
        '0': "exit_panel",
        '1': "list_movies",
        '2': "add_movie",
        '3': "delete_movie",
        '4': "update_movie",
        '5': "show_status",
        '6': "random_choice",
        '7': "search_movie",
        '8': "sort_rating",
        '9': "sort_year",
        '10': "filter_movies"
    }




if __name__ == "__main__":
    main()

