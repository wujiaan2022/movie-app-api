# from movie_app import MovieApp
# from storage_json import StorageJson
#
# storage = StorageJson('data.json')
# movie_app = MovieApp(storage)
# movie_app.run()

from movie_app import MovieApp
from storage_csv import StorageCsv

storage = StorageCsv('data.csv')
movie_app = MovieApp(storage)
movie_app.run()