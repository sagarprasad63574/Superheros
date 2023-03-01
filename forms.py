from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Optional

class SignUpForm(FlaskForm):
    """Form for adding users."""

    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired(), Length(min=6)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    image_url = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[InputRequired(), Length(min=6)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])

class UserEditForm(FlaskForm):
    """Form for editing a user."""
    
    first_name = StringField('First name', validators=[InputRequired()])
    last_name = StringField('Last name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    image_url = StringField('(Optional) Image URL')

class SearchForm(FlaskForm):
    """Search for superhero form."""
    
    name = StringField('Name of superhero', validators=[InputRequired(), Length(min=2)])

class SearchOrderForm(FlaskForm):
    """Search for superhero form."""
    
    name = StringField('Name of superhero', validators=[InputRequired(), Length(min=2)])
    order = SelectField('Order By', choices=[('asec','Name asec'), ('desc', 'Name desc')])

class ImageForm(FlaskForm):
    """Add image for superhero form."""
    
    image_url = StringField('Image URL', validators=[Optional()])


class SuperheroForm(FlaskForm):
    """Add superhero form"""

    name = StringField('Enter name of superhero', validators=[InputRequired(), Length(min=2)])

    image_url = StringField('(Optional) Image URL')

class PowerstatsForm(FlaskForm):
    """Add powerstats form"""

    intelligence = StringField('Intelligence', validators=[InputRequired(), Length(min=1)])
    strength = StringField('Strength', validators=[InputRequired(), Length(min=1)])
    speed = StringField('Speed', validators=[InputRequired(), Length(min=1)])
    durability = StringField('Durability', validators=[InputRequired(), Length(min=1)])
    power = StringField('Power', validators=[InputRequired(), Length(min=1)])
    combat = StringField('Combat', validators=[InputRequired(), Length(min=1)])

class BiographyForm(FlaskForm):
    """Add biography form"""

    full_name = StringField('Full name', validators=[Optional()])
    place_of_birth = StringField('Place of birth', validators=[Optional()])
    first_appearance = StringField('First appearance', validators=[Optional()])
    alter_egos = StringField('Alter egos', validators=[Optional()])
    publisher = StringField('Publisher', validators=[Optional()])

class AppearanceForm(FlaskForm):
    """Add appearance form"""

    gender = StringField('Gender', validators=[Optional()])
    race = StringField('Race', validators=[Optional()])
    height = StringField('Height', validators=[Optional()])
    weight = StringField('Weight', validators=[Optional()])
    eye_color = StringField('Eye color', validators=[Optional()])
    hair_color = StringField('Hair color', validators=[Optional()])

class WorkForm(FlaskForm):
    """Add work form"""

    occupation = StringField('Occupation', validators=[Optional()])
    base_of_operation = StringField('Base', validators=[Optional()])

class ConnectionsForm(FlaskForm):
    """Add connections form"""

    group_affiliation = StringField('Group affiliations', validators=[Optional()])
    relatives = TextAreaField('Relatives', validators=[Optional()])