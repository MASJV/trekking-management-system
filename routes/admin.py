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

    trek_id = (request.args.get('trek_id') or '').strip()
    name = (request.args.get('name') or '').strip()
    difficulty = (request.args.get('difficulty') or '').strip()
    location = (request.args.get('location') or '').strip()
    status = (request.args.get('status') or '').strip()

    filters = []
    if trek_id.isdigit():
        filters.append(Trek.trek_id == int(trek_id))
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
    assignable_staff = Staff.query.filter_by(is_approved=True, status='active').all()


    return render_template('admin_treks.html', treks=treks, locations=locations,
                           u_trek_id=trek_id, u_name=name, u_difficulty=difficulty,
                           u_location=location, u_status=status, assignable_staff=assignable_staff)


@admin_routes.route('/admin/treks/add', methods=['GET', 'POST'])
@login_required
def add_trek():
    if current_user.role != "admin":
        return "Access Denied", 403

    if request.method == 'POST':
        try:
            trek = Trek(
                trek_name=request.form['trek_name'].strip(),
                location=request.form['location'].strip(),
                difficulty=request.form['difficulty'].strip(),
                duration=int(request.form['duration']),
                available_slots=int(request.form['available_slots']),
                price=float(request.form['price']),
                status=request.form['status'].strip(),
                start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d'),
                end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d'),
            )
            if trek.end_date < trek.start_date:
                raise ValueError
                
        except(KeyError, ValueError):
            return redirect(url_for('admin.add_trek'))
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

@admin_routes.route('/admin/users')
@login_required
def manage_users():
    if current_user.role != "admin":
        return "Access Denied", 403

    user_id = (request.args.get('user_id') or '').strip()
    name = (request.args.get('name') or '').strip()
    is_blacklisted = (request.args.get('is_blacklisted') or '').strip()

    filters = []
    if user_id.isdigit():
        filters.append(User.user_id == int(user_id))
    if name:
        filters.append(User.name.ilike(f"%{name}%"))
    if is_blacklisted == 'True':
        filters.append(User.is_blacklisted.is_(True))
    elif is_blacklisted == 'False':
        filters.append(User.is_blacklisted.is_(False))

    users = User.query.filter(*filters).all()

    return render_template('admin_users.html', users=users, u_user_id=user_id,
                           u_name=name, u_isblacklisted=is_blacklisted)

@admin_routes.route('/admin/users/blacklist/<int:user_id>', methods=['POST'])
@login_required
def blacklist_user(user_id):
    if current_user.role != 'admin':
        return "Access Denied", 403

    user = User.query.get(user_id)

    if user:
        user.is_blacklisted = True
        db.session.commit()

    return redirect(url_for('admin.manage_users'))

@admin_routes.route('/admin/users/unblacklist/<int:user_id>', methods=['POST']) 
@login_required
def unblacklist_user(user_id):
    if current_user.role != 'admin':
        return "Access Denied", 403

    user = User.query.get(user_id)

    if user:
        user.is_blacklisted = False
        db.session.commit()

    return redirect(url_for('admin.manage_users'))

@admin_routes.route('/admin/staff')
@login_required
def manage_staff():
    if current_user.role != 'admin':
        return "Access Denied", 403
    
    staff_id = (request.args.get('staff_id') or '').strip()
    name = (request.args.get('name') or '').strip()
    status = (request.args.get('status') or '').strip()

    filters = []
    if staff_id.isdigit():
        filters.append(Staff.staff_id == int(staff_id))
    if name:
        filters.append(Staff.name.ilike(f"%{name}%"))

    if status:
        filters.append(Staff.status == status.lower())
    
    filters.append(Staff.is_approved.is_(True))  # Only shows approved staff

    staffs = Staff.query.filter(*filters).all()

    for s in staffs:
        s.trek_ids = ""
        for t in s.treks:
            if s.trek_ids == "": 
                s.trek_ids = str(t.trek_id)
            else:
                s.trek_ids = s.trek_ids + ", " + str(t.trek_id) 

        if s.trek_ids == "":
            s.trek_ids = "None"

    return render_template('admin_staffs.html', staffs=staffs, u_staff_id=staff_id,
                           u_name=name, u_status=status)

@admin_routes.route('/admin/staff/unapprove/<int:staff_id>', methods=['POST'])
@login_required
def unapprove_staff(staff_id):
    if current_user.role != "admin":
        return "Access Denied", 403

    staff = Staff.query.get(staff_id)
    if staff:
        staff.is_approved = False
        for trek in staff.treks:
            trek.assigned_staff_id = None  # unassign treks allotted to staff
        db.session.commit()

    return redirect(url_for('admin.manage_staff'))

@admin_routes.route('/admin/staff/approve/<int:staff_id>', methods=['POST'])
@login_required
def approve_staff(staff_id):
    if current_user.role != "admin":
        return "Access Denied", 403

    staff = Staff.query.get(staff_id)
    if staff:
        staff.is_approved = True
        db.session.commit()

    return redirect(url_for('admin.manage_staff'))

@admin_routes.route('/admin/staff/delete/<int:staff_id>', methods=['POST'])
@login_required
def delete_staff(staff_id):
    if current_user.role != "admin":
        return "Access Denied", 403

    staff = Staff.query.get(staff_id)
    if staff:
        for trek in staff.treks:
            trek.assigned_staff_id = None  

        db.session.delete(staff)
        db.session.commit()

    return redirect(url_for('admin.manage_staff'))

@admin_routes.route('/admin/staff/unapproved')
@login_required
def unapproved_staff():
    if current_user.role != "admin":
        return "Access Denied", 403

    unapproved_staffs = Staff.query.filter_by(is_approved=False).all()

    return render_template('admin_unapproved_staffs.html', staffs=unapproved_staffs)

@admin_routes.route('/admin/treks/assign_staff/<int:trek_id>', methods=['POST'])
@login_required
def assign_staff(trek_id):
    if current_user.role != "admin":
        return "Access Denied", 403
    
    trek = Trek.query.get(trek_id)
    if not trek:
        return redirect(url_for('admin.manage_treks'))
    
    staff_id = request.form.get('staff_id')
    if not staff_id:
        trek.assigned_staff_id = None
    else:
        staff = Staff.query.get(staff_id) # no error as staff id exists!?
    
        if staff and staff.is_approved and staff.status == 'active':
            trek.assigned_staff_id = staff.staff_id
        
    db.session.commit()
    return redirect(url_for('admin.manage_treks'))

@admin_routes.route('/admin/bookings')
@login_required
def manage_bookings():
    if current_user.role != "admin":
        return "Access Denied", 403

    user_id = (request.args.get('user_id') or '').strip()
    trek_id = (request.args.get('trek_id') or '').strip()
    status = (request.args.get('status') or '').strip()

    filters = []
    if user_id.isdigit():
        filters.append(Booking.user_id == int(user_id))
    if trek_id.isdigit():
        filters.append(Booking.trek_id == int(trek_id))
    if status:
        filters.append(Booking.status == status)

    bookings = Booking.query.filter(*filters).order_by(Booking.booking_date.desc()).all()

    return render_template('admin_bookings.html', bookings=bookings,
                           u_user_id=user_id, u_trek_id=trek_id, u_status=status)

@admin_routes.route('/admin/bookings/payment/<int:booking_id>', methods=['POST'])
@login_required
def toggle_payment(booking_id):
    if current_user.role != "admin":
        return "Access Denied", 403

    booking = Booking.query.get(booking_id)
    if booking:
        booking.payment_status = 'paid' if booking.payment_status != 'paid' else 'pending'
        db.session.commit()

    return redirect(url_for('admin.manage_bookings'))