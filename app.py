"""
Routes for User. The user is able to create a new account or login in to an existing acccount.
Using sessions, the website is able to keep a user logged in and the user is able to logout.
"""
import os
from flask import Flask, redirect, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User
from forms import SignUpForm, LoginForm
from users import users
from api import api
from favorites import favorites
from mylist import mylist

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.register_blueprint(users, url_prefix="")
app.register_blueprint(api, url_prefix="")
app.register_blueprint(favorites, url_prefix="")
app.register_blueprint(mylist, url_prefix="")

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///superhero-app'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route("/")
def root():
    if g.user: 
        return redirect('/api/search')
    else: 
        return render_template("home.html")

@app.before_request
def add_user_to_g():
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    session[CURR_USER_KEY] = user.id

def do_logout():
    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                username=form.username.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():    
    do_logout()
    flash("Logged out.", 'success')
    return redirect('/login')