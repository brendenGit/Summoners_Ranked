"""Models for LoC."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


class Friends(db.Model):
    """Friends model"""

    __tablename__ = 'friends'

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )

    friend_puuid = db.Column(
        db.String, 
        nullable=False
    )
    
    friended_by_puuid = db.Column(
        db.String, 
        db.ForeignKey('users.puuid', ondelete="cascade"),
        nullable=False
    )

    #need to add methods and class methods


class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    puuid = db.Column(
        db.String, 
        primary_key=True, 
        nullable=False, 
        unique=True
    )

    email = db.Column(
        db.String, 
        unique=True, 
        nullable=False
    )
    
    password = db.Column(
        db.String, 
        nullable=False
    )

    region = db.Column(
        db.String, 
        nullable=False
    )

    friends = db.relationship(
        "Friends",
        primaryjoin=(Friends.friended_by_puuid == id),
    )

    #need to add methods and class methods



class Leaderboard(db.Model):
    """Leaderboard model"""

    __tablename__ = 'leaderboards'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    created_by = db.Column(
        db.String,
        db.ForeignKey('users.puuid', ondelete="cascade"),
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    ranked_by = db.Column(
        db.String,
        nullable=False
    )

    number_of_games = db.Column(
        db.Integer,
        nullable=False,
        default=20
    )

    #need to add methods and class methods

class Performance(db.Model):
    """
    Model for performances

    This model holds data about an individual player's performance across a 
    set of games. This data is linked to a single leaderboard
    """

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )

    puuid = db.Column(
        db.String,
        nullable=False
    )

    perf_metric = db.Column(
        db.String,
        nullable=False
    )

    leaderboard_id = db.Column(
        db.Integer,
        db.ForeignKey('leaderboards.id', ondelete="cascade"),
        nullable=False
    )

    score = db.Column(
        db.Integer,
        nullable=False
    )

    #need to add methods and class methods