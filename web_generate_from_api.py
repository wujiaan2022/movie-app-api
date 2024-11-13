import requests
from dotenv import load_dotenv
import os
import json


# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")


def load_user_movies():
    try:
        with open("data.json", "r") as file:
            return json.load(file)  # Return the dictionary as-is
    except FileNotFoundError:
        print("User movies file not found.")
        return {}


def get_simple_infos_from_api(name):
    url = f"http://www.omdbapi.com/?apikey={api_key}&t={name}"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            parsed = response.json()

            if parsed:

                # print(parsed)
                # print(parsed.keys())

                simple_infos = {}

                title = parsed.get("Title", "Unknown Title")
                poster = parsed.get("Poster", "Unknown Poster")
                year = parsed.get("Year", "Unknown Year")
                ratings = parsed.get("Ratings", [])
                if ratings:
                    rating = ratings[0].get("Value", "Unknown Rating")
                else:
                    rating = "Unknown Rating"
                    print(f"Ratings for {name} is unavailable.")

                simple_infos[title] = {
                    "poster": poster,
                    "year": year,
                    "rating": rating,
                }

                return simple_infos

            else:
                print(f"The response for {name} is empty.")
                return None  # Ensure something is returned even if empty
        else:
            print(f"Failed to retrieve information for {name}. Status code: {response.status_code}")
            return None  # Ensure something is returned even if empty

    except Exception as e:
        print(f"An error occurred in get_simple_infos_from_api: {e}")


def generate_movie_grid(movies):
    movie_items = ""
    for title, details in movies.items():
        poster = details.get("Poster")

        # Only include movies that have a poster
        if poster and poster != "No poster available":
            year = details.get("Year of release", "Unknown Year")
            rating = details.get("Rating", "Unknown Rating")

            movie_items += f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{poster}"/>
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">Year: {year}</div>
                    <div class="movie-rating">Rating: {rating}</div>
                </div>
            </li>
            """
    return movie_items


def generate_html():
    # Get the absolute path to the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the path to the template file
    template_path = os.path.join(base_dir, "_static", "index_template.html")

    # Load the HTML template
    try:
        with open(template_path, "r") as template_file:
            template_html = template_file.read()
    except FileNotFoundError:
        print(f"Template file not found at: {template_path}")
        return

    # Load movie data from data.json
    movies = load_user_movies()

    # Generate movie grid HTML
    movie_grid_html = generate_movie_grid(movies)

    # Replace the placeholder with the movie grid
    final_html = template_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    # Write the generated HTML to a new file
    with open(os.path.join("_static", "index.html"), "w") as output_file:
        output_file.write(final_html)

    print("Website generated successfully!")

# print(get_simple_infos_from_api("The Dark Knight"))

# if __name__ == "__main__":
#     generate_html()
