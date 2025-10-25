#!/usr/bin/env python3
"""
Socket.io Functionality Test
Tests real-time features of the application
"""

import socketio
import time
import threading

# Create a Socket.IO client
sio = socketio.Client()

# Event handlers
@sio.event
def connect():
    print("✅ Connected to Socket.io server")

@sio.event
def disconnect():
    print("❌ Disconnected from Socket.io server")

@sio.event
def user_joined(data):
    print(f"📥 User joined event: {data}")

@sio.event
def user_left(data):
    print(f"📤 User left event: {data}")

@sio.event
def new_event(data):
    print(f"🎉 New event created: {data}")

@sio.event
def vote_update(data):
    print(f"🗳️  Vote update: {data}")

@sio.event
def new_message(data):
    print(f"💬 New message: {data}")

def test_socketio():
    try:
        print("🔌 Testing Socket.io connectivity...")
        
        # Connect to the server
        sio.connect('http://localhost:5000')
        
        # Test joining a group
        print("🏠 Testing group join...")
        sio.emit('join_group', {'group_id': 1})
        time.sleep(1)
        
        # Test creating an event
        print("📅 Testing event creation...")
        sio.emit('create_event', {
            'group_id': 1,
            'event_data': {
                'title': 'Socket.io Test Event',
                'description': 'Testing real-time functionality',
                'event_type': 'activity'
            }
        })
        time.sleep(1)
        
        # Test sending a message
        print("💬 Testing message sending...")
        sio.emit('send_message', {
            'group_id': 1,
            'message': {
                'text': 'Hello from Socket.io test!',
                'user': 'Test User',
                'timestamp': time.time()
            }
        })
        time.sleep(1)
        
        # Test leaving group
        print("🚪 Testing group leave...")
        sio.emit('leave_group', {'group_id': 1})
        time.sleep(1)
        
        print("✅ Socket.io tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Socket.io test failed: {str(e)}")
    finally:
        sio.disconnect()

if __name__ == "__main__":
    test_socketio()