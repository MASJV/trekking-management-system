from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from models.admin import Admin
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "IITMProjectMay2026" # used for session management and CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db' # using SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app) # initialize the db with the Flask app

def create_admin():
    if not Admin.query.first():
        admin = Admin(username = "admin", password = generate_password_hash("admin123")) 
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)
