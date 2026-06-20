from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db
from models.admin import Admin
from models.staff import Staff
from models.user import User
from werkzeug.security import generate_password_hash
from routes.admin import admin_routes
from routes.auth import auth_routes
from routes.user import user_routes
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "IITMProjectMay2026" # session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trekking.db' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(admin_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(user_routes)

db.init_app(app) # initialize the db with the Flask app

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    role, id = user_id.split(':')
    id = int(id)
    if role == 'admin':
        return Admin.query.get(id)
    elif role == 'staff':
        return Staff.query.get(id)
    elif role == 'user':
        return User.query.get(id)
    else:
        return None

def create_admin():
    if not Admin.query.first():
        admin = Admin(username = "admin", password = generate_password_hash("admin123*")) 
        db.session.add(admin)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)
