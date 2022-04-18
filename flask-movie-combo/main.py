from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import InputRequired, NumberRange
import requests


db_path = "sqlite:///movie_db.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = db_path
Bootstrap(app)


db = SQLAlchemy(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    year = db.Column(db.Integer(), unique=False, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float(), unique=False, nullable=False)
    ranking = db.Column(db.Integer(), unique=True, nullable=False)
    review = db.Column(db.String(250), unique=False, nullable=False)
    img_url = db.Column(db.String(250), unique=False, nullable=False)

    def __repr__(self):
        return f"<Movie: {self.title} {self.description}>"


class RateMovieForm(FlaskForm):
    rating = FloatField('Your Rating Out of 10', validators=[InputRequired(), NumberRange(1.0, 10.0)])
    review = StringField('Your Review', validators=[InputRequired()])
    submit = SubmitField('Done')


class MovieTitleForm(FlaskForm):
    title = StringField('Movie Title', validators=[InputRequired()])
    submit = SubmitField('Add Movie')


@app.route("/", methods=["POST", "GET"])
def home():
    movies = Movie.query.all()
    if request.args:
        movie_id = request.args.get('id')
        movie = Movie.query.get(movie_id)
        db.session.delete(movie)
        db.session.commit()
        return redirect('/')
    return render_template("index.html", movies=movies)


@app.route("/edit", methods=["POST", "GET"])
def edit():
    movie_id = request.args.get('id')
    movie = Movie.query.get(movie_id)

    form = RateMovieForm()
    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect('/')
    return render_template("edit.html", form=form, movie=movie)


@app.route("/add", methods=["POST", "GET"])
def add():
    form = MovieTitleForm()
    if form.validate_on_submit():
        title = form.title.data
        # Movie List API
    return render_template("add.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
