import sys
import random
import difflib
from datetime import datetime

from common import display_menu, exit_panel
from user_input import (get_valid_movie_name, choose_add_or_not, get_valid_movie_infos,
                        get_valid_partial_name, get_valid_int)
from utils import assign_sequence_to_movies, display_sequence_movies, average, median, best_worst
from operations import (display_list_movie, add_movie, delete_movie, update_movie, show_status, get_random_movie,
                        search_movie, sort_rating, sort_year, filter_movie, generate_website)


# Main function to drive the program
def main():

    menu = {
        '0': exit_panel,
        '1': display_list_movie,
        '2': add_movie,
        '3': delete_movie,
        '4': update_movie,
        '5': show_status,
        '6': get_random_movie,
        '7': search_movie,
        '8': sort_rating,
        '9': sort_year,
        '10': filter_movie,
        '11': generate_website
    }

    while True:
        display_menu()
        print()
        num_str = str(get_valid_int(menu, include_exit=True))

        if num_str == "0":
            menu[num_str]()
            break
        else:
            menu[num_str]()


if __name__ == "__main__":
    main()
