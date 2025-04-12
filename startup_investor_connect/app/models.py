from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'startup' or 'investor'

    # Relationships for messages
    messages_sent = db.relationship('Message', foreign_keys='Message.sender_id', backref='sender', lazy='dynamic')
    messages_received = db.relationship('Message', foreign_keys='Message.receiver_id', backref='receiver', lazy='dynamic')

class Startup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    funding_received = db.Column(db.Float, nullable=False)
    looking_for_investors = db.Column(db.Boolean, default=False)
    cover_image = db.Column(db.String(255), nullable=True)
    website_url = db.Column(db.String(255), nullable=True)
    founder_details = db.Column(db.Text, nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    funding_required = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'Individual' or 'Company'
    investment_portfolio = db.Column(db.Text, nullable=True)
    total_funding_given = db.Column(db.Float, nullable=False)
    industry = db.Column(db.String(50), nullable=False)
    funding_range_min = db.Column(db.Float, nullable=False)
    funding_range_max = db.Column(db.Float, nullable=False)
    cover_image = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())