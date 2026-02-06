from .extensions import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="Calculation")
    gross_salary = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, default=26)
    children = db.Column(db.Integer, default=0)
    tax = db.Column(db.Float)
    net = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)