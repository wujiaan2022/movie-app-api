import requests
from dotenv import load_dotenv
import os


# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("API_KEY")


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
    for movie in movies:

        for title, details in movie.items():
            poster = details.get("poster", "https://via.placeholder.com/300x450?text=No+Poster+Available")
            year = details.get("year", "Unknown Year")

            movie_items += f"""
            <li>
                <div class="movie">
                    <img class="movie-poster" src="{poster}"/>
                    <div class="movie-title">{title}</div>
                    <div class="movie-year">{year}</div>
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

    # Get movie data for two movies
    movies = []
    movie_titles = ["The Dark Knight", "Pulp Fiction"]
    for title in movie_titles:
        movie_info = get_simple_infos_from_api(title)
        if movie_info:
            movies.append(movie_info)

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
