from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    profile = db.relationship("Profile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    matches_sent = db.relationship("Match", foreign_keys="Match.sender_id", back_populates="sender", cascade="all, delete-orphan")
    matches_received = db.relationship("Match", foreign_keys="Match.receiver_id", back_populates="receiver", cascade="all, delete-orphan")
    messages = db.relationship("Message", back_populates="sender", cascade="all, delete-orphan")
    favourites = db.relationship("Favourite", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Interest(db.Model):
    __tablename__ = "interest"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    profiles = db.relationship("ProfileInterest", back_populates="interest", cascade="all, delete-orphan")


class Profile(db.Model):
    __tablename__ = "profile"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    looking_for = db.Column(db.String(20), default="any", nullable=False)
    bio = db.Column(db.Text)
    location = db.Column(db.String(100))
    profile_photo = db.Column(db.String(255))
    occupation = db.Column(db.String(100))
    education_level = db.Column(db.String(50))
    height_cm = db.Column(db.SmallInteger)
    relationship_goal = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=True, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="profile")
    interests = db.relationship("ProfileInterest", back_populates="profile", cascade="all, delete-orphan")
    favourites = db.relationship("Favourite", back_populates="profile", cascade="all, delete-orphan")


class ProfileInterest(db.Model):
    __tablename__ = "profile_interest"
    
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id", ondelete="CASCADE"), primary_key=True)
    interest_id = db.Column(db.Integer, db.ForeignKey("interest.id", ondelete="CASCADE"), primary_key=True)

    profile = db.relationship("Profile", back_populates="interests")
    interest = db.relationship("Interest", back_populates="profiles")


class Match(db.Model):
    __tablename__ = "match"
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    status = db.Column(db.String(20), default="liked", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    sender = db.relationship("User", foreign_keys=[sender_id], back_populates="matches_sent")
    receiver = db.relationship("User", foreign_keys=[receiver_id], back_populates="matches_received")
    messages = db.relationship("Message", back_populates="match", cascade="all, delete-orphan")


class Message(db.Model):
    __tablename__ = "message"
    
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey("match.id", ondelete="CASCADE"), nullable=False)
    sender_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    match = db.relationship("Match", back_populates="messages")
    sender = db.relationship("User", back_populates="messages")


class Favourite(db.Model):
    __tablename__ = "favourite"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id", ondelete="CASCADE"), nullable=False)
    saved_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="favourites")
    profile = db.relationship("Profile", back_populates="favourites")
