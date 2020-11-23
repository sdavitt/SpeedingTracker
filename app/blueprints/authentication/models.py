from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    display = db.Column(db.String)
    password = db.Column(db.String)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    taken = db.Column(db.Integer, default=0)
    inhand = db.Column(db.Integer, default=0)
    owed = db.Column(db.Integer, default=0)
    team = db.Column(db.Integer, default=0)

    def hash_password(self, original_password):
        self.password = generate_password_hash(original_password)

    def check_password(self, original_password):
        return check_password_hash(self.password, original_password)

    def __repr__(self):
        return f"<User: {self.username}>"

@login.user_loader
def login_user(id):
    return User.query.get(int(id))