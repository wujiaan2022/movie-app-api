import sys


# display the main menu
def display_menu():
    print("\n" + "*" * 7 + " My Movies Database Panel" + "*" * 7 + "\n")
    menu = {
        '0': "Exit the movie panel",
        '1': "Show list of the movies",
        '2': "Add movies",
        '3': "Delete movies",
        '4': "Update movies",
        '5': "Show stats (average and median rating, best and worst rating)",
        '6': "Get a random movie",
        '7': "Search movies",
        '8': "Movies sorted by rating",
        '9': "Movies sorted by year",
        '10': "Filter movies",
        '11': "Generate Website"
    }
    for key, value in menu.items():
        print(f"{key}. {value}")


# function to exit the movie panel
def exit_panel():
    print("Bye!")
    sys.exit()