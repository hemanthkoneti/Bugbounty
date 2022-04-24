from flask import render_template,request, redirect, url_for, flash
from submiss import app, db
from flask_login import login_user, login_required, logout_user, current_user
from submiss.models import User, Notification, Announcement,Submission, Feedback
from submiss.forms import LoginForm, RegistrationForm,SubmissionForm,FeedbackForm
from datetime import datetime
from submiss.picture_handler import add_submission_pic

admin=[205321018]
@app.context_processor
def info():
    def score():
        if current_user.is_authenticated:
            score=current_user.score
        else:
            score="Non-Existent"
        return score
    def unread():
        count = Notification.query.filter_by(uid=current_user.id).count()
        if count != current_user.notif_count:
            notifs = count - current_user.notif_count
        else:
            notifs = 0
        return notifs
    
    return dict(
        score=score,
        unread=unread,
        time=datetime.now(),
    ) 

@app.route("/")
def index():
    return render_template("home.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.roll.data in admin:
            user = User(
                roll=form.roll.data,
                roll2=form.roll2.data,
                username=form.username.data,
                password=form.password.data,
                user_type="Admin",
            )
        else:
            user = User(
                roll=form.roll.data,
                roll2=form.roll2.data,
                username=form.username.data,
                password=form.password.data,
                user_type="Player",
            )

        db.session.add(user)
        db.session.commit()
        flash("Thank you for registering " + form.username.data + ".Remeber this username(it is case sensitive).")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.teamname.data).first()
        if user:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get("next")
                if next == None or not not next[0] == "/":
                    next = url_for("index")
                flash("Login Successful")
                return redirect(next)

            else:
                flash("Password is incorrect.")

        else:
            flash("Given team name does not exist.")
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/leaderboard")
def leaderboard():
    if current_user.is_anonymous:
        return render_template("lead_wait.html")
    # elif current_user.user_type != "Admin":
    #     return render_template("lead_wait.html")
    users = (
        User.query.filter_by(user_type="Player")
        .order_by(User.score.desc(),User.upgrade_time.asc())
        .all()
    )
    return render_template("leaderboard.html", users=users)


@app.route("/announcements")
@login_required
def announcements():
    ancmts = Announcement.query.all()
    ancmts.reverse()
    return render_template("announcements.html", ancmts=ancmts)

@app.route("/notifications")
@login_required
def notifications():
    notifs = Notification.query.filter_by(uid=current_user.id).all()
    notifs.reverse()
    count = Notification.query.filter_by(uid=current_user.id).count()
    current_user.notif_count = count
    db.session.commit()
    return render_template("notifications.html", notifs=notifs)

@app.route("/submissions", methods=["GET", "POST"])
@login_required
def submissions():
    form = SubmissionForm()
    if form.validate_on_submit():
        if form.picture.data:
            username=current_user.username
            attempt=current_user.sub_count
            pic=add_submission_pic(form.picture.data, username, attempt)
            
        submiss=Submission(
            ans=form.ans.data,
            points=0,
            picture=pic,
            correct=1,
        )
        current_user.update_count(current_user.sub_count)
        db.session.add(submiss)
        db.session.commit()
        flash("Submission has been sucessfull.")
        return redirect(url_for("submissions"))
    return render_template("submission.html",form=form)

@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        back = Feedback(feed=form.feed.data)
        db.session.add(back)
        db.session.commit()
        flash("Thank you for your valuable feedback.")
        return redirect(url_for("index"))

    return render_template("feedback.html", form=form)

@app.route("/instructions")
def instructions():
    return render_template("instructions.html")