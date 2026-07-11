from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db 
from models.admin import Admin 
from models.staff import Staff
from models.user import User

auth_routes = Blueprint('auth', __name__)

@auth_routes.route("/")
def home():
    return redirect(url_for("auth.login"))

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')

        user = (Admin.query.filter_by(username=username).first() 
                or Staff.query.filter_by(email=username).first() 
                or User.query.filter_by(email=username).first()
                )

        if not user or not check_password_hash(user.password, password):
            return render_template('login_error.html')
        
        if user and check_password_hash(user.password, password):
            if hasattr(user, "is_approved") and not user.is_approved:
                return render_template('login_error.html')
            
            if hasattr(user, "is_blacklisted") and user.is_blacklisted:
                return render_template('login_error.html')
            
            if hasattr(user, "status") and user.status == "inactive":
                return render_template('login_error.html')
            
            login_user(user)

            if user.role == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            elif user.role == "staff":
                return redirect(url_for("staff.staff_dashboard"))
            elif user.role == "user":
                return redirect(url_for("user.user_dashboard"))
            
    else:
        return render_template("login.html")
    
@auth_routes.route('/register/user', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user:
            return render_template('register_error.html') # user already exists
        
        user = User(name = name, email = email, password = generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return render_template('register_success.html')
    
    else:
        return render_template('user_register.html')
    
@auth_routes.route('/register/staff', methods=['GET', 'POST'])
def register_staff():
    if request.method == 'POST':
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')
        email = request.form.get('email')
        password = request.form.get('password')

        if not phone_number or not phone_number.isdigit() or len(phone_number) != 10:
            return render_template('register_error.html')  # phone number invalid

        user = Staff.query.filter_by(email=email).first()

        if user:
            return render_template('register_error.html') # user already exists

        user = Staff(name = name, phone_number = phone_number, email = email, password = generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

        return render_template('register_success.html')
    
    else:
        return render_template('staff_register.html')
    
@auth_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))