from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from database import db, User, Group, Event, Enquiry, Poll, EventOption, Vote, GroupMember, create_user_from_enquiry
from auth import token_required, generate_token
from api_services import GooglePlacesService, TMDBService, OpenWeatherService
from socket_events import socketio
from config import Config
from email_tracking import EmailLog, EmailTracker
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
CORS(app, resources={
    r"/api/*": {"origins": ["http://localhost:3000"]},
    r"/contact": {"origins": ["http://localhost:3000"]},
    r"/login": {"origins": ["http://localhost:3000"]},
    r"/groups": {"origins": ["http://localhost:3000"]},
    r"/events": {"origins": ["http://localhost:3000"]}
})
socketio.init_app(app)
mail = Mail(app)

# Home route is now handled by serve_frontend function

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
            # Send credentials to user
            user_subject = '🎉 Welcome to Plan My Outings - Account Created!'
            try:
                user_msg = Message(
                    subject=user_subject,
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[user.email]
                )
                user_msg.body = f"""
🎉 Welcome to Plan My Outings, {user.first_name}!
============================================

Congratulations! Your account has been created successfully.

👤 YOUR ACCOUNT DETAILS
------------------------
Name: {user.first_name} {user.last_name}
Email: {user.email}
Username: {user.username}
Password: {password}

🚀 GET STARTED
--------------
1. Login to your account: http://localhost:3000/login
2. Create or join groups with friends
3. Plan amazing outings together
4. Vote on activities and locations

🔐 SECURITY TIPS
----------------
• Keep your login credentials safe
• Don't share your password with others
• You can change your password after logging in

📱 FEATURES AVAILABLE
--------------------
✅ Create and manage groups
✅ Plan events and outings
✅ Vote on activities
✅ Get weather forecasts
✅ Find places and restaurants
✅ Invite friends to join

🆘 NEED HELP?
-------------
If you have any questions or need assistance:
• Visit our help section in the app
• Contact support through the app

Thank you for joining Plan My Outings!
Start creating memorable experiences with your friends today.

Best regards,
The Plan My Outings Team

---
This email was sent to {user.email}
If you didn't create this account, please ignore this email.
                """
                mail.send(user_msg)
                # Log successful email
                EmailTracker.log_email_sent(user.email, user_subject, 'welcome', user.id)
                
            except Exception as e:
                # Log failed email
                EmailTracker.log_email_failed(user.email, user_subject, 'welcome', str(e), user.id)
                import logging
                logging.error(f"User email sending failed: {str(e)}")
            
            # Send notification to admin
            admin_subject = 'New User Registration - Plan My Outings'
            try:
                admin_msg = Message(
                    subject=admin_subject,
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
                # Log successful admin email
                EmailTracker.log_email_sent(app.config['SUPER_ADMIN_EMAIL'], admin_subject, 'admin_notification')
                
            except Exception as e:
                # Log failed admin email
                EmailTracker.log_email_failed(app.config['SUPER_ADMIN_EMAIL'], admin_subject, 'admin_notification', str(e))
                import logging
                logging.error(f"Admin email sending failed: {str(e)}")
        
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

# Email tracking endpoints
@app.route('/api/admin/email-logs', methods=['GET'])
@token_required
def get_email_logs(current_user):
    # Check if user is super admin
    if current_user.username != Config.SUPER_ADMIN_USERNAME:
        return jsonify({'message': 'Admin access required!'}), 403
    
    try:
        # Get recent email logs
        recent_emails = EmailTracker.get_recent_emails(50)
        email_stats = EmailTracker.get_email_stats()
        
        email_data = {
            'stats': email_stats,
            'recent_emails': [{
                'id': email.id,
                'recipient': email.recipient_email,
                'subject': email.subject,
                'type': email.email_type,
                'status': email.status,
                'error': email.error_message,
                'sent_at': email.sent_at.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': email.user_id
            } for email in recent_emails]
        }
        
        return jsonify(email_data)
        
    except Exception as e:
        return jsonify({'message': f'Error fetching email logs: {str(e)}'}), 500

@app.route('/api/admin/clear-demo-data', methods=['POST'])
@token_required
def clear_demo_data(current_user):
    # Check if user is super admin
    if current_user.username != Config.SUPER_ADMIN_USERNAME:
        return jsonify({'message': 'Admin access required!'}), 403
    
    try:
        # Clear demo data (keep super admin)
        deleted_counts = {}
        
        # Delete email logs
        deleted_counts['email_logs'] = EmailLog.query.delete()
        
        # Delete votes
        deleted_counts['votes'] = Vote.query.delete()
        
        # Delete event options
        deleted_counts['event_options'] = EventOption.query.delete()
        
        # Delete polls
        deleted_counts['polls'] = Poll.query.delete()
        
        # Delete group members
        deleted_counts['group_members'] = GroupMember.query.delete()
        
        # Delete events
        deleted_counts['events'] = Event.query.delete()
        
        # Delete groups
        deleted_counts['groups'] = Group.query.delete()
        
        # Delete enquiries
        deleted_counts['enquiries'] = Enquiry.query.delete()
        
        # Delete users (except super admin)
        deleted_counts['users'] = User.query.filter(User.username != Config.SUPER_ADMIN_USERNAME).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Demo data cleared successfully!',
            'deleted_counts': deleted_counts
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error clearing demo data: {str(e)}'}), 500

@app.route('/api/admin/resend-email', methods=['POST'])
@token_required
def resend_email(current_user):
    # Check if user is super admin
    if current_user.username != Config.SUPER_ADMIN_USERNAME:
        return jsonify({'message': 'Admin access required!'}), 403
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'message': 'User ID required!'}), 400
        
        # Get user details
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({'message': 'User not found!'}), 404
        
        # Generate new password
        from database import generate_random_password
        new_password = generate_random_password()
        user.password = new_password
        db.session.commit()
        
        # Send welcome email with new password
        subject = '🎉 Plan My Outings - Account Credentials (Resent)'
        try:
            user_msg = Message(
                subject=subject,
                sender=app.config['MAIL_USERNAME'],
                recipients=[user.email]
            )
            user_msg.body = f"""
🎉 Welcome to Plan My Outings, {user.first_name}!
============================================

Your account credentials have been resent as requested.

👤 YOUR ACCOUNT DETAILS
------------------------
Name: {user.first_name} {user.last_name}
Email: {user.email}
Username: {user.username}
Password: {new_password} (NEW PASSWORD)

🚀 GET STARTED
--------------
1. Login to your account: http://localhost:3000/login
2. Create or join groups with friends
3. Plan amazing outings together
4. Vote on activities and locations

🔐 SECURITY TIPS
----------------
• Keep your login credentials safe
• Don't share your password with others
• You can change your password after logging in

Thank you for using Plan My Outings!

Best regards,
The Plan My Outings Team

---
This email was resent to {user.email} by system administrator.
            """
            
            mail.send(user_msg)
            # Log successful resend
            EmailTracker.log_email_sent(user.email, subject, 'resend', user.id)
            
            return jsonify({
                'message': 'Email resent successfully!',
                'new_password': new_password
            })
            
        except Exception as e:
            # Log failed resend
            EmailTracker.log_email_failed(user.email, subject, 'resend', str(e), user.id)
            return jsonify({'message': f'Failed to resend email: {str(e)}'}), 500
        
    except Exception as e:
        return jsonify({'message': f'Error resending email: {str(e)}'}), 500

