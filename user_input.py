import sys
import random
import difflib
from datetime import datetime

from common import display_menu, exit_panel


# prompt and validate user input for the sequence number of a movie that user want to work on
# def get_valid_int(dic, include_exit=False):
#     while True:
#         try:
#             if include_exit:
#                 choice = int(input(f"Enter choice (1-{len(dic)-1}), or '0' to exit: ").strip())
#             else:
#                 choice = int(input(f"Enter choice (1-{len(dic)}): ").strip())
#
#             if include_exit and choice == 0:
#                 return 0
#
#             elif 1 <= choice <= len(dic):
#                 return choice
#             else:
#                 print(f"Input error! Please enter a number between 1-{len(dic)}.")
#         except ValueError:
#             print("Input error! Please enter an integer.")
#         except Exception as e:
#             print(f"An error occurred in get_valid_int: {e}")


# def get_valid_int(dic, include_exit=False):
#     while True:
#         try:
#             if include_exit:
#                 choice = int(input(f"Enter choice (1-{len(dic)-1}), or '0' to exit: ").strip())
#             else:
#                 choice = int(input(f"Enter choice (1-{len(dic)}, or '0' to exit): ").strip())
#
#             if 0 <= choice <= len(dic):
#                 return choice
#             else:
#                 print(f"Input error! Please enter a number between 1-{len(dic)}, or '0' to exit.")
#         except ValueError:
#             print("Input error! Please enter an integer.")
#         except Exception as e:
#             print(f"An error occurred in get_valid_int: {e}")


def get_valid_int(dic, include_exit=False):
    while True:
        try:
            upper_limit = len(dic)-1 if include_exit else len(dic)

            choice = int(input(f"Enter choice (1-{upper_limit}), or '0' to exit: ").strip())

            if 0 <= choice <= upper_limit:
                return choice
            else:
                print(f"Input error! Please enter a number between 1-{upper_limit}, or '0' to exit.")
        except ValueError:
            print("Input error! Please enter an integer.")
        except Exception as e:
            print(f"An error occurred in get_valid_int: {e}")


# prompt and validate the user input for the movie name before adding
def get_valid_partial_or_full_name():
    while True:
        try:
            movie_name = input("Please enter partial or full name of the movie (or 'q' for quit): ").strip().title()
            if movie_name.lower() == "q":
                return "q"
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
            answer = input("Enter any key to add this name anyway,\n"
                           "or 'm' to go back to menu;\n"
                           "'n' to add a new movie name: ").strip().lower()  # Stripping whitespaces and lowercasing
            return answer
    except Exception as e:
        print(f"An error occurred in choose_add_or_not. {e}")


# prompt and validate user input for year and rating when add or update movie
def get_valid_movie_infos():
    while True:
        try:
            movie_year = input("Please enter the year of release(or 'q' for quit): ")

            if movie_year.lower() == "q":
                return "q", None, None

            movie_year = int(movie_year)
            if movie_year < 1888 or movie_year > datetime.now().year:
                print("Input error! Movie year cannot be earlier than 1888 or later than the current year.")
                continue

            poster = (input("Please enter the poster address (or press enter to skip): ").strip()
                      or "No poster available")

            while True:
                try:
                    movie_rating = input("Please enter the rating (0-10), or 'q' for quit: ")

                    if movie_rating.lower() == "q":
                        return "q", None, None

                    movie_rating = float(movie_rating)
                    if movie_rating < 0 or movie_rating > 10:
                        print("Input error! You must enter a number between 0-10.")
                        continue

                    break

                except ValueError:
                    print("Input error! Please enter a valid number for the rating.")

            converted_year = str(movie_year)
            rounded_rating = round(movie_rating, 1)

            return converted_year, rounded_rating, poster

        except ValueError:
            print("Input error! Please enter a valid number for the year of release.")
        except Exception as e:
            print(f"An error occurred in get_valid_movie_infos: {e}")


def get_valid_filter_rating():
    while True:
        try:
            filter_rating = input("\nEnter minimum rating (leave blank for no minimum rating) or 'q' for quit: ")

            if filter_rating.lower() == "q":
                return filter_rating

            if filter_rating == "":
                return None

            else:
                filter_rating = float(filter_rating)
                if 0 <= filter_rating <= 10:
                    rounded_rating = round(filter_rating, 1)
                    return rounded_rating

                else:
                    print("Input error! You must enter a number between 0-10.")

        except ValueError:
            print("Input error! Please enter a valid number for minimus rating.")
        except Exception as e:
            print(f"An error occurred in get_valid_filter_rating: {e}")


def get_valid_filter_year():
    while True:
        try:
            filter_year = input("Enter a year number or leave it empty, or 'q' for quit: ")

            if filter_year.lower() == "q":
                return filter_year

            if filter_year == "":
                return None

            filter_year = int(filter_year)
            if 1888 <= filter_year <= datetime.now().year:
                return filter_year

            else:
                print("Input error! Movie year cannot be earlier than 1888 or later than the current year.")

        except ValueError:
            print("Input error! Please enter a valid number for minimus rating.")
        except Exception as e:
            print(f"An error occurred in get_valid_filter_rating: {e}")

