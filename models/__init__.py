from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .admin import Admin
from .booking import Booking 
from .staff import Staff 
from .user import User
from .trek import Trek