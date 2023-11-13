import requests
from models_forms.forms import *
from models_forms.models import *
from flask import Flask, render_template, request, jsonify, flash, redirect, session, g, url_for
from utils.backend_funcs import *
from flask_migrate import Migrate
from utils.riot_api_calls import *
from keys import RIOT_API_KEY
from sqlalchemy.exc import IntegrityError
import os


CURR_USER_KEY = "curr_user"

app = Flask(__name__)

with app.app_context():

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dlfgbfgw:P-GAR-WSsDZCCrt3eLkRRkMDp1g7x8bq@bubble.db.elephantsql.com/dlfgbfgw'
    app.config['SECRET_KEY'] = 'sage123'
    db.init_app(app)
    db.create_all()

    ##############################################################################
    # Main routes for user sign in/sign up and the main page

    @app.route("/")
    def start():
        if g.user:
            return redirect("/home")
        
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
            user = User.authenticate(form.username.data,
                                    form.password.data)

            if user:
                do_login(user)
                flash(f"Hello, {user.summoner_name}!","success")
                return redirect(url_for('show_home')), 302
            
            response = {"error": "Invalid username or password!"}
            return jsonify(response), 401

        return redirect('/')



    @app.route('/logout')
    def logout():
        """Handle logout of user."""
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/"), 401
        
        do_logout()
        flash("Successfully logged out.", "success")
        return redirect("/"), 302



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
                        username = form.sign_up_username.data,
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
                    response = {"error": "Account with that username or summoner name is already taken"}
                    return jsonify(response), 400
            else:
                response = {"error": "Failed to retrieve summoner data"}
                return jsonify(response), 500

        else:
            errors = form.errors
            response = {"error": "Form validation failed", "form_errors": errors}
            return jsonify(response), 400
        



    ##############################################################################
    # Add friends

    @app.route("/add_friend", methods=['GET', 'POST'])
    def add_friend_form():
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/"), 302
        
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

                try:
                    Friends.add_friend(friend_puuid,
                                    friended_by_puuid,
                                    friend_profile_icon, 
                                    friend_summoner_name,
                                    friend_region
                                    )
                    db.session.commit()

                    response = {"success": f"Successfully added {friend_summoner_name}",
                                "friend_puuid": friend_puuid,
                                "friend_summoner_name": friend_summoner_name}
                    return jsonify(response), 200

                except IntegrityError as e:
                    db.session.rollback()

                    if 'unique constraint' in str(e).lower():
                        response = {"error": "Friend already added"}
                        return jsonify(response), 400
                    else:
                        response = {"error": "Failed to add friend due to an integrity error"}
                        return jsonify(response), 500

            else:
                response = {"error": "Failed to retrieve summoner data"}
                return jsonify(response), 500
        
        else:
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
            number_of_games = form.number_of_games.data

            leaderboard = Leaderboard.create_leaderboard(created_by,
                                                        game_type,
                                                        number_of_games)
            db.session.add(leaderboard)
            db.session.commit()

            personal_performance = per_performance(api_key=RIOT_API_KEY,
                                                puuid=created_by,
                                                queue=game_type,
                                                num_games=number_of_games)

            personal_perf = Performance.create_performance(puuid=created_by,
                                        summoner_name=g.user.summoner_name,
                                        leaderboard_id=leaderboard.id,
                                        kills=personal_performance['Kills'],
                                        deaths=personal_performance['Deaths'],
                                        wins=personal_performance['Wins'],
                                        losses=personal_performance['Losses'],
                                        total_damage_dealt=personal_performance['Total Damage Dealt'],
                                        total_damage_taken=personal_performance['Total Damage Taken'],
                                        kda=round(personal_performance['KDA'], 1))
            db.session.add(personal_perf)
            db.session.commit()

            for puuid in selected_friends:
                score = friends_performance(api_key=RIOT_API_KEY,
                                            puuid=puuid,
                                            queue=game_type,
                                            num_games=number_of_games)
                
                friend = Friends.query.filter_by(friend_puuid=puuid).first()
                
                performance = Performance.create_performance(puuid=created_by,
                                            summoner_name=friend.friend_summoner_name,
                                            leaderboard_id=leaderboard.id,
                                            kills=score['Kills'],
                                            deaths=score['Deaths'],
                                            wins=score['Wins'],
                                            losses=score['Losses'],
                                            total_damage_dealt=score['Total Damage Dealt'],
                                            total_damage_taken=score['Total Damage Taken'],
                                            kda=round(score['KDA'], 1))
                
                db.session.add(performance)
                db.session.commit()

            perf_data = get_perf_data(leaderboard.performances)

            return jsonify(perf_data)
        
        else:
            errors = form.errors
            response = {"error": "Form validation failed", "form_errors": errors}
            return jsonify(response), 400