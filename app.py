import requests
from flask import Flask, render_template
from models import db, User
from forms import *
from flask_migrate import Migrate
from riot_api_calls import *
from keys import RIOT_API_KEY
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///LoC_db'
app.config['SECRET_KEY'] = 'sage123'



db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def show_home():
    return "<p>Helo, world!</p>"

@app.route("/sign_up", methods=['GET','POST'])
def sign_up_form():
    form = SignUpForm()

    if form.validate_on_submit():
        summoner_name = form.summoner_name.data
        email = form.email.data
        password = form.password.data
        region = form.region.data
        summoner_data = get_summoner_data(RIOT_API_KEY, summoner_name, region)

        print(summoner_data)

        if summoner_data:
            puuid = summoner_data['puuid']
            profile_icon_id = summoner_data['profileIconId']

            User.create_account(puuid, email, password, region, summoner_name, profile_icon_id)
            db.session.commit()

            return summoner_data
        else:
            return "Error: Failed to retrieve summoner data"
    
    else:
        return render_template("sign_up.html", form=form)