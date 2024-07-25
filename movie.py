import sys
import random
import difflib
from datetime import datetime


def display_menu():
    print("\n" + "*" * 7 + " My Movies Database " + "*" * 7)
    menu = {
        '0': "Exit",
        '1': "List movies",
        '2': "Add movie",
        '3': "Delete movie",
        '4': "Update movie",
        '5': "Stats",
        '6': "Random movie",
        '7': "Search movie",
        '8': "Movies sorted by rating",
        '9': "Movies sorted by year",
        '10': "Filter movies"
    }
    for key, value in menu.items():
        print(f"{key}. {value}")


def choose_from_menu():
    while True:
        try:
            menu_choice = int(input("Enter choice (0-10): ").strip())
            if 0 <= menu_choice <= 10:
                return menu_choice
            else:
                print("Input error! Please enter a number between 0-10.")
        except ValueError:
            print("Input error! Please enter an integer.")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")


def exit_panel():
    print("Bye!")
    sys.exit()


# Function to list movies
def list_movies(movies):
    print(f"{len(movies)} movies in total")
    for name, infos in movies.items():
        print(f"{name} ({infos["Year of release"]}): {infos["Rating"]}")


def get_valid_movie_name():
    while True:
        try:
            movie_name = input("Please enter the movie name: ").strip().title()
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

        except KeyError as ke:
            print(f"Key error: {ke}")
        except Exception as e:
            print(f"Unexpected error occurred: {e}")


# Function to delete a movie
def delete_movie(movies):
    try:
        movie_name = get_valid_movie_name()
        if movie_name in movies:
            del movies[movie_name]
            print(f"Movie {movie_name} has been deleted successfully!")
        else:
            print("Sorry, the movie you entered does not exist.")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")


# Function to update a movie rating
def update_movie_infos(movies):
    movie_name = get_valid_movie_name()
    if movie_name in movies:
        year, rating = get_valid_movie_infos()
        movies[movie_name] = {"Year of release": year, "Rating": rating}
        print(f"Infos for movie {movie_name} has been updated successfully!")
    else:
        print("Sorry, the movie you entered does not exist.")

# Function to calculate average rating
def average(movies):
    total_sum = sum(movies.values())
    average_rating = total_sum / len(movies)
    print(f"Average rating: {average_rating:.2f}")


# Function to calculate median rating
def median(movies):
    ratings = sorted(movies.values())
    mid = len(ratings) // 2
    median_rating = (ratings[mid - 1] + ratings[mid]) / 2 if len(ratings) % 2 == 0 else ratings[mid]
    print(f"Median rating: {median_rating:.2f}")
# Function to find the best and worst rated movies


def best_worst(movies):
    sorted_movies = sorted(movies.items(), key=lambda item: item[1])
    print(f"The best movie is {sorted_movies[-1][0]} with a rating of {sorted_movies[-1][1]}")
    print(f"The worst movie is {sorted_movies[0][0]} with a rating of {sorted_movies[0][1]}")


def show_status(movies):
    average(movies)
    median(movies)
    best_worst(movies)


# Function to pick a random movie
def random_choice(movies):
    random_movie = random.choice(list(movies.items()))
    print(f"The random movie is {random_movie[0]} with a rating of {random_movie[1]}")
# Function to search for movies by partial name


def search_movie(movies):
    query = input("Please enter part of the movie name you are searching for: ")
    matches = {name: rating for name, rating in movies.items() if query.lower() in name.lower()}
    if matches:
        print("Found the following matches:")
        for name, rating in matches.items():
            print(f"{name}: {rating}")
    else:
        print("No match found.")


# Function to display movies sorted by rating
def sort_rating(movies):
    sorted_movies = sorted(movies.items(), key=lambda item: item[1], reverse=True)
    print("Movies sorted by rating (highest to lowest):")
    for name, rating in sorted_movies:
        print(f"{name}: {rating}")
# Function to display the menu and get user choice

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

