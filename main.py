import sys
import random
import difflib
from datetime import datetime

import storage_json
import movie_app

from common import display_menu, exit_panel
from user_input import (choose_add_or_not, get_valid_movie_infos, get_valid_int)
from utils import display_sequence_movies, average, median, best_worst


# Main function to drive the program
def main():
    storage_json_1 = storage_json.StorageJson("data.json")
    movie_app_1 = movie_app.MovieApp(storage_json_1)
    movie_app_1.run()


if __name__ == "__main__":
    main()
