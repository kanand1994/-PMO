from flask_socketio import SocketIO, emit, join_room, leave_room
from database import db, User, Group, Event, Vote, EventOption
import json

socketio = SocketIO(cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join_group')
def handle_join_group(data):
    group_id = data.get('group_id')
    join_room(f'group_{group_id}')
    emit('user_joined', {'message': 'A user joined the group'}, room=f'group_{group_id}')

@socketio.on('leave_group')
def handle_leave_group(data):
    group_id = data.get('group_id')
    leave_room(f'group_{group_id}')
    emit('user_left', {'message': 'A user left the group'}, room=f'group_{group_id}')

@socketio.on('create_event')
def handle_create_event(data):
    group_id = data.get('group_id')
    event_data = data.get('event_data')
    emit('new_event', {'event': event_data}, room=f'group_{group_id}')

@socketio.on('cast_vote')
def handle_cast_vote(data):
    poll_id = data.get('poll_id')
    option_id = data.get('option_id')
    user_id = data.get('user_id')
    
    # Save vote to database
    vote = Vote(poll_id=poll_id, option_id=option_id, user_id=user_id)
    db.session.add(vote)
    db.session.commit()
    
    # Get updated vote counts
    option = EventOption.query.get(option_id)
    vote_count = len(option.votes)
    
    emit('vote_update', {
        'poll_id': poll_id,
        'option_id': option_id,
        'vote_count': vote_count,
        'user_id': user_id
    }, room=f'poll_{poll_id}')

@socketio.on('send_message')
def handle_send_message(data):
    group_id = data.get('group_id')
    message_data = data.get('message')
    emit('new_message', {'message': message_data}, room=f'group_{group_id}')

@socketio.on('event_decision')
def handle_event_decision(data):
    event_id = data.get('event_id')
    decision_data = data.get('decision')
    emit('decision_made', {'decision': decision_data}, room=f'event_{event_id}')
