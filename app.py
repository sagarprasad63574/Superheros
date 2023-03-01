import os
import requests, json
from flask import Flask, redirect, render_template, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import db, connect_db, User, MySuperheros, Superheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections
from forms import SignUpForm, LoginForm, UserEditForm, SearchForm, SearchOrderForm, ImageForm, SuperheroForm, PowerstatsForm, BiographyForm, AppearanceForm, WorkForm, ConnectionsForm

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

@app.route("/")
def root():
    if g.user: 
        return redirect('/api/search')
    else: 
        return render_template("home.html")

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

@app.route('/user/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user=user)

@app.route('/user/edit/<int:user_id>', methods=["GET", "POST"])
def users_edit(user_id):
    """Edit user profile."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = UserEditForm()

    if form.validate_on_submit():

        user = User.authenticate(g.user.username, form.password.data)

        if not user: 
            flash("Invalid password.", 'danger')
            return redirect("/")

        g.user.username = form.username.data
        g.user.first_name = form.first_name.data
        g.user.last_name = form.last_name.data
        if form.image_url.data != "":
            g.user.image_url = form.image_url.data

        db.session.commit()
        return redirect(f"/user/{g.user.id}")
    
    return render_template('/users/edit.html', form=form)

@app.route("/search", methods=["GET", "POST"])
def search_superhero_from_otherUsers():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SearchForm()

    if form.validate_on_submit():
        try:
            name = form.name.data
            
            other_users_list = db.session.query(MySuperheros).filter(MySuperheros.user_id != g.user.id).all()

            results = []
            for superhero in other_users_list:
                hero = db.session.query(SuperheroInfo).filter_by(id=superhero.superheroinfo_id).filter(SuperheroInfo.name.like(f"%{name}%")).one_or_none()
                if hero:
                    results.append(hero)

            return render_template('/users/search.html', form=form, results=results)

        except IntegrityError:
            flash("No superhero found with that name", 'danger')
            return render_template('/users/search.html', form=form)

    return render_template('/users/search.html', form=form)

@app.route("/users/view/superhero/<int:superheroinfo_id>", methods=["GET"])
def view_other_users_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    superheroinfo = db.session.query(SuperheroInfo).filter_by(id=superheroinfo_id).one_or_none()
    powerstats = db.session.query(Powerstats).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    biography = db.session.query(Biography).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    appearance = db.session.query(Appearance).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    work = db.session.query(Work).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    connections = db.session.query(Connections).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()

    return render_template('/users/view_superhero.html', 
    superheroinfo=superheroinfo, 
    powerstats=powerstats, 
    biography=biography, 
    appearance=appearance, 
    work=work, 
    connections=connections)

@app.route("/users/add/superhero/<int:superheroinfo_id>", methods=["POST"])
def add_superhero_to_favorties(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    superheroinfo = db.session.query(SuperheroInfo).filter_by(id=superheroinfo_id).one_or_none()

    if superheroinfo:
        in_favorites = db.session.query(Superheros).filter_by(user_id=g.user.id).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()

        if in_favorites:
            flash("Superhero already in favorties", 'danger')
            return redirect('/search')
        else: 
            g.user.superheros.append(superheroinfo)
            db.session.commit()
                
            flash(f"Superhero ({superheroinfo.name}) added!", 'success')
            return redirect('/search')

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
            else: 
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

    except InvalidRequestError:
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

@app.route("/favorites/view", methods=["GET", "POST"])
def view_favorites_list_by_search():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SearchOrderForm()

    users_superheros_ids = db.session.query(Superheros).filter_by(user_id=g.user.id).all() 

    if form.validate_on_submit():

        name = form.name.data 
        order = form.order.data

        superhero_list = []
        for superhero in users_superheros_ids:

            superhero = db.session.query(SuperheroInfo).filter_by(id=superhero.superheroinfo_id).filter(SuperheroInfo.name.like(f"%{name}%")).one_or_none()
                
            if superhero:
                superhero_list.append(superhero)

        superhero_list.sort(key=lambda x: x.name, reverse=True) if order == "desc" else superhero_list.sort(key=lambda x: x.name)

        return render_template('/favorites/view_all.html', form=form, superhero_list=superhero_list)

    superhero_list = []
    for superhero in users_superheros_ids:
        superhero_list.append(db.session.query(SuperheroInfo).filter_by(id=superhero.superheroinfo_id).one())

    return render_template('/favorites/view_all.html', form=form, superhero_list=superhero_list)


@app.route("/favorites/view/<int:superheroinfo_id>", methods=["GET"])
def view_superheroinfo_by_id(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    superheroinfo = db.session.query(SuperheroInfo).filter_by(id=superheroinfo_id).one_or_none()
    powerstats = db.session.query(Powerstats).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    biography = db.session.query(Biography).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    appearance = db.session.query(Appearance).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    work = db.session.query(Work).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    connections = db.session.query(Connections).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()

    return render_template('/favorites/view_superhero.html', 
    superheroinfo=superheroinfo, 
    powerstats=powerstats, 
    biography=biography, 
    appearance=appearance, 
    work=work, 
    connections=connections)

@app.route("/favorites/delete/<int:superheroinfo_id>", methods=["POST"])
def delete_superhero_from_list(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    get_superhero = check_favorites_list(superheroinfo_id)
    db.session.delete(get_superhero)
    db.session.commit()

    flash("Deleted superhero from list", "success")
    return redirect('favorites/view')

@app.route("/mylist/create", methods=["GET", "POST"])
def create_new_superhero():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SuperheroForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo(name=form.name.data, image_url=form.image_url.data)

        g.user.mysuperheros.append(superheroinfo)
        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/create_superhero.html', form=form)

@app.route("/mylist/view", methods=["GET", "POST"])
def mylist_view_all():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = SearchOrderForm()
    users_mysuperheros_ids = db.session.query(MySuperheros).filter_by(user_id=g.user.id).all() 

    if form.validate_on_submit():

        name = form.name.data 
        order = form.order.data

        superhero_list = []
        for superhero in users_mysuperheros_ids:
            superhero = db.session.query(SuperheroInfo).filter_by(id=superhero.superheroinfo_id).filter(SuperheroInfo.name.like(f"%{name}%")).one_or_none()
            if superhero:
                superhero_list.append(superhero)


        superhero_list.sort(key=lambda x: x.name, reverse=True) if order == "desc" else superhero_list.sort(key=lambda x: x.name)

        return render_template('/mylist/view_all.html', form=form, superhero_list=superhero_list)

    superhero_list = []
    for superhero in users_mysuperheros_ids:
        superhero_list.append(db.session.query(SuperheroInfo).filter_by(id=superhero.superheroinfo_id).one())

    return render_template('/mylist/view_all.html', form=form, superhero_list=superhero_list)

@app.route("/mylist/view/<int:superheroinfo_id>", methods=["GET"])
def mylist_view_superheroinfo_by_id(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    superheroinfo = db.session.query(SuperheroInfo).filter_by(id=superheroinfo_id).one()
    powerstats = db.session.query(Powerstats).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    biography = db.session.query(Biography).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    appearance = db.session.query(Appearance).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    work = db.session.query(Work).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()
    connections = db.session.query(Connections).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()

    return render_template('mylist/view_superhero.html', 
    superheroinfo=superheroinfo, 
    powerstats=powerstats, 
    biography=biography, 
    appearance=appearance, 
    work=work, 
    connections=connections)

@app.route("/mylist/edit/image_url/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_image_of_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ImageForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        superheroinfo.image_url = form.image_url.data

        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_image.html', form=form)

@app.route("/mylist/add/powerstats/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_powerstats_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = PowerstatsForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        powerstat = Powerstats(
            intelligence=form.intelligence.data,
            strength=form.strength.data,
            speed=form.speed.data,
            durability=form.durability.data,
            power=form.power.data,
            combat=form.combat.data
        )

        superheroinfo.powerstats.append(powerstat)
        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_powerstats.html', form=form)

@app.route("/mylist/edit/powerstats/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_powerstats_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = PowerstatsForm()
    superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)
    powerstat = db.session.query(Powerstats).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        powerstat = db.session.query(Powerstats).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

        powerstat.intelligence = form.intelligence.data
        powerstat.strength = form.strength.data
        powerstat.speed = form.speed.data
        powerstat.durability = form.durability.data
        powerstat.power = form.power.data
        powerstat.combat = form.combat.data

        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_powerstats.html', form=form)


@app.route("/mylist/add/biography/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_biography_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = BiographyForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        biography = Biography(
            full_name=form.full_name.data,
            place_of_birth=form.place_of_birth.data,
            first_appearance=form.first_appearance.data,
            alter_egos=form.alter_egos.data,
            publisher=form.publisher.data
        )

        superheroinfo.biography.append(biography)
        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_biography.html', form=form)

@app.route("/mylist/edit/biography/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_biography_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = BiographyForm()
    superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)
    biography = db.session.query(Biography).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        biography = db.session.query(Biography).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

        biography.full_name = biography.full_name if form.full_name.data == "" else form.full_name.data
        biography.place_of_birth = biography.place_of_birth if form.place_of_birth.data == "" else form.place_of_birth.data
        biography.first_appearance = biography.first_appearance if form.first_appearance.data == "" else form.first_appearance.data
        biography.alter_egos = biography.alter_egos if form.alter_egos.data == "" else form.alter_egos.data
        biography.publisher = biography.publisher if form.publisher.data == "" else form.publisher.data
        
        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_biography.html', form=form)
    
@app.route("/mylist/add/appearance/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_appearance_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AppearanceForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        appearance = Appearance(
            gender=form.gender.data,
            race=form.race.data,
            height=form.height.data,
            weight=form.weight.data,
            eye_color=form.eye_color.data,
            hair_color=form.hair_color.data
        )

        superheroinfo.appearance.append(appearance)
        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_appearance.html', form=form)

@app.route("/mylist/edit/appearance/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_appearance_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AppearanceForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        appearance = db.session.query(Appearance).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

        appearance.gender = appearance.gender if form.gender.data == "" else form.gender.data
        appearance.race = appearance.race if form.race.data == "" else form.race.data
        appearance.height = appearance.height if form.height.data == "" else form.height.data
        appearance.weight = appearance.weight if form.weight.data == "" else form.weight.data
        appearance.eye_color = appearance.eye_color if form.eye_color.data == "" else form.eye_color.data
        appearance.hair_color = appearance.hair_color if form.hair_color.data == "" else form.hair_color.data

        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_appearance.html', form=form)

@app.route("/mylist/add/work/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_work_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = WorkForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        work = Work(
            occupation=form.occupation.data,
            base_of_operation=form.base_of_operation.data
        )

        superheroinfo.work.append(work)
        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_work.html', form=form)

@app.route("/mylist/edit/work/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_work_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = WorkForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        work = db.session.query(Work).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

        work.occupation = work.occupation if form.occupation.data == "" else form.occupation.data
        work.base_of_operation = work.base_of_operation if form.base_of_operation.data == "" else form.base_of_operation.data

        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_work.html', form=form)

@app.route("/mylist/add/connections/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_connections_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ConnectionsForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        connections = Connections(
            group_affiliation=form.group_affiliation.data,
            relatives=form.relatives.data
        )

        superheroinfo.connections.append(connections)
        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_connections.html', form=form)

@app.route("/mylist/edit/connections/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_connections_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ConnectionsForm()

    if form.validate_on_submit():

        superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

        connections = db.session.query(Connections).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

        connections.group_affiliation = connections.group_affiliation if form.group_affiliation.data == "" else form.group_affiliation.data
        connections.relatives = connections.relatives if form.relatives.data == "" else form.relatives.data

        db.session.commit()

        return redirect(f'/mylist/view/{superheroinfo.id}')

    return render_template('/mylist/add_connections.html', form=form)

@app.route("/mylist/delete/<int:superheroinfo_id>", methods=["POST"])
def mylist_delete_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    get_superhero = db.session.query(MySuperheros).filter_by(user_id=g.user.id).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()

    db.session.delete(get_superhero)
    db.session.commit()

    flash("Deleted superhero from list", "success")
    return redirect('mylist/view')