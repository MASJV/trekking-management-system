from . import db
from flask_login import UserMixin

class Admin(db.Model, UserMixin):
    __tablename__ = 'admin'

    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    role = "admin"

    def get_id(self):
        return f"admin:{self.admin_id}"

