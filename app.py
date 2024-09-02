"""
The assignment on one hand wants us to work with a junction db table in order
to relate many unique users to many unique movies, but at the same time it
wants the movie entries to be editable. Bob's edit of the Titanic should not
modify Alice's own Titanic entry. Meaning the movie entries can't be unique.
It's a paradox that has lead me to seek a balance of redundancy on one hand
and adjustment of the assignment's blueprints on the other hand.
"""

from flask import Flask, render_template, request, abort, redirect, url_for
from flask import flash, get_flashed_messages
from utils.omdb_api_data_fetcher import fetch_omdb_data
from datamanager.sqlite_data_manager import SQLiteDataManager

app = Flask(__name__)
# needed for flask.flash()
app.config['SECRET_KEY'] = 'super_secret_key'
# I'm choosing not to bloat my SQLiteDataManager's __init__ and instead prefer
# to externalize the db config. See SQL_FILEPATH in sql_data_manager
data_manager = SQLiteDataManager()


@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    """Present a list of all users registered in MovieWeb App"""
    popup = get_flashed_messages(with_categories=True)
    users = data_manager.get_all_users()
    return render_template('users.html', popup=popup, users=users), 200


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    """Render any movies that user with <user_id> has added to their app"""
    popup = get_flashed_messages(with_categories=True)
    # for when someone manually enters users/<gibberish id>
    if not data_manager.user_id_exists(user_id):
        flash(f"Bad user id: {user_id}", "info")
        return redirect(url_for('list_users')), 302
    movies = data_manager.get_user_movies(user_id)
    return render_template('user_page.html',
                           popup=popup, movies=movies, user_id=user_id), 200


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Add new user to users table if not already in the db."""
    if request.method == 'GET':
        popup = get_flashed_messages(with_categories=True)
        return render_template('add_user.html',
                               popup=popup), 200
    elif request.method == 'POST':
        name = request.form.get('name', "").strip()
        if not name:
            abort(400)
        if not data_manager.is_available_username(name):
            flash(f"User '{name}' already exists in the database!")
            return redirect(url_for('add_user')), 302
        data_manager.add_user(name)
        flash(f"'{name}' added to database.", "info")
        return redirect(url_for('add_user')), 302


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_user_movie(user_id):
    """Add new movie to movies table, even if it's a duplicate title entry due
    to what the assignment is asking, and then also add a new UserMovie
    relationship to 'user_movies' database table."""
    if request.method == 'GET':
        popup = get_flashed_messages(with_categories=True)
        # for when someone manually enters /<gibberish id>/add_movie
        if not data_manager.user_id_exists(user_id):
            flash(f"Unassigned user id: {user_id}.", "info")
            return redirect(url_for('list_users')), 302
        return render_template('add_movie.html',
                               popup=popup, user_id=user_id), 200
    elif request.method == 'POST':
        # name = request.form.get('name', "").strip()
        # if not name:
        #     abort(400)
        #
        # # repurposing 'name' variable currently
        # fetched_data = fetch_omdb_data(name)
        # if not fetched_data:
        #     flash(f"oMDB API found nothing, try another query", "info")
        #     return redirect(url_for(f'add_user_movie', user_id=user_id)), 302
        # name, director, year, rating, poster = fetched_data
        # if not (name and director and year and rating and poster):
        #     flash(f"Incomplete oMDB API entry, try another query", "info")
        #     return redirect(url_for(f'add_user_movie', user_id=user_id)), 302
        # else:

        # reacquire the data that was passed through the html
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')
        poster = request.form.get('poster')
        movie_id = data_manager.add_movie(name, director, int(year),
                                          float(rating), poster)
        print(f"movie id: {movie_id}. user id: {user_id}")
        data_manager.add_user_movie(user_id, movie_id)
        flash(f"'{name}' added to database.", "info")
        # movies = data_manager.get_user_movies(user_id)
        return redirect(url_for('list_user_movies', user_id=user_id)), 302


@app.route('/users/<user_id>/add_movie/confirm', methods=['POST'])
def confirm_adding(user_id):
    """Render a page to have user confirm the inclusion of what OMDB has
    fetched. Exclusively handles POST method."""
    name = request.form.get('name', "").strip()
    if not name:
        abort(400)

    fetched_data = fetch_omdb_data(name)
    if not fetched_data:
        flash(f"oMDB API found nothing, try another query", "info")
        return redirect(url_for(f'add_user_movie', user_id=user_id)), 302
    # repurposing 'name' variable currently
    name, director, year, rating, poster = fetched_data
    if not (name and director and year and rating and poster):
        flash(f"Incomplete oMDB API entry, try another query", "info")
        return redirect(url_for(f'add_user_movie', user_id=user_id)), 302
    else:
        return render_template(
            'confirm_adding.html', name=name,
            director=director, year=year, rating=rating,
            poster=poster, user_id=user_id), 200


@app.route('/users/<user_id>/update_movie/<movie_id>',
           methods=['GET', 'POST'])
def update_user_movie(user_id, movie_id):
    """Render editing interface for GET, delegate updating for POST"""
    if request.method == 'GET':
        movie = data_manager.get_movie_from_id(movie_id)
        return render_template('update_movie.html',
                               movie=movie, user_id=user_id)
    elif request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')
        poster = request.form.get('poster')
        movie = data_manager.create_movie_object(
            int(movie_id), name, director, int(year), float(rating), poster)
        data_manager.update_movie(movie)
        flash(f"Update success", "info")
        return redirect(url_for('list_user_movies', user_id=user_id)), 302


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_user_movie(user_id, movie_id):
    """Delegate deletion protocol. Render nothing. Flash confirmation."""
    movie = data_manager.get_movie_from_id(movie_id)
    mov_title = movie.name
    data_manager.delete_movie(user_id, movie_id)
    flash(f"'{mov_title}' successfully removed from database.", "info")
    return redirect(url_for('list_user_movies', user_id=user_id)), 302


@app.route('/users/<user_id>/delete_movie/<movie_id>/confirm')
def confirm_deletion(user_id, movie_id):
    """Render a page to ask user's confirmation."""
    movie = data_manager.get_movie_from_id(movie_id)
    return render_template('confirm_deletion.html',
                           movie=movie, user_id=user_id), 200


if __name__ == "__main__":
    app.run(debug=True, port=5000)
