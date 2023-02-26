import os
import requests, json
from flask import Flask, redirect, render_template, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import db, connect_db, User, Superheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections
from forms import SignUpForm, LoginForm, SearchForm

CURR_USER_KEY = "curr_user"
API_KEY = "https://www.superheroapi.com/api.php/1406925980051610/"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///superhero-app'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.
    If form not valid, present form.
    If the there already is a user with that username: flash message
    and re-present form.
    """

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
    """Handle user login."""

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
    """Handle logout of user."""
    
    do_logout()
    flash("Logged out.", 'success')
    return redirect('/login')

@app.route("/api/search", methods=["GET", "POST"])
def search_superhero():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SearchForm()

    if form.validate_on_submit():
        try:
            name = form.name.data
            res = requests.get(f"{API_KEY}/search/{name}")
            data = res.json()
            
            if (data['response'] == 'error'):
                flash("No superhero found with that name", 'danger')
                return render_template('superhero/search.html', form=form)

            return render_template('superhero/search.html', form=form, data=data)

        except IntegrityError:
            flash("No superhero found with that name", 'danger')
            return render_template('superhero/search.html', form=form)

    return render_template('superhero/search.html', form=form)


@app.route("/api/superhero/<int:superhero_id>/view", methods=["GET"])
def search_superhero_by_id(superhero_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    try:
        res = requests.get(f"{API_KEY}/{superhero_id}")
        data = res.json()

        return render_template('superhero/view.html', data=data)

    except IntegrityError:
        flash("No superhero found with that name", 'danger')
        return redirect('/api/search')

@app.route("/api/superhero/<int:superhero_id>/add", methods=["POST"])
def add_superhero(superhero_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    try:
        res = requests.get(f"{API_KEY}/{superhero_id}")
        data = res.json()

        is_superhero_in_superheroinfo = find_superhero(data['id'])

        if is_superhero_in_superheroinfo:
            is_superhero_in_favorites = check_favorites_list(is_superhero_in_superheroinfo.id)

            if is_superhero_in_favorites:
                flash("Superhero already in the list", 'danger')
                return redirect('/api/search')
            
            g.user.superheros.append(is_superhero_in_superheroinfo)
            db.session.commit()

            flash(f"Superhero ({data['name']}) added!", 'success')
            return redirect('/api/search')

        superheroinfo = add_superheroinfo(data)

        powerstat = add_powerstats(data['powerstats'])
        biography = add_biography(data['biography'])
        appearance = add_appearance(data['appearance'])
        work = add_work(data['work'])
        connections = add_connections(data['connections'])

        superheroinfo.powerstats.append(powerstat)
        superheroinfo.biography.append(biography)
        superheroinfo.appearance.append(appearance)
        superheroinfo.work.append(work)
        superheroinfo.connections.append(connections)

        g.user.superheros.append(superheroinfo)

        superhero = [superheroinfo, powerstat, biography, appearance, work, connections]

        db.session.add_all(superhero)
        db.session.commit()

        flash(f"Superhero ({data['name']}) added!", 'success')
        return redirect('/api/search')

    except IntegrityError:
        flash("Superhero already in the list", 'danger')
        return redirect('/api/search')

def find_superhero(id):
    superhero = db.session.query(SuperheroInfo).filter_by(superhero_id=id).one_or_none()

    return superhero

def check_favorites_list(id):
    in_favorites = db.session.query(Superheros).filter_by(user_id=g.user.id).filter_by(superheroinfo_id=id).one_or_none()

    return in_favorites

def add_superheroinfo(data):
    superheroinfo = SuperheroInfo(
                    superhero_id=data['id'], 
                    name=data['name'], 
                    image_url=data['image']['url'])
    return superheroinfo
        
def add_powerstats(powerstats):
    powerstat = Powerstats(
                intelligence=powerstats['intelligence'], 
                strength=powerstats['strength'], 
                speed=powerstats['speed'], 
                durability=powerstats['durability'], 
                power=powerstats['power'], 
                combat=powerstats['combat'])
    return powerstat

def add_biography(biography):
    bio = Biography(
                full_name=biography['full-name'], 
                place_of_birth=biography['place-of-birth'], 
                first_appearance=biography['first-appearance'], 
                alter_egos=biography['alter-egos'], 
                publisher=biography['publisher'])
    return bio

def add_appearance(appearance):
    appear = Appearance(
                gender=appearance['gender'], 
                race=appearance['race'], 
                height=appearance['height'][0], 
                weight=appearance['weight'][0], 
                eye_color=appearance['eye-color'],
                hair_color=appearance['hair-color'])
    return appear

def add_work(work):
    w = Work(
                occupation=work['occupation'], 
                base_of_operation=work['base'])
    return w

def add_connections(connections):
    connection = Connections(
                group_affiliation=connections['group-affiliation'], 
                relatives=connections['relatives'])
    return connection


@app.route("/favorites/view", methods=["GET"])
def view_favorites_list():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    favorites = db.session.query(Superheros).filter_by(user_id=g.user.id).all()
 
    return render_template('favorites/view.html', favorites=favorites)

    

@app.route("/")
def root():
    # user = User(full_name="teemo", username="teemo", password="teemo")
    # superheroinfo = SuperheroInfo(superhero_id='70', full_name='batman')
    # powerstat = Powerstats(intelligence='90', strength='90', speed='90', durability='90', power='90', combat='90')
    # superheroinfo.powerstats.append(powerstat)
    # user.superheros.append(superheroinfo)
    # db.session.add(user)
    # db.session.add(superheroinfo)
    # db.session.add(powerstat)
    # db.session.commit()

    if g.user: 
        return redirect('/api/search')
    else: 
        return render_template("home.html")