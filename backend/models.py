from extensions import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(256), nullable=False)
    alerts = db.relationship('Alert', backref='user', lazy=True)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_symbol = db.Column(db.String(30), nullable=False)
    price_threshold = db.Column(db.Float, nullable=False)
    alert_type = db.Column(db.String(10), nullable=False)  # "above" or "below"
    enabled = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
