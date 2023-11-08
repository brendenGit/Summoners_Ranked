from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, PasswordField, IntegerRangeField, BooleanField
from wtforms.validators import InputRequired, AnyOf, NumberRange, URL

class SignUpForm(FlaskForm):
    """Form for creating an account (signing up to LoC)."""
    
    sign_up_email = StringField("Email", validators=[InputRequired()])
    sign_up_password = PasswordField("Password", validators=[InputRequired()])
    region = SelectField('Region', choices=[('NA1', 'North America'), 
                                      ('EUW1', 'Europe West'), 
                                      ('EUN1', 'Europe Nordic & East'),
                                      ('BR1', 'Brazil'),
                                      ('JP1', 'Japan'), 
                                      ('KR', 'Korea')])
    summoner_name = StringField("Summoner Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging in"""
    
    email = StringField('Email', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class AddFriendForm(FlaskForm):
    """Form for adding a friend to a users friends list"""
    
    friend_summoner_name = StringField("Summoner Name", validators=[InputRequired()])
    friend_region = SelectField('Region', choices=[('NA1', 'North America'), 
                                      ('EUW1', 'Europe West'), 
                                      ('EUN1', 'Europe Nordic & East'),
                                      ('BR1', 'Brazil'),
                                      ('JP1', 'Japan'), 
                                      ('KR', 'Korea')])


class CreateLeaderboardForm(FlaskForm):
    """Form for creating a new leaderboard"""
    
    game_type = SelectField('Game Mode', choices=[(450, 'ARAM'), 
                                      (420, 'Ranked Solo Queue')])
    
    ranked_by = SelectField('Compare by', choices=[('win', 'Wins / Losses'), 
                                      ('totalDamageDealtToChampions', 'Total Damage to Champs'), 
                                      ('kills', 'Kills'),
                                      ('deaths', 'Deaths')])
    
    number_of_games = IntegerRangeField("Number of Games",
                                        default=20,
                                        render_kw={'min': 1, 'max': 100})
    
    # friends_to_compare = BooleanField('Friends to Compare', validators=[InputRequired()])