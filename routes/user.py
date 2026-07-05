from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from models import db 
from models.user import User
from models.trek import Trek
from models.booking import Booking


user_routes = Blueprint('user', __name__)

@user_routes.route('/user/dashboard')
@login_required
def user_dashboard():
    if current_user.role != 'user':
        return "Access Denied", 403 # need to add redirect to login page?

    difficulty = (request.args.get('difficulty') or '').strip().lower()
    location = (request.args.get('location') or '').strip()

    filters = []
    if difficulty:
        filters.append(Trek.difficulty == difficulty)
    if location:
        filters.append(Trek.location == location)

    booked_treks = [Trek.query.get(booking.trek_id) for booking in current_user.bookings if booking.status != "cancelled"]
    treks = Trek.query.filter(Trek.status == 'open').filter(*filters).all()
    treks = [trek for trek in treks if trek not in booked_treks]

    locations = [row[0] for row in db.session.query(Trek.location).distinct().all()]
    return render_template('user_dashboard.html', treks=treks, locations=locations,
                           u_difficulty=difficulty, u_location=location)
    
@user_routes.route('/user/treks') # trekking history
@login_required
def user_treks():
    if current_user.role != 'user':
        return "Access Denied", 403

    booked_trek_ids = [booking.trek_id for booking in current_user.bookings if booking.status == "completed"]
    treks = Trek.query.filter(Trek.trek_id.in_(booked_trek_ids), Trek.status == 'completed').all()
    
    return render_template('user_treks.html', treks=treks)
    
@user_routes.route('/user/treks/<int:trek_id>')
@login_required
def trek_detail(trek_id):
    if current_user.role != 'user':
        return "Access Denied", 403
    
    trek = Trek.query.filter_by(trek_id=trek_id).first()

    if not trek:
        return "Access Denied", 403
    
    return render_template('user_trek_detail.html', trek=trek)

@user_routes.route('/user/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.role != 'user':
        return "Access Denied", 403

    if request.method == 'POST':
        new_name = (request.form.get('name') or '').strip()
        new_email = (request.form.get('email') or '').strip()

        if not new_name or not new_email:
            return "Name and email are required", 400

        current_user.name = new_name
        current_user.email = new_email
        db.session.commit()
        return redirect(url_for('user.user_dashboard'))

    data = {
        'name': current_user.name,
        'email': current_user.email,
    }
    return render_template('user_edit_profile.html', data=data)

@user_routes.route('/user/treks/<int:trek_id>/book', methods=['POST'])
@login_required
def book_trek(trek_id):
    if current_user.role != 'user':
        return "Access Denied", 403

    trek = Trek.query.filter_by(trek_id=trek_id).first()
    if not trek or trek.status != 'open':
        return "Trek not available for booking", 400

    if trek.available_slots is None or trek.available_slots < 1:
        return "No slots available for this trek", 400
    
    booking = Booking.query.filter_by(user_id=current_user.user_id, trek_id=trek_id).first()
    if booking:
        if booking.status in ["booked", "completed"]:
            return "You have already booked this trek", 400
        
        else:
            booking.status = "booked"
            trek.available_slots -= 1
            db.session.commit()
            return redirect(url_for('user.booked_treks', trek_id=trek_id))


    booking = Booking(
        user_id=current_user.user_id,
        trek_id=trek.trek_id,
        booking_date=db.func.now(),
        status='booked'
    )
    trek.available_slots -= 1
    db.session.add(trek)
    db.session.add(booking)
    db.session.commit()

    return redirect(url_for('user.booked_treks', trek_id=trek_id))
    
@user_routes.route('/user/booked_treks') # check out first
@login_required
def booked_treks():
    if current_user.role != 'user':
        return "Access Denied", 403

    booked_treks = [Trek.query.get(booking.trek_id) for booking in current_user.bookings if booking.status != "cancelled"]

    return render_template('user_booked_treks.html', treks=booked_treks)

@user_routes.route('/user/booked_treks/<int:trek_id>/cancel', methods=['POST'])
@login_required
def cancel_booking(trek_id):
    if current_user.role != 'user':
        return "Access Denied", 403

    booking = Booking.query.filter_by(user_id=current_user.user_id, trek_id=trek_id).first()
    if not booking:
        return "Booking not found", 404

    if(booking.status != "cancelled"):
        booking.status = "cancelled"

        trek = Trek.query.filter_by(trek_id=trek_id).first()
        if not trek:
            return "Trek not found", 404

        trek.available_slots += 1
        db.session.add(trek)
        db.session.commit()

    return redirect(url_for('user.booked_treks'))