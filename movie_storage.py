import json


def storage_get_movies(filename="data.json"):
    try:
        with open(filename, "r") as file:
            movies = json.load(file)

    except FileNotFoundError:
        movies = {}
    except Exception as e:
        print(f"An error occurred in get_movies: {e}")
        movies = {}

    return movies


def storage_save_movies(movies, filename="data.json"):
    try:
        with open(filename, "w") as file:
            json.dump(movies, file, indent=4)
    except Exception as e:
        print(f"An error occurred in storage_save_movies: {e}")


def storage_add_movie(title, year_of_release, rating, filename="data.json"):
    try:
        movies = storage_get_movies(filename)
        if title in movies:
            print(f"The movie '{title}' already exists.")
            return False

        movies[title] = {"Year of release": year_of_release, "Rating": rating}
        storage_save_movies(movies, filename)
        return True

    except Exception as e:
        print(f"An error occurred in storage_add_movie: {e}")
        return False


def storage_delete_movie(title, filename="data.json"):
    try:
        movies = storage_get_movies(filename)
        if title in movies:
            del movies[title]
            storage_save_movies(movies, filename)
            return True
        else:
            print(f"Movie {title} not found.")
            return False
    except Exception as e:
        print(f"An error occurred in storage_delete_movie: {e}")
        return False


def storage_update_movie(title, year_of_release, rating, filename="data.json"):
    try:
        movies = storage_get_movies(filename)
        if title in movies:
            movies[title] = {"Year of release": year_of_release, "Rating": rating}
            storage_save_movies(movies,filename)
            return True
        else:
            print(f"Movie {title} not found.")
            return False

    except Exception as e:
        print(f"An error occurred in storage_update_movie: {e}")
        return False



