import sys
import random
import difflib
from datetime import datetime


# prompt and validate user input for the sequence number of a movie that user want to work on
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


# prompt and validate the user input for the movie name before adding
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


# prompt and validate user input for year and rating when add or update movie
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


# prompt and validate user input for partial name of movie before delete or update movie
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