from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from models import db
from models.trek import Trek
from models.user import User
from models.staff import Staff
from models.booking import Booking
from datetime import datetime

admin_routes = Blueprint('admin', __name__)

@admin_routes.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return "Access Denied", 403
    
    total_treks = Trek.query.count()
    total_users = User.query.count()
    total_staff = Staff.query.count()
    total_bookings = Booking.query.count()
    
    
    return render_template('admin_dashboard.html',
                           total_treks=total_treks,
                            total_users=total_users,
                            total_staff=total_staff,
                            total_bookings=total_bookings
                            ) 


@admin_routes.route('/admin/treks')
@login_required
def manage_treks():
    if current_user.role != "admin":
        return "Access Denied", 403

    name = (request.args.get('name') or '').strip()
    difficulty = (request.args.get('difficulty') or '').strip()
    location = (request.args.get('location') or '').strip()
    status = (request.args.get('status') or '').strip()

    filters = []
    if name:
        filters.append(Trek.trek_name.ilike(f"%{name}%"))
    if difficulty:
        filters.append(Trek.difficulty == difficulty)
    if location:
        filters.append(Trek.location == location)
    if status:
        filters.append(Trek.status == status)

    treks = Trek.query.filter(*filters).all()

    locations = [row[0] for row in db.session.query(Trek.location).distinct().all()]

    return render_template('admin_treks.html', treks=treks, locations=locations,
                           u_name=name, u_difficulty=difficulty,
                           u_location=location, u_status=status)


@admin_routes.route('/admin/treks/add', methods=['GET', 'POST'])
@login_required
def add_trek():
    if current_user.role != "admin":
        return "Access Denied", 403

    if request.method == 'POST':
        trek = Trek(
            trek_name = request.form.get('trek_name'),
            location = request.form.get('location'),
            difficulty = request.form.get('difficulty'),
            duration = int(request.form.get('duration')),
            available_slots = int(request.form.get('available_slots')),
            price = float(request.form.get('price')),
            status = request.form.get('status'),
            start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d'),
            end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d')
        )
        db.session.add(trek)
        db.session.commit()

        return redirect(url_for('admin.manage_treks'))   

    return render_template('admin_add_trek.html')  

@admin_routes.route('/admin/treks/delete/<int:trek_id>', methods=['POST'])
@login_required
def delete_trek(trek_id):
    if current_user.role != "admin":
        return "Access Denied", 403
    
    trek = Trek.query.get(trek_id)
    if trek:
        db.session.delete(trek)
        db.session.commit()

    return redirect(url_for('admin.manage_treks'))


@admin_routes.route('/admin/treks/edit/<int:trek_id>', methods=['GET', 'POST'])
@login_required
def edit_trek(trek_id):
    if current_user.role != "admin":
        return "Access Denied", 403
    
    trek = Trek.query.get(trek_id)
    if not trek:                      
        return redirect(url_for('admin.manage_treks'))
    
    if request.method == 'POST':
        try:
            trek.trek_name = request.form['trek_name'].strip()
            trek.location = request.form['location'].strip()
            trek.difficulty = request.form['difficulty'].strip()
            trek.duration = int(request.form['duration'])
            trek.available_slots = int(request.form['available_slots'])
            trek.price = float(request.form['price'])
            trek.status = request.form['status'].strip()
            trek.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
            trek.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
            if trek.end_date < trek.start_date:
                raise ValueError
        except(KeyError, ValueError):
            return redirect(url_for('admin.edit_trek', trek_id=trek_id))
        
        db.session.commit()
        return redirect(url_for('admin.manage_treks'))
    
    data = {
        'trek_name': trek.trek_name, 
        'location': trek.location, 
        'difficulty': trek.difficulty,
        'duration' : trek.duration,
        'available_slots': trek.available_slots, 
        'price': trek.price, 
        'status': trek.status,
        'start_date': trek.start_date.strftime('%Y-%m-%d'),
        'end_date': trek.end_date.strftime('%Y-%m-%d')
    }
    
    return render_template('admin_edit_trek.html', data=data, trek_id=trek_id)


