"""
For better or for worse, I've come to the following conclusion:
I should define the models in the same file where I'm creating and binding
the engine. I'm sure some basic importing can make Base accessible elsewhere,
however I decided to keep things simple and focus on achieving better control
of sqlalchemy.orm rather than of the python importing game.
"""

from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, backref
from data_manager_interface import DataManagerInterface

# Create the database engine/connection
engine = create_engine('sqlite:///data/moviesdb.sqlite')
# Create a session factory
Session = sessionmaker(bind=engine)
# Create a base class for declarative models, the parent for tables ("classes")
Base = declarative_base()


# Define the 'users' table model
class User(Base):
    """
    The "class" (ORM) corresponds with the 'users' table.
    """
    __tablename__ = 'users'
    # The id assignment will automatically be done by SQLAlchemy when commit()
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)

    def to_dict(self) -> Dict:
        """Convert the User object to a dictionary"""
        return {
            'id': self.id,
            'name': self.name
        }


# Define the 'movies' table model
class Movie(Base):
    """
    The "class" (ORM) corresponds with the 'movies' table basically.
    By convention, __tablename__ should be lower-cased, plural of class name.
    Class properties in a table class map to table columns.
    """
    __tablename__ = 'movies'
    # The id assignment will automatically be done by SQLAlchemy when commit()
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(120), unique=True, nullable=False)
    director = Column(String(120), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)

    def to_dict(self) -> Dict:
        """Convert the Movie object to a dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'director': self.director,
            'year': self.year,
            'rating': self.rating
        }


# Define the 'user_movies' junction table model
class UserMovie(Base):
    """
    This 'junction / association / cross-reference table' is needed since we
    want to relate many (movies) to many (users) meaning multiple occurrences
    of either. The attribute 'back_populates' sets up a bidirectional
    relationship between two classes.
    Note: The class attributes 'user' and 'movie' are not columns. Instead,
    what they achieve translates to the following in SQL:
    CREATE TABLE user_movies (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),      <--
        FOREIGN KEY(movie_id) REFERENCES movies(id)     <--
    );
    """
    __tablename__ = 'user_movies'
    # The id assignment will automatically be done by SQLAlchemy when commit()
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

    # Relationships to User and Movie tables
    user = relationship('User', backref=backref('movies'))
    movie = relationship('Movie', backref=backref('users'))


# Create the tables (if not yet created). Must be done below 'Base' usages
Base.metadata.create_all(engine)


class SQLiteDataManager(DataManagerInterface):
    def __init__(self):
        self.db_session = Session()  # Create a session instance

    def get_all_users(self):
        """
        Return a [] of dictionaries (User objects converted to dictionaries)
        """
        list_of_user_objects = self.db_session.query(User).all()
        users_list = [user.to_dict() for user in list_of_user_objects]
        return users_list

    def get_all_movies(self):
        """
        Return a [] of dictionaries (Movie objects converted to dictionaries)
        """
        list_of_movie_objects = self.db_session.query(Movie).all()
        movies_list = [movie.to_dict() for movie in list_of_movie_objects]
        return movies_list

    def get_user_movies(self, user_id):
        """
        We consult (!) UserMovie in order to fetch a [] of Movie (!) objects.
        Explanation:
        Join existing UserMovie and Movie at the movie_id match.
        Despite joining them, each table retains its respective identity.
        So we are able to address UserMovie within that join:
        filter(UserMovie.user_id == user_id)
        Return:
        a [] of dictionaries (Movie objects converted to dictionaries)
        """
        movie_objects_list = self.db_session.query(Movie) \
            .join(UserMovie, Movie.id == UserMovie.movie_id) \
            .filter(UserMovie.user_id == user_id) \
            .all()
        user_movies_list = [movie.to_dict() for movie in movie_objects_list]
        return user_movies_list

    def add_user(self, user):
        new_user = User(name=user)
        self.db_session.add(new_user)
        # SQLAlchemy will now automatically generate a unique ID when commit()
        self.db_session.commit()

    def add_movie(self, name, director, year, rating):
        new_movie = Movie(name="Titanic", director="James Cameron", year=1997,
                          rating=7.8)
        self.db_session.add(new_movie)
        self.db_session.commit()

    def add_user_movie(self, user_id, movie_id):
        new_relationship = UserMovie(user_id=user_id, movie_id=movie_id)
        self.db_session.add(new_relationship)
        self.db_session.commit()

    def get_user_id(self, user_name_sought):
        list_of_users = self.get_all_users()
        for user in list_of_users:
            if user.get("name") == user_name_sought:
                return int(user.get("id"))
        return None

    def get_movie_id(self, movie_title_sought):
        list_of_movies = self.get_all_movies()
        for movie in list_of_movies:
            if movie.get("name") == movie_title_sought:
                return int(movie.get("id"))
        return None

    def update_movie(self, movie_id):
        pass

    def delete_movie(self, movie_id):
        movie_to_delete = self.db_session.query(Movie) \
            .filter(Movie.id == movie_id)
        self.db_session.delete(movie_to_delete)
        self.db_session.commit()
