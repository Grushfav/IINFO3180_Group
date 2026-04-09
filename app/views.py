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
from datetime import datetime, date
import os

def form_errors(form):
    """Collects form errors"""
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)
    return error_messages


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
    try:
        data = request.get_json()
        if not data:
            return jsonify({"errors": ["No JSON data provided"]}), 400
        
        form = SignupForm(data=data, meta={'csrf': False})
        if form.validate():
            user = User(email=form.email.data, username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            # Parse date_of_birth if provided
            dob = date(2000, 1, 1)  # Default date
            dob_str = data.get("date_of_birth")
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                except ValueError:
                    return jsonify({"errors": ["Invalid date format for date_of_birth, use YYYY-MM-DD"]}), 400
            
            # Create a starter profile
            profile = Profile(
                user_id=user.id,
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
                date_of_birth=dob,  
                gender=data.get("gender", "unspecified")
            )
            db.session.add(profile)
            db.session.commit()

            return jsonify({"message": "Account created successfully!", "user_id": user.id}), 201
        return jsonify({"errors": form_errors(form)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"errors": ["No JSON data provided"]}), 400
        
        form = LoginForm(data=data, meta={'csrf': False})
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                return jsonify({"message": "Logged in successfully!", "user_id": user.id}), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401
        return jsonify({"errors": form_errors(form)}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200


@app.route("/api/profile", methods=["GET", "POST"])
@login_required
def profile():
    try:
        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"errors": ["No JSON data provided"]}), 400
            
            form = ProfileForm(data=data, meta={'csrf': False})
            if form.validate():
                user_profile = current_user.profile
                user_profile.first_name = form.first_name.data
                user_profile.last_name = form.last_name.data
                
                # Parse date_of_birth properly
                dob_str = data.get("date_of_birth")
                if dob_str:
                    try:
                        user_profile.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
                    except (ValueError, TypeError):
                        return jsonify({"errors": ["Invalid date format for date_of_birth, use YYYY-MM-DD"]}), 400
                
                user_profile.gender = form.gender.data
                user_profile.bio = form.bio.data
                user_profile.location = form.location.data
                user_profile.occupation = form.occupation.data
                user_profile.education_level = form.education_level.data
                user_profile.relationship_goal = form.relationship_goal.data
                db.session.commit()
                return jsonify({"message": "Profile updated successfully!"}), 200
            return jsonify({"errors": form_errors(form)}), 400
        else:
            user_profile = current_user.profile
            return jsonify({
                "first_name": user_profile.first_name,
                "last_name": user_profile.last_name,
                "date_of_birth": user_profile.date_of_birth.isoformat() if user_profile.date_of_birth else None,
                "gender": user_profile.gender,
                "bio": user_profile.bio,
                "location": user_profile.location,
                "occupation": user_profile.occupation,
                "education_level": user_profile.education_level,
                "relationship_goal": user_profile.relationship_goal
            }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/password-reset", methods=["POST"])
def password_reset():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"errors": ["No JSON data provided"]}), 400
        
        form = PasswordResetForm(data=data, meta={'csrf': False})
        if form.validate():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                return jsonify({"message": "Password reset email sent!"}), 200
            return jsonify({"error": "Email not found"}), 404
        return jsonify({"errors": form_errors(form)}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/upload-photo", methods=["POST"])
@login_required
def upload_photo():
    try:
        if 'photo' not in request.files:
            return jsonify({"errors": ["No photo file provided"]}), 400
        
        photo = request.files['photo']
        if photo.filename == '':
            return jsonify({"errors": ["No file selected"]}), 400
        
        # Save the photo file
        filename = f"{current_user.id}_profile.jpg"
        upload_dir = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        photo.save(os.path.join(upload_dir, filename))
        
        # Update profile with photo path
        current_user.profile.profile_photo = filename
        db.session.commit()
        
        return jsonify({"message": "Photo uploaded successfully!", "photo_url": f"/static/uploads/{filename}"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500

@app.route("/api/preferences", methods=["GET", "POST"])
@login_required
def preferences():
    try:
        if request.method == "POST":
            data = request.get_json()
            if not data:
                return jsonify({"errors": ["No JSON data provided"]}), 400
            
            form = PreferenceForm(data=data, meta={'csrf': False})
            if form.validate():
                # TODO: Save preferences to database
                return jsonify({"message": "Preferences saved!"}), 200
            return jsonify({"errors": form_errors(form)}), 400
        else:
            # Return current preferences
            return jsonify({"min_age": 18, "max_age": 99, "gender": "any", "location": ""}), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/message", methods=["POST"])
@login_required
def send_message():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"errors": ["No JSON data provided"]}), 400
        
        form = MessageForm(data=data, meta={'csrf': False})
        recipient_id = data.get('recipient_id')
        
        if form.validate() and recipient_id:
            # TODO: Implement message storage
            # message = Message(sender_id=current_user.id, recipient_id=recipient_id, text=form.text.data)
            # db.session.add(message)
            # db.session.commit()
            return jsonify({"message": "Message sent!"}), 200
        
        if not recipient_id:
            return jsonify({"errors": ["recipient_id is required"]}), 400
        
        return jsonify({"errors": form_errors(form)}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/report", methods=["POST"])
@login_required
def report_user():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"errors": ["No JSON data provided"]}), 400
        
        form = ReportForm(data=data, meta={'csrf': False})
        reported_user_id = data.get('reported_user_id')
        
        if form.validate() and reported_user_id:
            # TODO: Implement report storage
            # report = Report(reporter_id=current_user.id, reported_user_id=reported_user_id, reason=form.reason.data)
            # db.session.add(report)
            # db.session.commit()
            return jsonify({"message": "User reported!"}), 200
        
        if not reported_user_id:
            return jsonify({"errors": ["reported_user_id is required"]}), 400
        
        return jsonify({"errors": form_errors(form)}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


