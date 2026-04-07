from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField, SelectField, TextAreaField, FileField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .model import User

class SignupForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Sign Up")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already registered.")

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("Username already taken.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class ProfileForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(max=50)])
    last_name = StringField("Last Name", validators=[DataRequired(), Length(max=50)])
    date_of_birth = DateField("Date of Birth", validators=[DataRequired()])
    gender = SelectField("Gender", choices=[("male", "Male"), ("female", "Female"), ("other", "Other")], validators=[DataRequired()])
    bio = TextAreaField("Bio", validators=[Length(max=500)])
    location = StringField("Location", validators=[Length(max=100)])
    occupation = StringField("Occupation", validators=[Length(max=100)])
    education_level = StringField("Education Level", validators=[Length(max=50)])
    relationship_goal = StringField("Relationship Goal", validators=[Length(max=50)])
    submit = SubmitField("Save Profile")


class PhotoUploadForm(FlaskForm):
    photo = FileField("Profile Picture", validators=[DataRequired()])
    submit = SubmitField("Upload")


class MessageForm(FlaskForm):
    text = TextAreaField("Message", validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField("Send")

class PasswordResetForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Reset Password")

class PreferenceForm(FlaskForm):
    min_age = IntegerField("Minimum Age", validators=[DataRequired()])
    max_age = IntegerField("Maximum Age", validators=[DataRequired()])
    gender = SelectField("Preferred Gender", choices=[("male", "Male"), ("female", "Female"), ("other", "Other"), ("any", "Any")], validators=[DataRequired()])
    location = StringField("Preferred Location", validators=[Length(max=100)])
    submit = SubmitField("Save Preferences")

class ReportForm(FlaskForm):
    reason = TextAreaField("Reason", validators=[DataRequired()])
    submit = SubmitField("Report User")


