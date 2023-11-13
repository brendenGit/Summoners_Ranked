"""Models for LoC."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.schema import UniqueConstraint



bcrypt = Bcrypt()
db = SQLAlchemy()


class Performance(db.Model):
    """
    Model for performances

    This model holds data about an individual player's performance across a 
    set of games. This data is linked to a single leaderboard
    """

    __tablename__ = 'performances'

    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )

    puuid = db.Column(
        db.String,
        nullable=False
    )

    summoner_name = db.Column(
        db.String,
        nullable=False
    )

    leaderboard_id = db.Column(
        db.Integer,
        db.ForeignKey('leaderboards.id', ondelete="cascade"),
        nullable=False
    )

    kills = db.Column(
        db.Integer,
    )

    deaths = db.Column(
        db.Integer,
    )

    wins = db.Column(
        db.Integer,
    )

    losses = db.Column(
        db.Integer,
    )

    total_damage_dealt = db.Column(
        db.Integer,
    )

    total_damage_taken = db.Column(
        db.Integer,
    )

    kda = db.Column(
        db.Float,
    )

    #need to add methods and class methods
    @classmethod
    def create_performance(cls, 
                           puuid, 
                           summoner_name, 
                           leaderboard_id, 
                           kills, 
                           deaths, 
                           wins, 
                           losses, 
                           total_damage_dealt,
                           total_damage_taken,
                           kda):
        """Create a new performance."""

        performance = Performance(puuid=puuid, 
                                  summoner_name=summoner_name, 
                                  leaderboard_id=leaderboard_id, 
                                  kills=kills,
                                  deaths=deaths,
                                  wins=wins,
                                  losses=losses,
                                  total_damage_dealt=total_damage_dealt,
                                  total_damage_taken=total_damage_taken,
                                  kda=kda
        )

        return performance


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
        nullable=False,
    )
    
    friended_by_puuid = db.Column(
        db.String, 
        db.ForeignKey('users.puuid', ondelete="cascade"),
        nullable=False,
    )

    friend_profile_icon = db.Column(
        db.String,
        nullable=True,
        #need to set default value later
    )

    friend_summoner_name = db.Column(
        db.String,
        nullable=False
    )

    friend_region = db.Column(
        db.String,
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint('friend_puuid', 'friended_by_puuid', name='uq_friendship'),
    )

    #need to add methods and class methods
    @classmethod
    def add_friend(cls, friend_puuid, friended_by_puuid, friend_profile_icon, friend_summoner_name, friend_region):
        """Add a new friend.

        Adds a friend db entry done by the user.
        """

        friend = Friends(
            friend_puuid=friend_puuid,
            friended_by_puuid=friended_by_puuid,
            friend_profile_icon=friend_profile_icon,
            friend_summoner_name=friend_summoner_name,
            friend_region = friend_region
        )

        db.session.add(friend)

        return friend


class Leaderboard(db.Model):
    """Leaderboard model"""

    __tablename__ = 'leaderboards'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    created_by = db.Column(
        db.String,
        db.ForeignKey('users.puuid', ondelete="cascade"),
    )

    game_type = db.Column(
        db.String
    )

    number_of_games = db.Column(
        db.Integer,
        nullable=False,
        default=20
    )

    performances = db.relationship(
        "Performance",
        primaryjoin=(Performance.leaderboard_id == id),
    )

    #need to add methods and class methods
    @classmethod
    def create_leaderboard(cls, created_by, game_type, number_of_games):
        """Create a new leaderboard."""

        leaderboard = Leaderboard(
            created_by=created_by,
            game_type=game_type,
            number_of_games=number_of_games
        )

        return leaderboard



class User(db.Model):
    """User model"""

    __tablename__ = 'users'

    puuid = db.Column(
        db.String, 
        primary_key=True, 
        nullable=False, 
        unique=True
    )

    username = db.Column(
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

    summoner_name = db.Column(
        db.String,
        nullable=False
    )

    profile_icon_id =db.Column(
        db.Integer
    )

    friends = db.relationship(
        "Friends",
        primaryjoin=(Friends.friended_by_puuid == puuid),
    )

    leaderboards = db.relationship(
        "Leaderboard",
        primaryjoin=(Leaderboard.created_by == puuid),
    )

    #need to add methods and class methods
    @classmethod
    def create_account(cls, puuid, username, password, region, summoner_name, profile_icon_id):
        """Create a new user account.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            puuid=puuid,
            username=username,
            password=hashed_pwd,
            region=region,
            summoner_name=summoner_name,
            profile_icon_id=profile_icon_id
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False