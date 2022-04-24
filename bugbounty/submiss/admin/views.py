from flask import render_template, request, Blueprint, redirect, url_for, flash, abort
from flask_login import current_user
from submiss import db
from submiss.models import (
    User,
    Submission,
    Notification,
    Announcement,
    Feedback,
)
from submiss.forms import ReviewForm, AnnounceForm, NotifForm,UserSubmissions
from datetime import datetime


admin = Blueprint("admin", __name__)


def admin_required(function):
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.user_type == "Admin":
            return function()
        else:
            return abort(403)

    wrapper.__name__ = function.__name__
    return wrapper


@admin.route("/admin_dash")
@admin_required
def admin_dash():
    return render_template("admin/admin_dash.html")


@admin.route("/review", methods=["GET", "POST"])
@admin_required
def review():
    form = ReviewForm()
    submissions = Submission.query.filter_by(correct=1).all()
    users = User.query.all()
    now = datetime.now()
    prev_submission=Submission.query.filter_by(correct=2).all()
    if form.validate_on_submit():
        submission = Submission.query.filter_by(id=form.submission_id.data).first()
        user = User.query.filter_by(id=submission.by).first()
        if form.review.data == "Accept":
            submission.correct = 2
            score=user.score+form.points.data
            submission.bug_id=form.bug_id.data
            message = (
                "Congratulations! Your Submission on "
                + submission.time.strftime("%d %b %Y at %I:%M %p")
                + " has been accepted on "
                + now.strftime("%d %b %Y at %I:%M %p")
                + ". You are given "
                + str(form.points.data)
                +" points, Which brings your total score to "
                +str(score)
            )
            user.update_score(form.points.data)
            user.upgrade_time = submission.time
        elif form.review.data=="Reject":
            submission.correct = 0
            message = (
                "Oops! Your Submission on"
                + submission.time.strftime("%d %b %Y at %I:%M %p")
                + " has not been accepted on "
                + now.strftime("%d %b %Y at %I:%M %p")
                + " .As it was not correct."
            )
        elif form.review.data=="AlreadySubmitted":
            submission.correct = 0
            message = (
                "Oops! Your Submission on"
                + submission.time.strftime("%d %b %Y at %I:%M %p")
                + " has not been accepted on "
                + now.strftime("%d %b %Y at %I:%M %p")
                + " .As it has been already been accepted before."
            )

        notification = Notification(uid=user.id, message=message)

        db.session.add(notification)

        db.session.commit()
        return redirect(url_for("admin.review"))
    return render_template(
        "admin/review.html", submissions=submissions, form=form, users=users, prev_submission=prev_submission
    )


@admin.route("/announce", methods=["GET", "POST"])
@admin_required
def announce():
    form = AnnounceForm()
    if form.validate_on_submit():
        announcement = Announcement(message=form.message.data)
        db.session.add(announcement)
        db.session.commit()
        flash("Announcement Sucessfull")
        return redirect(url_for("admin.announce"))
    return render_template("admin/announce.html", form=form)


@admin.route("/all_users")
@admin_required
def all_users():
    users = User.query.order_by(User.id.asc()).all()
    return render_template("admin/users.html", users=users)


@admin.route("/dnotif", methods=["GET", "POST"])
@admin_required
def dnotif():
    form = NotifForm()
    if form.validate_on_submit():
        notif = Notification(uid=form.uid.data, message=form.message.data)
        db.session.add(notif)
        db.session.commit()
        flash("Notification sent Sucessfully")
        return redirect(url_for("admin.dnotif"))
    return render_template("admin/dnotif.html", form=form)


@admin.route("/user_subs", methods=["GET", "POST"])
@admin_required
def user_subs():
    form=UserSubmissions()
    if form.validate_on_submit():
        submissions = Submission.query.filter_by(by=form.uid.data).order_by(Submission.time.desc()).all()
        user = User.query.filter_by(id=form.uid.data).first() 
        return render_template("admin/user_subs.html", submissions=submissions, user=user)
    return render_template('admin/usersearch.html',form=form)

@admin.route("/all_feeds")
@admin_required
def all_feeds():
    feedbacks = Feedback.query.order_by(Feedback.id.desc()).all()
    users = User.query.all()
    return render_template("admin/all_feeds.html", feedbacks=feedbacks, users=users)
