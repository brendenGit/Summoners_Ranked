from flask import Flask
from models import db
from flask_migrate import Migrate
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///LoC_db'
app.config['SECRET_KEY'] = 'sage123'

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def show_home():
    return "<p>Helo, world!</p>"