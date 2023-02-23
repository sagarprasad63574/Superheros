import os

from flask import Flask, redirect, render_template, request, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, SuperheroInfo, Powerstats, User, Superheros

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///superhero-app'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()


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

    return render_template("home.html")