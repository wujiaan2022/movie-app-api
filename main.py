


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
