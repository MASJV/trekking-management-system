from . import db

class Booking(db.Model):
    __tablename__ = "bookings"
    
    booking_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey('treks.trek_id'), nullable=False)
    booking_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False) # 'booked', 'cancelled', or 'completed'
    
    def get_details(self):
        return {
            "booking_id": self.booking_id,
            "user_id": self.user_id,
            "trek_id": self.trek_id,
            "status": self.status,
            "booking_date": self.booking_date
        }