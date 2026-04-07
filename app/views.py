"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from . import app
from flask import render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from .model import db, User, Profile
from .forms import SignupForm, LoginForm, ProfileForm, PasswordResetForm, PhotoUploadForm, PreferenceForm, MessageForm, ReportForm
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


###
# The functions below should be applicable to all Flask apps.
###

# Here we define a function to collect form errors from Flask-WTF
# which we can later use






@app.route("/api/signup", methods=["POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Create a starter profile
        profile = Profile(
            user_id=user.id,
            first_name="",
            last_name="",
            date_of_birth="2000-01-01",  
            gender="unspecified"
        )
        db.session.add(profile)
        db.session.commit()

        return jsonify({"message": "Account created successfully!", "user_id": user.id}), 201
    return jsonify({"errors": form_errors(form)}), 400


@app.route("/api/login", methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return jsonify({"message": "Logged in successfully!", "user_id": user.id}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    return jsonify({"errors": form_errors(form)}), 400


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200


@app.route("/api/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        form = ProfileForm()
        if form.validate_on_submit():
            profile = current_user.profile
            profile.first_name = form.first_name.data
            profile.last_name = form.last_name.data
            profile.date_of_birth = form.date_of_birth.data
            profile.gender = form.gender.data
            profile.bio = form.bio.data
            profile.location = form.location.data
            profile.occupation = form.occupation.data
            profile.education_level = form.education_level.data
            profile.relationship_goal = form.relationship_goal.data
            db.session.commit()
            return jsonify({"message": "Profile updated successfully!"}), 200
        return jsonify({"errors": form_errors(form)}), 400
    else:
        profile = current_user.profile
        return jsonify({
            "first_name": profile.first_name,
            "last_name": profile.last_name,
            "date_of_birth": profile.date_of_birth.isoformat() if profile.date_of_birth else None,
            "gender": profile.gender,
            "bio": profile.bio,
            "location": profile.location,
            "occupation": profile.occupation,
            "education_level": profile.education_level,
            "relationship_goal": profile.relationship_goal
        }), 200


@app.route("/api/password-reset", methods=["POST"])
def password_reset():
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Here you would send a password reset email
            # For now, just return success
            return jsonify({"message": "Password reset email sent!"}), 200
        return jsonify({"error": "Email not found"}), 404
    return jsonify({"errors": form_errors(form)}), 400


@app.route("/api/upload-photo", methods=["POST"])
@login_required
def upload_photo():
    form = PhotoUploadForm()
    if form.validate_on_submit():
        photo = form.photo.data
        # Save the photo file
        filename = f"{current_user.id}_profile.jpg"
        photo.save(os.path.join(app.root_path, 'static', 'uploads', filename))
        # Update profile with photo path
        current_user.profile.profile_photo = filename
        db.session.commit()
        return jsonify({"message": "Photo uploaded successfully!", "photo_url": f"/static/uploads/{filename}"}), 200
    return jsonify({"errors": form_errors(form)}), 400

@app.route("/api/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    if request.method == "POST":
        form = PreferenceForm()
        if form.validate_on_submit():
            # Assuming you have a Preferences model
            # For now, just return success
            return jsonify({"message": "Preferences saved!"}), 200
        return jsonify({"errors": form_errors(form)}), 400
    else:
        # Return current preferences
        return jsonify({"min_age": 18, "max_age": 99, "gender": "any", "location": ""}), 200


@app.route("/api/message", methods=["POST"])
@login_required
def send_message():
    form = MessageForm()
    recipient_id = request.form.get('recipient_id')
    if form.validate_on_submit() and recipient_id:
        # Assuming you have a Message model
        # message = Message(sender_id=current_user.id, recipient_id=recipient_id, text=form.text.data)
        # db.session.add(message)
        # db.session.commit()
        return jsonify({"message": "Message sent!"}), 200
    return jsonify({"errors": form_errors(form)}), 400


@app.route("/api/report", methods=["POST"])
@login_required
def report_user():
    form = ReportForm()
    reported_user_id = request.form.get('reported_user_id')
    if form.validate_on_submit() and reported_user_id:
        # Assuming you have a Report model
        # report = Report(reporter_id=current_user.id, reported_user_id=reported_user_id, reason=form.reason.data)
        # db.session.add(report)
        # db.session.commit()
        return jsonify({"message": "User reported!"}), 200
    return jsonify({"errors": form_errors(form)}), 400