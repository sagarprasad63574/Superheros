"""SQLAlchemy models for Superheros."""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    full_name = db.Column(
        db.Text,
        nullable=False,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique = True,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )

    superheros = db.relationship(
        'SuperheroInfo',
        secondary="superheros"
    )

class Superheros(db.Model):

    __tablename__ = 'superheros' 

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
    )

    superheroinfo_id = db.Column(
        db.Integer,
        db.ForeignKey('superheroinfos.id', ondelete='cascade'),
        unique=True,
    )


class MySuperheros(db.Model):

    __tablename__ = 'mysuperheros' 

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
    )

    superheroinfo_id = db.Column(
        db.Integer,
        db.ForeignKey('superheroinfos.id', ondelete='cascade'),
        unique=True,
    )

class SuperheroInfo(db.Model):

    __tablename__ = 'superheroinfos'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    superhero_id = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    full_name = db.Column(
        db.Text,
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        default="",
    )

    powerstats = db.relationship('Powerstats')


class Powerstats(db.Model):

    __tablename__ = 'powerstats'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    superheroinfo_id = db.Column(
        db.Integer,
        db.ForeignKey('superheroinfos.id', ondelete='CASCADE'),
        nullable=False,
    )

    intelligence = db.Column(
        db.Text,
    )

    strength = db.Column(
        db.Text,
    )

    speed = db.Column(
        db.Text,
    )

    durability = db.Column(
        db.Text,
    )

    power = db.Column(
        db.Text,
    )

    combat = db.Column(
        db.Text,
    )

    superheroinfo = db.relationship('SuperheroInfo')

def connect_db(app):

    db.app = app
    db.init_app(app)