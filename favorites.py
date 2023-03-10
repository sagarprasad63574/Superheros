"""
Routes for favorites list. A user is able to view all superheros added to their favorties list.
User is able to view more details about a superhero and the user is able to delete a superhero from their list.
"""
from flask import Flask, redirect, render_template, Blueprint, flash, session, g
from sqlalchemy import desc
from models import db, Superheros, SuperheroInfo, Powerstats, Biography, Appearance, Work, Connections
from forms import SearchOrderForm

favorites = Blueprint("favorites", __name__, static_folder="static", template_folder="templates")

@favorites.route("/favorites/view", methods=["GET", "POST"])
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

@favorites.route("/favorites/view/<int:superheroinfo_id>", methods=["GET"])
def view_superheroinfo_by_id(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    get_superhero = check_favorites_list(superheroinfo_id)

    if get_superhero: 
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
    else: 
        flash("No superhero found in list!", "danger")
        return redirect('/favorites/view')

@favorites.route("/favorites/delete/<int:superheroinfo_id>", methods=["POST"])
def delete_superhero_from_list(superheroinfo_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    get_superhero = check_favorites_list(superheroinfo_id)
    if get_superhero:
        db.session.delete(get_superhero)
        db.session.commit()

        flash("Deleted superhero from list", "success")
        return redirect('favorites/view')
    else:
        flash("No superhero found in list!", "danger")
        return redirect('/favorites/view')

def check_favorites_list(id):
    in_favorites = db.session.query(Superheros).filter_by(user_id=g.user.id).filter_by(superheroinfo_id=id).one_or_none()

    return in_favorites