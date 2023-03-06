"""
Routes for API search. The user is able to enter a name of a superhero and 
the returned response is a list of the superheros gathered from the API. 
The user is able to  view more details about a superhero and 
a user is able to add a superhero to their favorties list. 
"""
import os
import requests, json
from flask import Flask, redirect, render_template, Blueprint, request, flash, session, g
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from models import db, Superheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections
from forms import SearchForm
API_KEY = "https://www.superheroapi.com/api.php/1406925980051610/"

api = Blueprint("api", __name__, static_folder="static", template_folder="templates")

@api.route("/api/search", methods=["GET", "POST"])
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


@api.route("/api/superhero/<int:superhero_id>/view", methods=["GET"])
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

@api.route("/api/superhero/<int:superhero_id>/add", methods=["POST"])
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