from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from models import db, Trek, User, Staff, Booking
from datetime import datetime

staff_routes = Blueprint('staff', __name__)

@staff_routes.route('/staff/dashboard')
@login_required
def staff_dashboard():
    if current_user.role != 'staff':
        return "Access Denied", 403
    
    status = (request.args.get('status') or '').strip().lower()
    location = (request.args.get('location') or '').strip()

    assigned_treks_count = len(current_user.treks)
    total_registerred_trekkers = 0
    for trek in current_user.treks:
        trek.registered_count = sum(1 for b in trek.bookings if b.status != "cancelled")
        total_registerred_trekkers += trek.registered_count

    treks = current_user.treks
    if status:
        treks = [t for t in treks if t.status == status]
    if location:
        treks = [t for t in treks if t.location == location]

    locations = sorted({t.location for t in current_user.treks})

    return render_template('staff_dashboard.html', assigned_treks_count=assigned_treks_count,
                           total_registerred_trekkers=total_registerred_trekkers,
                           treks=treks, u_status=status, u_location=location, locations=locations)

@staff_routes.route('/staff/treks/<int:trek_id>')
@login_required
def trek_detail(trek_id):
    if current_user.role != 'staff':
        return "Access Denied", 403
    
    trek = Trek.query.filter_by(trek_id=trek_id, assigned_staff_id=current_user.staff_id).first()

    if not trek:
        return "Access Denied", 403
    
    participants = [User.query.get(booking.user_id) for booking in trek.bookings if booking.status != "cancelled"]
    return render_template('staff_trek_detail.html', trek=trek, participants=participants)

@staff_routes.route('/staff/treks/<int:trek_id>/participants/<int:user_id>/remove', methods=['POST'])
@login_required
def remove_participant(trek_id, user_id):
    if current_user.role != 'staff':
        return "Access Denied", 403

    trek = Trek.query.filter_by(trek_id=trek_id, assigned_staff_id=current_user.staff_id).first()
    if not trek:
        return "Access Denied", 403

    booking = Booking.query.filter_by(trek_id=trek_id, user_id=user_id).first()
    if booking:
        if booking.status != "cancelled":
            booking.status = "cancelled"
            trek.available_slots += 1
            db.session.commit()

    return redirect(url_for('staff.trek_detail', trek_id=trek_id))

@staff_routes.route('/staff/treks/<int:trek_id>/update', methods=['POST'])
@login_required
def update_trek(trek_id):
    if current_user.role != 'staff':
        return "Access Denied", 403

    trek = Trek.query.filter_by(trek_id=trek_id, assigned_staff_id=current_user.staff_id).first()

    if not trek:
        return "Access Denied", 403

    new_status = (request.form.get('status') or '').strip().lower()
    new_available_slots = (request.form.get('available_slots') or '').strip()

    if new_status == 'completed' and trek.status != 'completed':
        if trek.end_date > datetime.now():
            return "Cannot complete a trek before its end date", 400

        current_user.number_of_treks_completed += 1
        for booking in trek.bookings:
            if booking.status != "cancelled":
                booking.status = "completed"

    # Reopening a trek that was marked completed by mistake
    elif new_status != 'completed' and trek.status == 'completed':
        if current_user.number_of_treks_completed > 0:
            current_user.number_of_treks_completed -= 1
        for booking in trek.bookings:
            if booking.status == "completed":
                booking.status = "booked"

    if new_status in ['open', 'closed', 'completed', 'started', 'ongoing']:
        trek.status = new_status
    if new_available_slots:
        try:
            slots = int(new_available_slots)
        except ValueError:
            return "Available slots must be a whole number", 400
        if slots < 0:
            return "Available slots cannot be negative", 400
        
        trek.available_slots = slots

    db.session.commit()

    return redirect(url_for('staff.trek_detail', trek_id=trek.trek_id))

@staff_routes.route('/staff/edit/<int:staff_id>', methods=['GET', 'POST']) 
@login_required
def edit_profile(staff_id):
    if current_user.role != 'staff':
        return "Access Denied", 403

    if staff_id != current_user.staff_id:
        return "Access Denied", 403
    
    staff = current_user
    if not staff:
        return "Staff not found", 404
    
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        phone_number = (request.form.get('phone_number') or '').strip()

        if not name or not email or not phone_number:
            return "All fields are required", 400

        if not phone_number.isdigit() or len(phone_number) != 10:
            return "Phone number must be exactly 10 digits", 400

        staff.name = name
        staff.email = email
        staff.phone_number = phone_number

        db.session.commit()
        return redirect(url_for('staff.staff_dashboard'))

    data = {
        'staff_name': staff.name,
        'email': staff.email,
        'phone_number': staff.phone_number,
    }

    return render_template('staff_edit_profile.html', data=data)