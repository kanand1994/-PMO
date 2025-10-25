from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from database import db, User, Group, Event, Enquiry, Poll, EventOption, Vote, GroupMember, create_user_from_enquiry
from auth import token_required, generate_token
from api_services import GooglePlacesService, TMDBService, OpenWeatherService
from socket_events import socketio
from config import Config
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app, resources={
    r"/api/*": {"origins": "*"},
    r"/contact": {"origins": "*"},
    r"/login": {"origins": "*"},
    r"/groups": {"origins": "*"},
    r"/events": {"origins": "*"}
})
socketio.init_app(app)
mail = Mail(app)

@app.route('/')
def home():
    return jsonify({"message": "Plan My Outings API"})

# Handle direct /contact requests (redirect to /api/contact)
@app.route('/contact', methods=['POST', 'OPTIONS'])
def contact_redirect():
    if request.method == 'OPTIONS':
        # Handle CORS preflight
        response = jsonify({'message': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    else:
        # Redirect POST to the correct endpoint
        return contact_enquiry()

# Handle direct /login requests (redirect to /api/login)
@app.route('/login', methods=['POST', 'OPTIONS'])
def login_redirect():
    if request.method == 'OPTIONS':
        # Handle CORS preflight
        response = jsonify({'message': 'OK'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    else:
        # Redirect POST to the correct endpoint
        return login()

# Handle direct /groups requests (redirect to /api/groups)
@app.route('/groups', methods=['OPTIONS'])
def groups_options():
    # Handle CORS preflight
    response = jsonify({'message': 'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/groups', methods=['GET', 'POST'])
@token_required
def groups_redirect(current_user):
    if request.method == 'GET':
        # Get groups for current user
        groups = Group.query.filter(Group.members.any(user_id=current_user.id)).all()
        return jsonify([{
            'id': group.id,
            'name': group.name,
            'description': group.description,
            'member_count': len(group.members)
        } for group in groups])
    else:  # POST
        # Create group for current user
        data = request.get_json()
        group = Group(
            name=data['name'],
            description=data.get('description', ''),
            created_by=current_user.id
        )
        db.session.add(group)
        db.session.commit()
        
        # Add creator as group member
        member = GroupMember(
            group_id=group.id,
            user_id=current_user.id,
            role='admin'
        )
        db.session.add(member)
        db.session.commit()
        
        return jsonify({'message': 'Group created successfully', 'group_id': group.id})

# Handle direct /events requests (redirect to /api/events)
@app.route('/events', methods=['OPTIONS'])
def events_options():
    # Handle CORS preflight
    response = jsonify({'message': 'OK'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/events', methods=['POST'])
@token_required
def events_redirect(current_user):
    # Create event for current user
    data = request.get_json()
    event = Event(
        title=data['title'],
        description=data.get('description', ''),
        event_type=data['event_type'],
        group_id=data['group_id'],
        created_by=current_user.id
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully', 'event_id': event.id})

# Authentication routes
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user = User.query.filter_by(username=username, password=password).first()
    
    if user:
        token = generate_token(user)
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })
    
    return jsonify({'message': 'Invalid credentials!'}), 401

# Enquiry and auto-user creation
@app.route('/api/contact', methods=['POST'])
def contact_enquiry():
    try:
        data = request.get_json()
        
        # Check if user with this email already exists
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({
                'message': 'An account with this email already exists. Please use the login page.',
                'error': 'duplicate_email'
            }), 400
        
        # Create enquiry
        enquiry = Enquiry(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            year_of_birth=data['year_of_birth'],
            message=data.get('message', '')
        )
        db.session.add(enquiry)
        db.session.commit()
        
        # Create user automatically
        user, password = create_user_from_enquiry(data)
        db.session.add(user)
        db.session.commit()
        
        # Send email with credentials and admin notification
        if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
            try:
                # Send credentials to user
                user_msg = Message(
                    subject='Welcome to Plan My Outings - Your Account Details',
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[user.email]
                )
                user_msg.body = f"""
Hello {user.first_name},

Welcome to Plan My Outings! Your account has been created successfully.

Your Login Details:
Username: {user.username}
Password: {password}

You can now login at: http://localhost:3000/login

Start planning amazing outings with your friends!

Best regards,
Plan My Outings Team
                """
                mail.send(user_msg)
                
                # Send notification to admin
                admin_msg = Message(
                    subject='New User Registration - Plan My Outings',
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[app.config['SUPER_ADMIN_EMAIL'] or app.config['MAIL_USERNAME']]
                )
                admin_msg.body = f"""
New User Registration Alert

User Details:
- Name: {user.first_name} {user.last_name}
- Email: {user.email}
- Username: {user.username}
- Year of Birth: {user.year_of_birth}
- Registration Time: {user.created_at}
- Message: {enquiry.message or 'No message provided'}

Total Users: {User.query.count()}

Admin Dashboard: http://localhost:3000/admin
                """
                mail.send(admin_msg)
                
            except Exception as e:
                # Log error silently, don't show to user
                import logging
                logging.error(f"Email sending failed: {str(e)}")
                # Continue without showing error to user
        
        return jsonify({
            'message': 'Enquiry submitted!',
            'credentials': {
                'username': user.username,
                'password': password
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

# Group management
@app.route('/api/groups', methods=['GET'])
@token_required
def get_groups(current_user):
    groups = Group.query.filter(Group.members.any(user_id=current_user.id)).all()
    return jsonify([{
        'id': group.id,
        'name': group.name,
        'description': group.description,
        'member_count': len(group.members)
    } for group in groups])

@app.route('/api/groups', methods=['POST'])
@token_required
def create_group(current_user):
    data = request.get_json()
    group = Group(
        name=data['name'],
        description=data.get('description', ''),
        created_by=current_user.id
    )
    db.session.add(group)
    db.session.commit()
    
    # Add creator as group member
    member = GroupMember(
        group_id=group.id,
        user_id=current_user.id,
        role='admin'
    )
    db.session.add(member)
    db.session.commit()
    
    return jsonify({'message': 'Group created successfully', 'group_id': group.id})

# Event management
@app.route('/api/events', methods=['POST'])
@token_required
def create_event(current_user):
    data = request.get_json()
    event = Event(
        title=data['title'],
        description=data.get('description', ''),
        event_type=data['event_type'],
        group_id=data['group_id'],
        created_by=current_user.id
    )
    db.session.add(event)
    db.session.commit()
    return jsonify({'message': 'Event created successfully', 'event_id': event.id})

# API integrations
@app.route('/api/places/search', methods=['GET'])
@token_required
def search_places(current_user):
    query = request.args.get('query')
    location = request.args.get('location')
    places = GooglePlacesService.search_places(query, location)
    return jsonify(places)

@app.route('/api/movies/search', methods=['GET'])
@token_required
def search_movies(current_user):
    query = request.args.get('query')
    movies = TMDBService.search_movies(query)
    return jsonify(movies)

@app.route('/api/weather/forecast', methods=['GET'])
@token_required
def get_weather(current_user):
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    weather = OpenWeatherService.get_weather_forecast(lat, lon)
    return jsonify(weather)

# Poll and voting
@app.route('/api/polls/<int:poll_id>/vote', methods=['POST'])
@token_required
def cast_vote(current_user, poll_id):
    data = request.get_json()
    option_id = data.get('option_id')
    
    # Check if user already voted (for single choice polls)
    existing_vote = Vote.query.filter_by(poll_id=poll_id, user_id=current_user.id).first()
    if existing_vote:
        return jsonify({'message': 'You have already voted!'}), 400
    
    vote = Vote(poll_id=poll_id, option_id=option_id, user_id=current_user.id)
    db.session.add(vote)
    db.session.commit()
    
    return jsonify({'message': 'Vote cast successfully!'})

# Admin-only endpoints
@app.route('/api/admin/stats', methods=['GET'])
@token_required
def get_admin_stats(current_user):
    # Check if user is super admin
    if current_user.username != 'superadmin':
        return jsonify({'message': 'Admin access required!'}), 403
    
    try:
        # Get system statistics
        total_users = User.query.count()
        total_groups = Group.query.count()
        total_events = Event.query.count()
        total_enquiries = Enquiry.query.count()
        
        # Get recent activity (last 7 days)
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_users = User.query.filter(User.created_at >= week_ago).count()
        recent_groups = Group.query.filter(Group.created_at >= week_ago).count()
        recent_events = Event.query.filter(Event.created_at >= week_ago).count()
        recent_enquiries = Enquiry.query.filter(Enquiry.created_at >= week_ago).count()
        
        return jsonify({
            'totals': {
                'users': total_users,
                'groups': total_groups,
                'events': total_events,
                'enquiries': total_enquiries
            },
            'recent': {
                'users': recent_users,
                'groups': recent_groups,
                'events': recent_events,
                'enquiries': recent_enquiries
            }
        })
        
    except Exception as e:
        return jsonify({'message': f'Error fetching stats: {str(e)}'}), 500

@app.route('/api/admin/recent-users', methods=['GET'])
@token_required
def get_recent_users(current_user):
    # Check if user is super admin
    if current_user.username != 'superadmin':
        return jsonify({'message': 'Admin access required!'}), 403
    
    try:
        # Get 10 most recent users
        recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
        
        users_data = []
        for user in recent_users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'name': f"{user.first_name} {user.last_name}",
                'email': user.email,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M'),
                'groups_count': len(user.groups),
                'events_count': Event.query.filter_by(created_by=user.id).count()
            })
        
        return jsonify(users_data)
        
    except Exception as e:
        return jsonify({'message': f'Error fetching recent users: {str(e)}'}), 500

@app.route('/api/admin/system-activity', methods=['GET'])
@token_required
def get_system_activity(current_user):
    # Check if user is super admin
    if current_user.username != 'superadmin':
        return jsonify({'message': 'Admin access required!'}), 403
    
    try:
        # Get recent activity across the system
        recent_groups = Group.query.order_by(Group.created_at.desc()).limit(5).all()
        recent_events = Event.query.order_by(Event.created_at.desc()).limit(5).all()
        recent_enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).limit(5).all()
        
        activity_data = {
            'recent_groups': [{
                'id': group.id,
                'name': group.name,
                'creator': User.query.get(group.created_by).username if User.query.get(group.created_by) else 'Unknown',
                'members': len(group.members),
                'created_at': group.created_at.strftime('%Y-%m-%d %H:%M')
            } for group in recent_groups],
            
            'recent_events': [{
                'id': event.id,
                'title': event.title,
                'type': event.event_type,
                'creator': User.query.get(event.created_by).username if User.query.get(event.created_by) else 'Unknown',
                'group': Group.query.get(event.group_id).name if Group.query.get(event.group_id) else 'Unknown',
                'created_at': event.created_at.strftime('%Y-%m-%d %H:%M')
            } for event in recent_events],
            
            'recent_enquiries': [{
                'id': enquiry.id,
                'name': f"{enquiry.first_name} {enquiry.last_name}",
                'email': enquiry.email,
                'message': enquiry.message[:100] + '...' if len(enquiry.message or '') > 100 else enquiry.message or '',
                'created_at': enquiry.created_at.strftime('%Y-%m-%d %H:%M')
            } for enquiry in recent_enquiries]
        }
        
        return jsonify(activity_data)
        
    except Exception as e:
        return jsonify({'message': f'Error fetching system activity: {str(e)}'}), 500

def create_super_admin():
    """Create super admin account if it doesn't exist"""
    try:
        # Check if super admin already exists
        super_admin = User.query.filter_by(username=app.config['SUPER_ADMIN_USERNAME']).first()
        
        if not super_admin and app.config['SUPER_ADMIN_USERNAME']:
            super_admin = User(
                username=app.config['SUPER_ADMIN_USERNAME'],
                password=app.config['SUPER_ADMIN_PASSWORD'],
                email=app.config['SUPER_ADMIN_EMAIL'],
                first_name=app.config['SUPER_ADMIN_FIRST_NAME'],
                last_name=app.config['SUPER_ADMIN_LAST_NAME'],
                year_of_birth=1990  # Default year
            )
            db.session.add(super_admin)
            db.session.commit()
            print(f"✅ Super admin created: {app.config['SUPER_ADMIN_USERNAME']}")
            
            # Send welcome email to super admin
            if app.config['MAIL_USERNAME'] and app.config['MAIL_PASSWORD']:
                try:
                    msg = Message(
                        subject='Plan My Outings - Super Admin Account Created',
                        sender=app.config['MAIL_USERNAME'],
                        recipients=[app.config['SUPER_ADMIN_EMAIL']]
                    )
                    msg.body = f"""
Super Admin Account Setup Complete

Your super admin credentials:
Username: {app.config['SUPER_ADMIN_USERNAME']}
Password: {app.config['SUPER_ADMIN_PASSWORD']}

Admin Access:
- Web Dashboard: http://localhost:3000/admin
- CLI Database Access: python cli_admin.py
- API Access: All endpoints with admin privileges

Keep these credentials secure!

Plan My Outings System
                    """
                    mail.send(msg)
                    print("✅ Super admin welcome email sent")
                except Exception as e:
                    print(f"⚠️ Could not send super admin email: {e}")
        else:
            print(f"ℹ️ Super admin already exists: {app.config['SUPER_ADMIN_USERNAME']}")
            
    except Exception as e:
        print(f"❌ Error creating super admin: {e}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_super_admin()
    socketio.run(app, debug=True, port=5000)
