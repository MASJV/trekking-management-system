from . import db

class Trek(db.Model):
    __tablename__ = "treks"
    
    trek_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trek_name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False) # easy, moderate, hard
    duration = db.Column(db.Integer, nullable=False)  
    available_slots = db.Column(db.Integer, nullable=False)
    assigned_staff_id = db.Column(db.Integer, db.ForeignKey('staff.staff_id'), nullable=True)
    status = db.Column(db.String(20), nullable=False) # pending, approved, open, closed, completed
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False) 
    price = db.Column(db.Float, nullable=False)  

    def get_details(self):
        return {
            "trek_id": self.trek_id,
            "trek_name": self.trek_name,
            "location": self.location,
            "duration": self.duration,
            "available_slots": self.available_slots,
            "assigned_staff_id": self.assigned_staff_id,
            "difficulty": self.difficulty,
            "price": self.price,
            "status": self.status
        }

    bookings = db.relationship('Booking', backref = 'trek', lazy = True)