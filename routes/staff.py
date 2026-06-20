from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import db 

staff_routes = Blueprint('staff', __name__)

@staff_routes.route('/staff/dashboard')
@login_required
def staff_dashboard():
    if current_user.role != 'staff':
        return "Access Denied", 403
    
    else:
        return render_template('staff_dashboard.html')