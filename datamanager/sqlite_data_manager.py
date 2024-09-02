"""
For better or for worse, I've come to the following conclusion:
I should define the models in the same file where I'm creating and binding
the engine. I'm sure some basic importing can make Base accessible elsewhere,
however I decided to keep things simple and focus on achieving better control
of sqlalchemy.orm rather than of the python importing game.

Furthermore, I'm choosing to work with strings as arguments of most methods,
in order to cut out the necessity for any additional layers of control.
"""

from typing import Type, List, Optional, cast
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, ForeignKey, literal
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm import relationship, backref
from datamanager.data_manager_interface import DataManagerInterface

SQL_FILEPATH = 'sqlite:///data/moviesdb.sqlite'

# Create the database engine/connection
engine = create_engine(SQL_FILEPATH)
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
    name = Column(String(80), unique=True, nullable=False)


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
    name = Column(String(120), nullable=False)
    director = Column(String(120), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    poster = Column(String(240), nullable=False)


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

    def get_all_users(self) -> List[Type[User]]:
        """Return a [] of User objects"""
        return self.db_session.query(User).all()

    def get_all_movies(self) -> List[Type[Movie]]:
        """Return a [] of Movie objects"""
        return self.db_session.query(Movie).all()

    def get_user_movies(self, user_id: int) -> List[Type[Movie]]:
        """
        We consult (!) UserMovie in order to fetch a [] of Movie (!) objects.
        Explanation:
        Join existing UserMovie and Movie at the movie_id match.
        Despite joining them, each table retains its respective identity.
        So we are able to address UserMovie within that join:
        filter(UserMovie.user_id == user_id)
        Return:
        a [] of Movie objects
        """
        movie_objects_list = self.db_session.query(Movie) \
            .join(UserMovie, Movie.id == UserMovie.movie_id) \
            .filter(UserMovie.user_id == literal(user_id)) \
            .all()
        # user_movies_list = [movie.to_dict() for movie in movie_objects_list]
        return movie_objects_list

    def add_user(self, user: str):
        new_user = User(name=user)
        self.db_session.add(new_user)
        # SQLAlchemy will now automatically generate a unique ID when commit()
        self.db_session.commit()
        print(f"User '{user}' added successfully!")

    def is_available_username(self, user: str) -> bool:
        """Return True if username (case-insensitive) not taken."""
        # .first() ensures that None is returned for no match, unlike .all()
        existing_user = self.db_session.query(User).filter_by(
            name=user).first()
        if existing_user:
            return False
        return True

    def user_id_exists(self, user_id: int) -> bool:
        """Return True if user_id present in 'users' table"""
        existing_user = self.db_session.query(User).filter_by(
            id=user_id).first()
        if existing_user:
            return True
        return False

    def add_movie(self, name: str, director: str, year: int,
                  rating: float, poster: str) -> int:
        # existing_movie = self.db_session.query(Movie).filter_by(
        #     name=name).first()
        # if existing_movie:
        #     print(f"Movie '{name}' already exists in the database!")
        #     return
        new_movie = Movie(name=name, director=director, year=year,
                          rating=rating, poster=poster)
        self.db_session.add(new_movie)
        self.db_session.commit()
        print(f"Movie '{name}' added successfully!")
        return cast(int, new_movie.id)  # redundant cast bc PyCharm typechecks

    def add_user_movie(self, user_id: int, movie_id: int):
        """Add a new relation of a usr to a mov. The ids are sure to exist"""

        # obtain 'movie' and 'user' names
        movie_object = self.db_session.query(Movie) \
            .filter(Movie.id == movie_id) \
            .one()
        movie = movie_object.name
        user_object = self.db_session.query(User) \
            .filter(User.id == user_id) \
            .one()
        user = user_object.name

        # Verify that the relationship doesn't already exist in 'user_movies'
        existing_relationship = self.db_session.query(UserMovie).filter_by(
            user_id=user_id, movie_id=movie_id).first()
        if existing_relationship:
            print(f"User {user} already has the movie {movie}!")
            return

        # Add a new relationship entry to 'user_movies'
        new_relationship = UserMovie(user_id=user_id, movie_id=movie_id)
        self.db_session.add(new_relationship)
        self.db_session.commit()
        print(f"Movie {movie} successfully added for {user}!")

    # def get_user_id(self, user_name_sought: str) -> Optional[int]:
    #     """Retrieve user id if user_name_sought present, else None"""
    #     list_of_users = self.get_all_users()
    #     for user in list_of_users:
    #         if user.name == user_name_sought:
    #             # cast necessary due to Pycharm typechecker vs. SQLAlchemy
    #             return cast(int, user.id)
    #     return None
    #
    # def get_movie_id(self, movie_title_sought: str) -> Optional[int]:
    #     """Retrieve movie id if movie_title_sought present, else None"""
    #     list_of_movies = self.get_all_movies()
    #     for movie in list_of_movies:
    #         if movie.name == movie_title_sought:
    #             # cast necessary due to Pycharm typechecker vs. SQLAlchemy
    #             return cast(int, movie.id)
    #     return None

    def get_movie_from_id(self, movie_id) -> Movie:
        """Query 'movies' table for movie_id match, return Movie object"""
        mov = self.db_session.query(Movie).filter(Movie.id == movie_id).one()
        # the redundant cast necessary to appease PyCharm's typechecker
        return cast(Movie, mov)

    @staticmethod
    def create_movie_object(movie_id: int, name: str, director: str, year: int,
                            rating: float, poster: str) -> Movie:
        """Bundle parameters into a Movie object"""
        movie = Movie(id=movie_id, name=name, director=director, year=year,
                      rating=rating, poster=poster)
        return movie

    def update_movie(self, movie: Movie):
        self.db_session.query(Movie).filter(Movie.id == movie.id).update(
            {'name': movie.name,
             'director': movie.director,
             'year': movie.year,
             'rating': movie.rating,
             'poster': movie.poster}
        )
        self.db_session.commit()

    def delete_movie(self, user_id: int, movie_id: int):
        """Remove the user-movie relationship entry, remove movie entry"""
        relationship_to_del = self.db_session.query(UserMovie). \
            filter(UserMovie.user_id == user_id,
            UserMovie.movie_id == movie_id).one()
        movie_to_del = self.db_session.query(Movie) \
            .filter(Movie.id == literal(movie_id)).one()
        # if not movie_to_delete:
        #     print(f"Error: Movie id <{movie_id}> not present in the db")
        #     return
        self.db_session.delete(relationship_to_del)
        self.db_session.delete(movie_to_del)
        self.db_session.commit()
        print(f"Movie with id <{movie_id}> successfully deleted.")
