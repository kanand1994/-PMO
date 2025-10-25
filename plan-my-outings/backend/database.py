from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    year_of_birth = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    groups = db.relationship('GroupMember', backref='user', lazy=True)
    created_events = db.relationship('Event', backref='creator', lazy=True)

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    members = db.relationship('GroupMember', backref='group', lazy=True)
    events = db.relationship('Event', backref='group', lazy=True)

class GroupMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    role = db.Column(db.String(20), default='member')
    joined_at = db.Column(db.DateTime, default=datetime.utcnow)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    event_type = db.Column(db.String(50), nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='planning')
    final_decision = db.Column(db.Integer, db.ForeignKey('event_option.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_date = db.Column(db.DateTime)
    
    # Relationships
    options = db.relationship('EventOption', backref='event', lazy=True, foreign_keys='EventOption.event_id')
    polls = db.relationship('Poll', backref='event', lazy=True)

class EventOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    option_type = db.Column(db.String(50))
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    external_id = db.Column(db.String(100))
    option_metadata = db.Column(db.Text)
    
    # Relationships
    votes = db.relationship('Vote', backref='option', lazy=True)

class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    question = db.Column(db.String(300), nullable=False)
    poll_type = db.Column(db.String(20), default='multiple')

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('event_option.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    vote_value = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Enquiry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    year_of_birth = db.Column(db.Integer, nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%"
    return ''.join(random.choice(characters) for i in range(length))

def create_user_from_enquiry(enquiry_data):
    first_name = enquiry_data['first_name']
    last_name = enquiry_data['last_name']
    year_of_birth = enquiry_data['year_of_birth']
    email = enquiry_data['email']
    
    # Generate username
    username = f"{first_name.lower()}.{last_name.lower()}.{year_of_birth}"
    
    # Check if username exists, append number if needed
    counter = 1
    original_username = username
    while User.query.filter_by(username=username).first():
        username = f"{original_username}{counter}"
        counter += 1
    
    # Generate random password
    password = generate_random_password()
    
    user = User(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        year_of_birth=year_of_birth
    )
    
    return user, password
