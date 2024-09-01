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
    def is_available_username(self, user):
        """Check for username availability"""
        pass

    @abstractmethod
    def add_movie(self, name, director, year, rating, poster):
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
    def delete_movie(self, user_id, movie_id):
        """Delete the movie with <movie_id> in the movies table"""
        pass
