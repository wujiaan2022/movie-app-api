import sys


# display the main menu
def display_menu():
    print("\n" + "*" * 7 + " My Movies Database Panel" + "*" * 7 + "\n")
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