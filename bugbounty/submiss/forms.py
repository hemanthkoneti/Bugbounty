from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    RadioField,
    IntegerField,
    TextAreaField,
    HiddenField,
)
from wtforms.validators import DataRequired, EqualTo, NumberRange,Length
from wtforms import ValidationError
from wtforms.fields.html5 import DecimalRangeField
from flask_wtf.file import FileField, FileAllowed
from submiss.models import User,Submission


class LoginForm(FlaskForm):
    teamname = StringField("Team Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    roll = IntegerField("Roll Number of student1", validators=[DataRequired()])
    roll2=IntegerField("Roll Number of student2(If you are participating solo give the same roll number again)", validators=[DataRequired()])
    username = StringField("Team Name (Do not foget this name)", validators=[DataRequired(),Length(min=1,max=20)])
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("pass_confirm", message="Passwords must Match!"),
        ],
    )
    pass_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    submit = SubmitField("Register")

    def validate_roll(self, roll):
        if User.query.filter_by(roll=self.roll.data).first():
            raise ValidationError("Roll Number already registered!")
    def validate_roll2(self,roll2):
        if User.query.filter_by(roll2=self.roll2.data).first():
            raise ValidationError("Roll Number already registered!")
        
    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError("Teamname already registered!")


class SubmissionForm(FlaskForm):
    ans = StringField("Explanation", validators=[DataRequired()])
    picture = FileField(
        "Upload Image (jpg, png, jpeg)", validators=[FileAllowed(["jpg", "png", "jpeg"]),DataRequired()]
    )
    submit = SubmitField("Submit")


class ReviewForm(FlaskForm):
    review = RadioField("Review", choices=["Reject", "Accept","AlreadySubmitted"])
    points= IntegerField("Points")
    bug_id=IntegerField("Bug_Id")
    submission_id = HiddenField("submission_id")
    submit = SubmitField("Submit")


class AnnounceForm(FlaskForm):
    message = StringField("Announcement", validators=[DataRequired()])
    submit = SubmitField("Submit")


class NotifForm(FlaskForm):
    uid = IntegerField("User ID", validators=[DataRequired()])
    message = StringField("Notification", validators=[DataRequired()])
    submit = SubmitField("Submit")

class FeedbackForm(FlaskForm):
    feed = TextAreaField("Feedback/Querry", validators=[DataRequired()])
    submit = SubmitField("Submit")

class UserSubmissions(FlaskForm):
    uid=IntegerField("User ID", validators=[DataRequired()])
    submit = SubmitField("Submit")