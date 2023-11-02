from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, validators, TextAreaField, BooleanField, SelectField
from wtforms.validators import InputRequired, AnyOf, NumberRange, URL

class SignUpForm(FlaskForm):
    """Form for creating an account (signing up to LoC)."""
    
    email = StringField("Email", validators=[InputRequired()])
    password = StringField("Password", validators=[InputRequired()])
    region = SelectField('', choices=[('NA1', 'North America'), 
                                      ('EUW1', 'Europe West'), 
                                      ('EUN1', 'Europe Nordic & East'),
                                      ('BR1', 'Brazil'),
                                      ('JP1', 'Japan'), 
                                      ('KR', 'Korea')])
    summoner_name = StringField("Summoner Name", validators=[InputRequired()])