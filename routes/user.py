from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import db 

user_routes = Blueprint('user', __name__)

@user_routes.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.role != 'user':
        return "Access Denied", 403
    
    else:
        return render_template('user_dashboard.html')