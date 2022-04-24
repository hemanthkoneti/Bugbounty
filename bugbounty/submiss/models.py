from submiss import db, login_manager
from flask_login import UserMixin, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

start = datetime(2022,4,12)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    roll = db.Column(db.String(64), unique=True, index=True)
    roll2=db.Column(db.String(64), unique=True, index=True)
    password=db.Column(db.String(128))   
    password_hash = db.Column(db.String(128))
    notif_count = db.Column(db.Integer, default=0)
    score=db.Column(db.Integer,default=0)
    user_type = db.Column(db.String(64))
    sub_count=db.Column(db.Integer,default=1)
    upgrade_time = db.Column(db.DateTime)

    def __init__(self,roll,roll2, username, password,user_type):
        self.roll = roll
        self.roll2=roll2
        self.username = username
        self.password=password
        self.password_hash = generate_password_hash(password)
        self.user_type = user_type
        self.upgrade_time=datetime.now()
    
    def update_count(self,sub_count):
        self.sub_count=sub_count+1
        db.session.add(self)
    
    def update_score(self,score):
        self.score += score
        db.session.add(self)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"{self.id}, {self.roll}, {self.username}"


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    picture = db.Column(db.String(64), nullable=False)
    ans = db.Column(db.String, nullable=False)
    points = db.Column(db.Integer)
    correct = db.Column(db.Integer)
    review = db.Column(db.String)
    bug_id=db.Column(db.Integer,default=0)
    time = db.Column(db.DateTime, nullable=False)
    usr = db.relationship("User", backref="by", lazy=True)

    def __init__(self, ans, points,picture,correct):
        self.by = current_user.id
        self.ans = ans
        self.time = datetime.now()
        self.points = points
        self.picture = picture
        self.correct = correct

    def __repr__(self):
        return (
            f"{self.id},{self.by}, {self.time}, {self.correct}"
        )



class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    message = db.Column(db.String, nullable=False)

    def __init__(self, uid, message):
        self.uid = uid
        self.message = message

    def __repr__(self):
        return f"{self.id},{self.uid},{self.message}"


class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String, nullable=False)

    def __init__(self, message):
        self.message = message

    def __repr__(self):
        return f"{self.id}, {self.message}"
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    feed = db.Column(db.String, nullable=False)

    def __init__(self, feed):
        self.uid = current_user.id
        self.feed = feed

    def __repr__(self):
        return f"{self.uid}, {self.feed}"
