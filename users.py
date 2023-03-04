import os
import requests, json
from flask import Flask, redirect, render_template, Blueprint, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import db, connect_db, User, MySuperheros, Superheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections
from forms import SignUpForm, LoginForm, UserEditForm, SearchForm, SearchOrderForm, ImageForm, SuperheroForm, PowerstatsForm, BiographyForm, AppearanceForm, WorkForm, ConnectionsForm

users = Blueprint("users", __name__, static_folder="static", template_folder="templates")

@users.route('/user/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    return render_template('users/profile.html', user=user)

@users.route('/user/edit/<int:user_id>', methods=["GET", "POST"])
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

@users.route("/users/search", methods=["GET", "POST"])
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

            if results: 
                return render_template('/users/search.html', form=form, results=results)
            else:
                flash("No superhero found with that name", 'danger')
                return redirect('/users/search')

        except IntegrityError:
            flash("No superhero found with that name", 'danger')
            return render_template('/users/search.html', form=form)

    return render_template('/users/search.html', form=form)

@users.route("/users/view/superhero/<int:superheroinfo_id>", methods=["GET"])
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

@users.route("/users/add/superhero/<int:superheroinfo_id>", methods=["POST"])
def add_superhero_to_favorties(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    superheroinfo = db.session.query(SuperheroInfo).filter_by(id=superheroinfo_id).one_or_none()

    if superheroinfo:
        in_favorites = db.session.query(Superheros).filter_by(user_id=g.user.id).filter_by(superheroinfo_id=superheroinfo_id).one_or_none()

        if in_favorites:
            flash("Superhero already in favorties", 'danger')
            return redirect('/users/search')
        else: 
            g.user.superheros.append(superheroinfo)
            db.session.commit()
                
            flash(f"Superhero ({superheroinfo.name}) added!", 'success')
            return redirect('/users/search')