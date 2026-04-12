"""
Flask API views for DriftDater
"""

from . import app
from flask import request, jsonify, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from .db import db
from .model import User, Profile, Interest, ProfileInterest, Match, Message, Favourite
from .forms import SignupForm, LoginForm, ProfileForm, PhotoUploadForm
from datetime import datetime, date
import os
from sqlalchemy import or_, and_


def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = "Error in the %s field - %s" % (
                getattr(form, field).label.text, error)
            error_messages.append(message)
    return error_messages


def profile_to_dict(profile, include_user=False):
    """Serialize a Profile + its User to a dict the frontend expects."""
    age = None
    if profile.date_of_birth:
        today = date.today()
        dob = profile.date_of_birth
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

    interests = [pi.interest.name for pi in profile.interests]

    data = {
        "id": profile.id,
        "user_id": profile.user_id,
        "first_name": profile.first_name,
        "last_name": profile.last_name,
        "date_of_birth": profile.date_of_birth.isoformat() if profile.date_of_birth else None,
        "age": age,
        "gender": profile.gender,
        "looking_for": profile.looking_for,
        "bio": profile.bio,
        "location": profile.location,
        "profile_photo": profile.profile_photo,
        "occupation": profile.occupation,
        "education_level": profile.education_level,
        "height_cm": profile.height_cm,
        "relationship_goal": profile.relationship_goal,
        "interests": interests,
        "is_public": profile.is_public,
    }

    if include_user and profile.user:
        data["username"] = profile.user.username
        data["email"] = profile.user.email

    return data


# ── Health check ──────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return jsonify(message="DriftDater API is running")


