from sqlite_setup import SQLiteDataManager


def main():
    db = SQLiteDataManager()
    db.add_user("Mile")
    db.add_movie("Titanic", "James Cameroon", 1997, 8.7)
    this_user = db.get_user_id("Mile")
    this_movie = db.get_movie_id("Titanic")
    db.add_user_movie(this_user, this_movie)
    movies = db.get_user_movies(this_user)
    for movie in movies:
        print(f"User has movie titled: {movie.get("name")}")


if __name__ == "__main__":
    main()
