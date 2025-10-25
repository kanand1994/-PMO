#!/usr/bin/env python3
"""
Simple functionality test to verify core features
"""

import requests
import json
import time
import random

def test_basic_functionality():
    print("🧪 Simple Functionality Test")
    print("=" * 40)
    
    base_url = "http://localhost:5000"
    
    # Generate unique email to avoid conflicts
    random_id = random.randint(1000, 9999)
    
    # Test 1: Contact form
    print("1. Testing contact form...")
    contact_data = {
        "first_name": "Simple",
        "last_name": "Test",
        "email": f"simple{random_id}@test.com",
        "year_of_birth": 1990,
        "message": "Simple test message"
    }
    
    try:
        response = requests.post(f"{base_url}/api/contact", json=contact_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            credentials = data['credentials']
            print(f"✅ Contact form works - User: {credentials['username']}")
        else:
            print(f"❌ Contact form failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Contact form error: {str(e)}")
        return False
    
    # Test 2: Login
    print("2. Testing login...")
    try:
        login_data = {
            "username": credentials['username'],
            "password": credentials['password']
        }
        response = requests.post(f"{base_url}/api/login", json=login_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            token = data['token']
            print("✅ Login works")
        else:
            print(f"❌ Login failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Login error: {str(e)}")
        return False
    
    # Test 3: Create group
    print("3. Testing group creation...")
    try:
        headers = {'Authorization': f'Bearer {token}'}
        group_data = {
            "name": f"Test Group {random_id}",
            "description": "Simple test group"
        }
        response = requests.post(f"{base_url}/api/groups", json=group_data, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            group_id = data['group_id']
            print(f"✅ Group creation works - ID: {group_id}")
        else:
            print(f"❌ Group creation failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Group creation error: {str(e)}")
        return False
    
    # Test 4: Create event
    print("4. Testing event creation...")
    try:
        event_data = {
            "title": f"Test Event {random_id}",
            "description": "Simple test event",
            "event_type": "dinner",
            "group_id": group_id
        }
        response = requests.post(f"{base_url}/api/events", json=event_data, headers=headers, timeout=10)
        if response.status_code == 200:
            print("✅ Event creation works")
        else:
            print(f"❌ Event creation failed - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Event creation error: {str(e)}")
        return False
    
    print("\n🎉 All basic functionality tests PASSED!")
    return True

if __name__ == "__main__":
    success = test_basic_functionality()
    if success:
        print("\n✨ Application is working correctly!")
    else:
        print("\n❌ Some tests failed!")