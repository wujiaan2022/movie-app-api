from storage import storage_json
import movie_app


# Main function to drive the program
def main():
    storage_json_1 = storage_json.StorageJson("data.json")
    movie_app_1 = movie_app.MovieApp(storage_json_1)
    movie_app_1.run()


if __name__ == "__main__":
    main()
