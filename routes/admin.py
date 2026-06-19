from flask import Blueprint, render_template, redirect, url_for;
from flask_login import login_required, current_user
from models import db

admin_routes = Blueprint('admin', __name__)

@admin_routes.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return "Access Denied", 403
    
    else:
        return render_template('admin_dashboard.html') 