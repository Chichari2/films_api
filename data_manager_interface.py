from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    """Abstract class to define abstract methods which each
    DataManager (e.g. SQLite, JSON, CSV, etc.) should have.
    For this project, we're probably only going to implement...
    class SQLiteDataManager(DataManagerInterface)
    ...which has a few consequences.
    SQLite operations are fundamentally different from file I/O. They involve
    SQL queries and interactions with a database engine rather than reading
    from and writing to a file. Ergo, can hardly define any instance methods
    within this ABC definition. Meaning unlike mere JSON vs CSV, these all
    need to be abstract methods.
    """
    @abstractmethod
    def get_all_users(self):
        """Return users data as a list"""
        pass

    @abstractmethod
    def get_all_movies(self):
        """Return data for all movies"""
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        """Return a collection of movies for this user"""
        pass

    @abstractmethod
    def add_user(self, user):
        """Add 'user' to the users table"""
        pass

    @abstractmethod
    def add_movie(self, name, director, year, rating):
        """Add 'movie' to the movies table"""
        pass

    @abstractmethod
    def add_user_movie(self, user, movie):
        """Add relationship between user and movie to user_movies tb."""
        pass

    @abstractmethod
    def get_user_id(self, user_name_sought):
        """Retrieve the id of user_name_sought"""
        pass

    @abstractmethod
    def get_movie_id(self, movie_title_sought):
        """Retrieve the id of movie_title_sought"""
        pass

    @abstractmethod
    def update_movie(self, movie):
        """Update details of the <movie> in the movies table"""
        pass

    @abstractmethod
    def delete_movie(self, movie_id):
        """Delete the movie with <movie_id> in the movies table"""
        pass

    # @abstractmethod
    # def _read_data(self):
    #     """Read data from file."""
    #     pass
    #
    # @abstractmethod
    # def _write_data(self, movies: dict):
    #     """Write data to file."""
    #     pass


"""

chatGPT resolving of AnhTuan Vu's remarks:

"""


class IStorage(ABC):
    """Only two things remain abstract in the abstract class"""
    def __init__(self, file_path_arg):
        self._file_path = file_path_arg

    def delete_movie(self, title: str):
        """Deletes a movie from the movie database."""
        movies = self.list_movies()
        movies.pop(title, None)  # Using pop with a default to avoid KeyError
        self._write_data(movies)

    def add_movie(self, title, year, rating, poster):
        """Add a movie to the movie database."""
        movies = self.list_movies()
        movies[title] = {'year': year, 'rating': rating, 'poster': poster, 'notes': ''}
        self._write_data(movies)

    def list_movies(self):
        """Return all movies from the database."""
        return self._read_data()

    def update_movie(self, title, notes):
        """Update a movie's notes in the movie database."""
        movies = self.list_movies()
        if title in movies:
            movies[title]['notes'] = notes
            self._write_data(movies)
        else:
            raise ValueError(f"Movie '{title}' not found in the database.")

    @abstractmethod
    def _read_data(self):
        """Read data from file."""
        pass

    @abstractmethod
    def _write_data(self, movies: dict):
        """Write data to file."""
        pass

import csv
import json

class StorageCsv(IStorage):
    """Now the only thing needing specification are those 2 abstracts"""
    def _read_data(self):
        """Read data from a CSV file."""
        movies = {}
        with open(self._file_path, "r") as fd:
            reader = csv.DictReader(fd)
            for row in reader:
                title = row.pop('title')
                movies[title] = row
        return movies

    def _write_data(self, movies: dict):
        """Write data to a CSV file."""
        with open(self._file_path, "w", newline='') as fd:
            writer = csv.DictWriter(fd, fieldnames=['title', 'year', 'rating', 'poster', 'notes'])
            writer.writeheader()
            for title, data in movies.items():
                writer.writerow({'title': title, **data})

class StorageJson(IStorage):
    """Now the only thing needing specification are those 2 abstracts"""
    def _read_data(self):
        """Read data from a JSON file."""
        with open(self._file_path, "r") as fd:
            return json.load(fd)

    def _write_data(self, movies: dict):
        """Write data to a JSON file."""
        with open(self._file_path, "w") as fd:
            json.dump(movies, fd, indent=4)
