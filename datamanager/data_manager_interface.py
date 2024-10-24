from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
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
    def get_movie_from_id(self, movie_id):
        """Fetch movie object for given movie_id"""
        pass

    @abstractmethod
    def update_movie(self, movie):
        """Update details of the <movie> in the movies table"""
        pass

    @abstractmethod
    def delete_movie(self, user_id, movie_id):
        """Delete the movie with <movie_id> in the movies table"""
        pass
