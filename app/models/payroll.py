from app.extensions import db

class PayrollHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gross = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer, default=30)
    children = db.Column(db.Integer, default=0)
    efka = db.Column(db.Float)
    tax = db.Column(db.Float)
    bonuses = db.Column(db.Float)
    net = db.Column(db.Float)