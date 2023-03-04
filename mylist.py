import os
import requests, json
from flask import Flask, redirect, render_template, Blueprint, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import db, connect_db, User, MySuperheros, Superheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections
from forms import SignUpForm, LoginForm, UserEditForm, SearchForm, SearchOrderForm, ImageForm, SuperheroForm, PowerstatsForm, BiographyForm, AppearanceForm, WorkForm, ConnectionsForm

mylist = Blueprint("mylist", __name__, static_folder="static", template_folder="templates")

def check_mylist(id):
    in_list = db.session.query(MySuperheros).filter_by(user_id=g.user.id).filter_by(superheroinfo_id=id).one_or_none()

    return in_list

@mylist.route("/mylist/create", methods=["GET", "POST"])
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

@mylist.route("/mylist/view", methods=["GET", "POST"])
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

@mylist.route("/mylist/view/<int:superheroinfo_id>", methods=["GET"])
def mylist_view_superheroinfo_by_id(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero: 
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

    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

@mylist.route("/mylist/edit/image_url/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_image_of_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ImageForm()
    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

        if form.validate_on_submit():

            superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)
            superheroinfo.image_url = form.image_url.data

            db.session.commit()
            
            return redirect(f'/mylist/view/{superheroinfo.id}')
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_image.html', form=form)

@mylist.route("/mylist/add/powerstats/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_powerstats_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = PowerstatsForm()
    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

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
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_powerstats.html', form=form)

@mylist.route("/mylist/edit/powerstats/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_powerstats_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = PowerstatsForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

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
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_powerstats.html', form=form)


@mylist.route("/mylist/add/biography/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_biography_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = BiographyForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

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
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_biography.html', form=form)

@mylist.route("/mylist/edit/biography/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_biography_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = BiographyForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

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
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_biography.html', form=form)
    
@mylist.route("/mylist/add/appearance/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_appearance_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AppearanceForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

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
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_appearance.html', form=form)

@mylist.route("/mylist/edit/appearance/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_appearance_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = AppearanceForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

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
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_appearance.html', form=form)

@mylist.route("/mylist/add/work/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_work_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = WorkForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

        if form.validate_on_submit():

            superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

            work = Work(
                occupation=form.occupation.data,
                base_of_operation=form.base_of_operation.data
            )

            superheroinfo.work.append(work)
            db.session.commit()

            return redirect(f'/mylist/view/{superheroinfo.id}')
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_work.html', form=form)

@mylist.route("/mylist/edit/work/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_work_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = WorkForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

        if form.validate_on_submit():

            superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)
            work = db.session.query(Work).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

            work.occupation = work.occupation if form.occupation.data == "" else form.occupation.data
            work.base_of_operation = work.base_of_operation if form.base_of_operation.data == "" else form.base_of_operation.data

            db.session.commit()

            return redirect(f'/mylist/view/{superheroinfo.id}')
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_work.html', form=form)

@mylist.route("/mylist/add/connections/<int:superheroinfo_id>", methods=["GET", "POST"])
def add_connections_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ConnectionsForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:

        if form.validate_on_submit():

            superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)

            connections = Connections(
                group_affiliation=form.group_affiliation.data,
                relatives=form.relatives.data
            )

            superheroinfo.connections.append(connections)
            db.session.commit()

            return redirect(f'/mylist/view/{superheroinfo.id}')
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')

    return render_template('/mylist/add_connections.html', form=form)

@mylist.route("/mylist/edit/connections/<int:superheroinfo_id>", methods=["GET", "POST"])
def edit_connections_to_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    form = ConnectionsForm()

    get_superhero = check_mylist(superheroinfo_id)

    if get_superhero:
        
        if form.validate_on_submit():

            superheroinfo = SuperheroInfo.query.get_or_404(superheroinfo_id)
            connections = db.session.query(Connections).filter_by(superheroinfo_id=superheroinfo.id).one_or_none()

            connections.group_affiliation = connections.group_affiliation if form.group_affiliation.data == "" else form.group_affiliation.data
            connections.relatives = connections.relatives if form.relatives.data == "" else form.relatives.data

            db.session.commit()

            return redirect(f'/mylist/view/{superheroinfo.id}')
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/mylist/view')
        
    return render_template('/mylist/add_connections.html', form=form)

@mylist.route("/mylist/delete/<int:superheroinfo_id>", methods=["POST"])
def mylist_delete_superhero(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    get_superhero = db.session.query(MySuperheros).filter_by(user_id=g.user.id).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()

    db.session.delete(get_superhero)
    db.session.commit()

    flash("Deleted superhero from list", "success")
    return redirect('mylist/view')