def create_super_admin():
    """Create super admin account if it doesn't exist"""
    try:
        # Get super admin username, handle None case
        admin_username = app.config.get('SUPER_ADMIN_USERNAME')
        if not admin_username:
            return  # Silently skip if no username configured
            
        # Check if super admin already exists
        super_admin = User.query.filter_by(username=admin_username).first()
        
        if not super_admin:
            # Get all required fields with fallbacks
            admin_password = app.config.get('SUPER_ADMIN_PASSWORD') or 'SuperAdmin@2025'
            admin_email = app.config.get('SUPER_ADMIN_EMAIL') or 'planmyouting@outlook.com'
            admin_first_name = app.config.get('SUPER_ADMIN_FIRST_NAME') or 'Super'
            admin_last_name = app.config.get('SUPER_ADMIN_LAST_NAME') or 'Admin'
            
            super_admin = User(
                username=admin_username,
                password=admin_password,
                email=admin_email,
                first_name=admin_first_name,
                last_name=admin_last_name,
                year_of_birth=1990  # Default year
            )
            db.session.add(super_admin)
            db.session.commit()
            print(f"✅ Super admin created: {admin_username}")
            
            # Send welcome email to super admin (only if email config is available)
            mail_username = app.config.get('MAIL_USERNAME')
            mail_password = app.config.get('MAIL_PASSWORD')
            
            if mail_username and mail_password:
                try:
                    msg = Message(
                        subject='Plan My Outings - Super Admin Account Created',
                        sender=mail_username,
                        recipients=[admin_email]
                    )
                    msg.body = f"""
Super Admin Account Setup Complete

Your super admin credentials:
Username: {admin_username}
Password: {admin_password}

Admin Access:
- Web Dashboard: /admin
- API Access: All endpoints with admin privileges

Keep these credentials secure!

Plan My Outings System
                    """
                    mail.send(msg)
                    # Log super admin email
                    EmailTracker.log_email_sent(admin_email, 'Plan My Outings - Super Admin Account Created', 'admin_setup')
                    print("✅ Super admin welcome email sent")
                except Exception as e:
                    # Log failed super admin email
                    EmailTracker.log_email_failed(admin_email, 'Plan My Outings - Super Admin Account Created', 'admin_setup', str(e))
                    print(f"⚠️ Could not send super admin email: {e}")
        # Super admin already exists - no message needed
            
    except Exception as e:
        print(f"❌ Error creating super admin: {e}")

@app.route('/')
def home():
    return jsonify({"message": "Plan My Outings API"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_super_admin()
    socketio.run(app, debug=True, port=5000)