# ── Auth ──────────────────────────────────────────────────────────────────────

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
            db.session.flush()  # Get the user.id before committing

            dob = date(2000, 1, 1)
            dob_str = data.get("date_of_birth")
            if dob_str:
                try:
                    dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
                except ValueError:
                    return jsonify({"errors": ["Invalid date format, use YYYY-MM-DD"]}), 400

            profile = Profile(
                user_id=user.id,
                first_name=data.get("first_name", ""),
                last_name=data.get("last_name", ""),
                date_of_birth=dob,
                gender=data.get("gender", "other"),
                looking_for=data.get("looking_for", "any"),
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
                # Update last_active
                user.last_active = datetime.utcnow()
                db.session.commit()
                return jsonify({
                    "message": "Logged in successfully!",
                    "user_id": user.id
                }), 200
            return jsonify({"error": "Invalid email or password"}), 401
        return jsonify({"errors": form_errors(form)}), 400
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully!"}), 200


# ── Profile ───────────────────────────────────────────────────────────────────

@app.route("/api/profile", methods=["GET", "POST"])
@login_required
def profile():
    try:
        if request.method == "GET":
            p = current_user.profile
            if not p:
                return jsonify({"errors": ["Profile not found"]}), 404
            return jsonify(profile_to_dict(p, include_user=True)), 200

        # POST — update profile
        data = request.get_json()
        if not data:
            return jsonify({"errors": ["No JSON data provided"]}), 400

        form = ProfileForm(data=data, meta={'csrf': False})
        if form.validate():
            p = current_user.profile
            p.first_name = form.first_name.data
            p.last_name = form.last_name.data
            p.gender = form.gender.data
            p.bio = form.bio.data
            p.location = form.location.data
            p.occupation = form.occupation.data
            p.education_level = form.education_level.data
            p.relationship_goal = form.relationship_goal.data
            p.updated_at = datetime.utcnow()

            dob_str = data.get("date_of_birth")
            if dob_str:
                try:
                    p.date_of_birth = datetime.strptime(dob_str, "%Y-%m-%d").date()
                except ValueError:
                    return jsonify({"errors": ["Invalid date format"]}), 400

            # Handle looking_for (not in ProfileForm but sent by frontend)
            if data.get("looking_for"):
                p.looking_for = data["looking_for"]

            # Handle interests array
            if "interests" in data:
                # Clear existing
                ProfileInterest.query.filter_by(profile_id=p.id).delete()
                for name in data["interests"]:
                    name = name.strip().lower()
                    if not name:
                        continue
                    interest = Interest.query.filter_by(name=name).first()
                    if not interest:
                        interest = Interest(name=name)
                        db.session.add(interest)
                        db.session.flush()
                    pi = ProfileInterest(profile_id=p.id, interest_id=interest.id)
                    db.session.add(pi)

            db.session.commit()
            return jsonify({"message": "Profile updated successfully!"}), 200
        return jsonify({"errors": form_errors(form)}), 400
    except Exception as e:
        db.session.rollback()
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

        # Only allow images
        allowed = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        ext = photo.filename.rsplit('.', 1)[-1].lower()
        if ext not in allowed:
            return jsonify({"errors": ["File type not allowed"]}), 400

        filename = f"user_{current_user.id}_profile.{ext}"
        upload_dir = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(upload_dir, exist_ok=True)
        photo.save(os.path.join(upload_dir, filename))

        current_user.profile.profile_photo = filename
        db.session.commit()

        return jsonify({
            "message": "Photo uploaded successfully!",
            "photo_url": f"/static/uploads/{filename}"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500


# ── Users (browse / search) ───────────────────────────────────────────────────

@app.route("/api/users", methods=["GET"])
@login_required
def get_users():
    """
    Browse / search users.
    Query params: name, location, age_min, age_max, gender, interests
    Returns users whose profiles are public and excludes the current user.
    """
    try:
        query = Profile.query.join(User).filter(
            Profile.user_id != current_user.id,
            Profile.is_public == True
        )

        name = request.args.get("name")
        if name:
            query = query.filter(
                or_(
                    Profile.first_name.ilike(f"%{name}%"),
                    Profile.last_name.ilike(f"%{name}%"),
                    Profile.bio.ilike(f"%{name}%"),
                )
            )

        location = request.args.get("location")
        if location:
            query = query.filter(Profile.location.ilike(f"%{location}%"))

        gender = request.args.get("gender")
        if gender:
            query = query.filter(Profile.gender == gender)

        profiles = query.all()

        # Filter by age range in Python (age is calculated, not stored)
        age_min = request.args.get("age_min", type=int)
        age_max = request.args.get("age_max", type=int)

        def get_age(p):
            if not p.date_of_birth:
                return 0
            today = date.today()
            dob = p.date_of_birth
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age_min:
            profiles = [p for p in profiles if get_age(p) >= age_min]
        if age_max:
            profiles = [p for p in profiles if get_age(p) <= age_max]

        # Filter by interests
        interests_param = request.args.get("interests")
        if interests_param:
            wanted = [i.strip().lower() for i in interests_param.split(",")]
            profiles = [
                p for p in profiles
                if any(pi.interest.name in wanted for pi in p.interests)
            ]

        result = [profile_to_dict(p) for p in profiles]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/users/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id):
    """Get a specific user's public profile."""
    try:
        profile = Profile.query.filter_by(user_id=user_id).first()
        if not profile:
            return jsonify({"error": "User not found"}), 404
        if not profile.is_public and profile.user_id != current_user.id:
            return jsonify({"error": "Profile is private"}), 403
        return jsonify(profile_to_dict(profile)), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


# ── Matches ───────────────────────────────────────────────────────────────────

@app.route("/api/matches", methods=["GET"])
@login_required
def get_matches():
    """Get all mutual matches (both users liked each other)."""
    try:
        # A mutual match = status is 'matched'
        matches = Match.query.filter(
            or_(
                Match.sender_id == current_user.id,
                Match.receiver_id == current_user.id,
            ),
            Match.status == "matched"
        ).all()

        result = []
        for m in matches:
            other_user_id = m.receiver_id if m.sender_id == current_user.id else m.sender_id
            other_profile = Profile.query.filter_by(user_id=other_user_id).first()
            if other_profile:
                result.append({
                    "id": m.id,
                    "matched_at": m.created_at.isoformat(),
                    "user": profile_to_dict(other_profile)
                })

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/matches/potential", methods=["GET"])
@login_required
def get_potential_matches():
    """
    Get profiles the current user hasn't liked or passed yet.
    Basic matching: filters by the user's looking_for preference.
    """
    try:
        # IDs already acted on
        acted_ids = db.session.query(Match.receiver_id).filter(
            Match.sender_id == current_user.id
        ).all()
        acted_ids = {r[0] for r in acted_ids}
        acted_ids.add(current_user.id)

        my_profile = current_user.profile
        target_gender = my_profile.looking_for if my_profile else "any"

        query = Profile.query.join(User).filter(
            Profile.user_id.notin_(acted_ids),
            Profile.is_public == True
        )

        if target_gender and target_gender != "any":
            query = query.filter(Profile.gender == target_gender)

        profiles = query.order_by(Profile.updated_at.desc()).limit(20).all()

        def match_score(p):
            if not my_profile or not p.interests:
                return 50
            my_interests = {pi.interest.name for pi in my_profile.interests}
            their_interests = {pi.interest.name for pi in p.interests}
            if not my_interests:
                return 50
            shared = len(my_interests & their_interests)
            total = len(my_interests | their_interests)
            return round((shared / total) * 100) if total else 50

        result = []
        for p in profiles:
            d = profile_to_dict(p)
            d["match_score"] = match_score(p)
            result.append(d)

        result.sort(key=lambda x: x["match_score"], reverse=True)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/matches/like/<int:user_id>", methods=["POST"])
@login_required
def like_user(user_id):
    """Like a user. If they already liked you, it's a mutual match."""
    try:
        if user_id == current_user.id:
            return jsonify({"error": "Cannot like yourself"}), 400

        # Check if already liked
        existing = Match.query.filter_by(
            sender_id=current_user.id, receiver_id=user_id
        ).first()
        if existing:
            return jsonify({"message": "Already liked"}), 200

        # Check if they already liked us
        reverse = Match.query.filter_by(
            sender_id=user_id, receiver_id=current_user.id
        ).first()

        new_match = Match(
            sender_id=current_user.id,
            receiver_id=user_id,
            status="liked"
        )
        db.session.add(new_match)

        matched = False
        if reverse:
            # Mutual match!
            reverse.status = "matched"
            new_match.status = "matched"
            matched = True

        db.session.commit()

        return jsonify({
            "message": "Matched!" if matched else "Liked!",
            "matched": matched,
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/matches/pass/<int:user_id>", methods=["POST"])
@login_required
def pass_user(user_id):
    """Pass/dislike a user so they don't show up again."""
    try:
        existing = Match.query.filter_by(
            sender_id=current_user.id, receiver_id=user_id
        ).first()
        if not existing:
            new_match = Match(
                sender_id=current_user.id,
                receiver_id=user_id,
                status="blocked"  # Using blocked to mean "passed"
            )
            db.session.add(new_match)
            db.session.commit()
        return jsonify({"message": "Passed"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500


# ── Messages ──────────────────────────────────────────────────────────────────

def get_match_between(user_a_id, user_b_id):
    """Get the mutual match record between two users."""
    return Match.query.filter(
        Match.status == "matched",
        or_(
            and_(Match.sender_id == user_a_id, Match.receiver_id == user_b_id),
            and_(Match.sender_id == user_b_id, Match.receiver_id == user_a_id),
        )
    ).first()


@app.route("/api/messages", methods=["GET"])
@login_required
def get_conversations():
    """Get conversation list — all mutual matches with latest message."""
    try:
        matches = Match.query.filter(
            or_(Match.sender_id == current_user.id, Match.receiver_id == current_user.id),
            Match.status == "matched"
        ).all()

        result = []
        for m in matches:
            other_id = m.receiver_id if m.sender_id == current_user.id else m.sender_id
            other_profile = Profile.query.filter_by(user_id=other_id).first()
            if not other_profile:
                continue

            last_msg = Message.query.filter_by(match_id=m.id).order_by(
                Message.sent_at.desc()
            ).first()

            result.append({
                "id": m.id,
                "user": profile_to_dict(other_profile),
                "last_message": last_msg.content if last_msg else "",
                "last_message_at": last_msg.sent_at.isoformat() if last_msg else m.created_at.isoformat(),
                "unread": 0,
            })

        result.sort(key=lambda x: x["last_message_at"], reverse=True)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/messages/<int:user_id>", methods=["GET"])
@login_required
def get_messages(user_id):
    """Get message history between current user and another user."""
    try:
        match = get_match_between(current_user.id, user_id)
        if not match:
            return jsonify({"error": "No match found with this user"}), 403

        messages = Message.query.filter_by(match_id=match.id).order_by(
            Message.sent_at.asc()
        ).all()

        result = [{
            "id": m.id,
            "sender_id": m.sender_id,
            "receiver_id": user_id if m.sender_id == current_user.id else current_user.id,
            "content": m.content,
            "created_at": m.sent_at.isoformat(),
            "edited": False,
        } for m in messages]

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/messages/<int:user_id>", methods=["POST"])
@login_required
def send_message(user_id):
    """Send a message to a matched user."""
    try:
        match = get_match_between(current_user.id, user_id)
        if not match:
            return jsonify({"error": "You can only message your matches"}), 403

        data = request.get_json()
        content = data.get("content", "").strip() if data else ""
        if not content:
            return jsonify({"errors": ["Message cannot be empty"]}), 400

        msg = Message(
            match_id=match.id,
            sender_id=current_user.id,
            content=content,
        )
        db.session.add(msg)
        db.session.commit()

        return jsonify({
            "id": msg.id,
            "sender_id": msg.sender_id,
            "receiver_id": user_id,
            "content": msg.content,
            "created_at": msg.sent_at.isoformat(),
            "edited": False,
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500


# ── Favourites ────────────────────────────────────────────────────────────────

@app.route("/api/favourites", methods=["GET"])
@login_required
def get_favourites():
    favs = Favourite.query.filter_by(user_id=current_user.id).all()
    result = [profile_to_dict(f.profile) for f in favs]
    return jsonify(result), 200


@app.route("/api/favourites/<int:profile_id>", methods=["POST"])
@login_required
def add_favourite(profile_id):
    try:
        existing = Favourite.query.filter_by(
            user_id=current_user.id, profile_id=profile_id
        ).first()
        if existing:
            return jsonify({"message": "Already saved"}), 200
        fav = Favourite(user_id=current_user.id, profile_id=profile_id)
        db.session.add(fav)
        db.session.commit()
        return jsonify({"message": "Saved to favourites"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500


@app.route("/api/favourites/<int:profile_id>", methods=["DELETE"])
@login_required
def remove_favourite(profile_id):
    try:
        fav = Favourite.query.filter_by(
            user_id=current_user.id, profile_id=profile_id
        ).first()
        if fav:
            db.session.delete(fav)
            db.session.commit()
        return jsonify({"message": "Removed from favourites"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": [str(e)]}), 500


# ── Static file serving ───────────────────────────────────────────────────────

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"error": "Not found"}), 404