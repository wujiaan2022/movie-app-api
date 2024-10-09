from abc import ABC, abstractmethod


class InterfaceStorage(ABC):
    """
    An abstract base class that defines the interface for storage operations
    related to movie data. All methods must be implemented by any subclass
    that inherits from this class.

    Methods:
    --------
    storage_get_movies_dict():
        Retrieves the dictionary containing movie data.

    storage_add_movie():
        Adds a new movie to the storage.

    storage_delete_movie():
        Deletes a movie from the storage.

    storage_update_movie():
        Updates the information of an existing movie in the storage.
    """

    @abstractmethod
    def storage_get_movies(self):
        """
        Abstract method to retrieve a dictionary of movies from storage.

        Returns:
        --------
        dict
            A dictionary containing movie data.
        """
        pass

    @abstractmethod
    def storage_save_movies(self, movies):
        """
        Abstract method to save a dictionary of movies to storage.
        """
        pass

    @abstractmethod
    def storage_add_or_update_movie(self, title, year, rating, poster):
        """
        Abstract method to add a new movie to the storage.
        """
        pass

    @abstractmethod
    def storage_delete_movie(self, title):
        """
        Abstract method to delete a movie from the storage.

        Parameters:
        -----------
        None

        Returns:
        --------
        None
        """
        pass

