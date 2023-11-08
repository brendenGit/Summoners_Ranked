import requests
from flask import Flask, render_template, request, jsonify, flash, redirect, session, g
from models import db, User, Friends, Leaderboard
from backend_funcs import *
from forms import *
from flask_migrate import Migrate
from riot_api_calls import *
from keys import RIOT_API_KEY
from sqlalchemy.exc import IntegrityError
import os




CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///LoC_db'
app.config['SECRET_KEY'] = 'sage123'



db.init_app(app)
migrate = Migrate(app, db)

##############################################################################
# Main routes for user sign in/sign up and the main page

@app.route("/")
def start():
    login_form = LoginForm()
    sign_up_form = SignUpForm()

    return render_template(
        "start.html", 
        sign_up_form=sign_up_form,
        login_form=login_form,
        )

@app.route("/home")
def show_home():

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    add_friend_form = AddFriendForm()
    create_leaderboard_form = CreateLeaderboardForm()

    return render_template(
        "home.html", 
        add_friend_form=add_friend_form,
        create_leaderboard_form=create_leaderboard_form,
        user=g.user
        )



##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.puuid


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.email.data,
                                 form.password.data)

        if user:
            do_login(user)
            response = {"success": f"Hello, {user.summoner_name}!"}
            return jsonify(response), 200
        
        response = {"error": "Invalid username or password!"}
        return jsonify(response), 401

    return redirect('/')


@app.route('/logout')
def logout():
    """Handle logout of user."""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    do_logout()
    response = {"success": "Successfully logged out"}
    return jsonify(response), 200


@app.route("/sign_up", methods=['GET','POST'])
def sign_up_form():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """
    if g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/home")
    
    form = SignUpForm()

    if form.validate_on_submit():

        summoner_data = get_summoner_data(
            RIOT_API_KEY, 
            form.summoner_name.data, 
            form.region.data)
        
        if summoner_data:
            try:
                user = User.create_account(
                    puuid=summoner_data['puuid'],
                    email = form.sign_up_email.data,
                    password=form.sign_up_password.data,
                    region = form.region.data,
                    summoner_name=summoner_data['name'],
                    profile_icon_id=summoner_data['profileIconId']
                )
                db.session.commit()
                do_login(user)

                flash(f"{user.summoner_name}! Thanks for creating an account","success")
                return redirect("/home")
            
            except IntegrityError:
                response = {"error": "Account with that email or summoner name is already taken"}
                return jsonify(response), 400
        else:
            response = {"error": "Failed to retrieve summoner data"}
            return jsonify(response), 500

    else:
        # If form validation fails, return an error response with the form errors
        errors = form.errors
        response = {"error": "Form validation failed", "form_errors": errors}
        return jsonify(response), 400
    

##############################################################################
# Add friends

@app.route("/add_friend", methods=['GET','POST'])
def add_friend_form():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = AddFriendForm()

    if form.validate_on_submit():
        friend_summoner_name = form.friend_summoner_name.data
        friend_region = form.friend_region.data
        friend_summoner_data = get_summoner_friend_data(RIOT_API_KEY,
                                                        friend_summoner_name,
                                                        friend_region)

        if friend_summoner_data:
            friend_puuid = friend_summoner_data['puuid']
            friended_by_puuid = g.user.puuid
            friend_profile_icon = friend_summoner_data['profileIconId']
            friend_summoner_name = friend_summoner_data['name']
            friend_region = friend_region

            Friends.add_friend(friend_puuid,
                            friended_by_puuid,
                            friend_profile_icon, 
                            friend_summoner_name,
                            friend_region
                            )
            db.session.commit()

            response = {"friend_puuid":friend_puuid, "friend_summoner_name":friend_summoner_name}
            return jsonify(response), 200
        else:
            response = {"error": "Failed to retrieve summoner data"}
            return jsonify(response), 500
    
    else:
        # If form validation fails, return an error response with the form errors
        errors = form.errors
        response = {"error": "Form validation failed", "form_errors": errors}
        return jsonify(response), 400
    

##############################################################################
# Routes for creating leaderboards and performances

@app.route("/create_leaderboard", methods=['GET','POST'])
def create_leaderboard():
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    
    form = CreateLeaderboardForm()

    if form.validate_on_submit():
        selected_friends = request.form.getlist('selected_friends')
        created_by = g.user.puuid

        game_type = form.game_type.data
        ranked_by = form.ranked_by.data
        number_of_games = form.number_of_games.data

        leaderboard = Leaderboard.create_leaderboard(created_by,
                                                     game_type,
                                                     ranked_by,
                                                     number_of_games)
        db.session.commit()

        personal_performance = per_performance(api_key=RIOT_API_KEY,
                                               puuid=created_by,
                                               queue=game_type,
                                               num_games=number_of_games,
                                               ranked_by=ranked_by)
        
        Performance.create_performance(puuid=created_by,
                                       summoner_name=g.user.summoner_name,
                                       perf_metric=ranked_by,
                                       leaderboard_id=leaderboard.id,
                                       score=personal_performance)

        for puuid in selected_friends:
            score = friends_performance(api_key=RIOT_API_KEY,
                                        puuid=puuid,
                                        queue=game_type,
                                        num_games=number_of_games,
                                        ranked_by=ranked_by)
            
            friend = Friends.query.filter_by(friend_puuid=puuid).first()
            
            Performance.create_performance(puuid=puuid,
                                           summoner_name=friend.friend_summoner_name,
                                           perf_metric=ranked_by,
                                           leaderboard_id=leaderboard.id,
                                           score=score)
            
        db.session.commit()

        perf_data = get_perf_data(leaderboard.performances)
            
        return jsonify(perf_data)
    
    else:
        # If form validation fails, return an error response with the form errors
        errors = form.errors
        response = {"error": "Form validation failed", "form_errors": errors}
        return jsonify(response), 400