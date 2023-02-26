from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length

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

class SearchForm(FlaskForm):
    """Search for superhero form."""
    
    name = StringField('Name of superhero', validators=[InputRequired(), Length(min=2)])