from . import db
from flask_login import UserMixin

class Staff(db.Model, UserMixin):
    __tablename__ = "staff"
    
    staff_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='active') # 'active' or 'inactive'
    number_of_treks_completed = db.Column(db.Integer, nullable=False, default=0)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_approved = db.Column(db.Boolean, nullable=False, default=False)
    
    role = "staff"

    def get_id(self):
        return f"staff:{self.staff_id}"
    
    def get_details(self):
        return {
            "staff_id": self.staff_id,
            "role": self.role,
            "name": self.name,
            "number_of_treks_completed": self.number_of_treks_completed,
            "phone_number": self.phone_number,
            "status": self.status,
            "track_assigned_count": len(self.treks)
        }

    treks = db.relationship('Trek', backref='staff', lazy=True)