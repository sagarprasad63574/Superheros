"""SQLAlchemy models for Superheros."""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    first_name = db.Column(
        db.Text,
        nullable=False,
    )

    last_name = db.Column(
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

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )
    
    superheros = db.relationship(
        'SuperheroInfo',
        secondary="superheros"
    )

    mysuperheros = db.relationship(
        'SuperheroInfo',
        secondary="mysuperheros"
    )

    def __repr__(self):
            return f"<User #{self.id}: {self.first_name}, {self.last_name}, {self.username}>"

    @classmethod
    def signup(cls, first_name, last_name, username, password):
        """Sign up user. Hashes password and adds user to system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

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
    )

    superheroinfo = db.relationship('SuperheroInfo')

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

    superheroinfo = db.relationship('SuperheroInfo')

class SuperheroInfo(db.Model):

    __tablename__ = 'superheroinfos'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    superhero_id = db.Column(
        db.Text,
        unique=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    #add the default image_url
    image_url = db.Column(
        db.Text,
        default="",
    )

    powerstats = db.relationship('Powerstats')
    biography = db.relationship('Biography')
    appearance = db.relationship('Appearance')
    work = db.relationship('Work')
    connections = db.relationship('Connections')


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
        nullable=False,
    )

    strength = db.Column(
        db.Text,
        nullable=False,
    )

    speed = db.Column(
        db.Text,
        nullable=False,
    )

    durability = db.Column(
        db.Text,
        nullable=False,
    )

    power = db.Column(
        db.Text,
        nullable=False,
    )

    combat = db.Column(
        db.Text,
        nullable=False,
    )

    superheroinfo = db.relationship('SuperheroInfo')


class Biography(db.Model):

    __tablename__ = 'biography'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    superheroinfo_id = db.Column(
        db.Integer,
        db.ForeignKey('superheroinfos.id', ondelete='CASCADE'),
        nullable=False,
    )

    full_name = db.Column(
        db.Text,
    )

    place_of_birth = db.Column(
        db.Text,
    )

    first_appearance = db.Column(
        db.Text,
    )

    alter_egos = db.Column(
        db.Text,
    )

    publisher = db.Column(
        db.Text,
    )

    superheroinfo = db.relationship('SuperheroInfo')

class Appearance(db.Model):

    __tablename__ = 'appearance'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    superheroinfo_id = db.Column(
        db.Integer,
        db.ForeignKey('superheroinfos.id', ondelete='CASCADE'),
        nullable=False,
    )

    gender = db.Column(
        db.Text,
    )

    race = db.Column(
        db.Text,
    )

    height = db.Column(
        db.Text,
    )

    weight = db.Column(
        db.Text,
    )

    eye_color = db.Column(
        db.Text,
    )

    hair_color = db.Column(
        db.Text,
    )

    superheroinfo = db.relationship('SuperheroInfo')

class Work(db.Model):

    __tablename__ = 'work'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    superheroinfo_id = db.Column(
        db.Integer,
        db.ForeignKey('superheroinfos.id', ondelete='CASCADE'),
        nullable=False,
    )

    occupation = db.Column(
        db.Text,
    )

    base_of_operation = db.Column(
        db.Text,
    )

    superheroinfo = db.relationship('SuperheroInfo')

class Connections(db.Model):

    __tablename__ = 'connections'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    superheroinfo_id = db.Column(
        db.Integer,
        db.ForeignKey('superheroinfos.id', ondelete='CASCADE'),
        nullable=False,
    )

    group_affiliation = db.Column(
        db.Text,
    )

    relatives = db.Column(
        db.Text,
    )

    superheroinfo = db.relationship('SuperheroInfo')

def connect_db(app):

    db.app = app
    db.init_app(app)