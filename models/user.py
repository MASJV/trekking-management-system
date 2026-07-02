from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(100), unique=True, nullable=False)
    ## ADD PHONE NUMBER RIGHT
    password = db.Column(db.String(255), nullable=False)
    is_blacklisted = db.Column(db.Boolean, default=False)

    role = "user"


    def get_id(self):
        return f"user:{self.user_id}"
    
    def get_details(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "is_blacklisted": self.is_blacklisted
    }

    bookings = db.relationship('Booking', backref='user', lazy=True)