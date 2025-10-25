#!/usr/bin/env python3
"""
Comprehensive Test Suite for Plan My Outings Application
Tests both backend API endpoints and frontend functionality
"""

import requests
import json
import time
import sys

# Configuration
BACKEND_URL = "http://localhost:5000"
FRONTEND_URL = "http://localhost:3000"

class TestRunner:
    def __init__(self):
        self.token = None
        self.user_data = None
        self.test_results = []
        
    def log_test(self, test_name, success, message=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        self.test_results.append({
            'test': test_name,
            'success': success,
            'message': message
        })
    
    def test_backend_health(self):
        """Test if backend server is running"""
        try:
            response = requests.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                data = response.json()
                self.log_test("Backend Health Check", True, f"Server running: {data['message']}")
                return True
            else:
                self.log_test("Backend Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Backend Health Check", False, f"Connection error: {str(e)}")
            return False
    
    def test_contact_enquiry(self):
        """Test contact form and auto user creation"""
        try:
            test_data = {
                "first_name": "TestUser",
                "last_name": "Automated",
                "email": "testuser@automated.com",
                "year_of_birth": 1995,
                "message": "Automated test enquiry"
            }
            
            response = requests.post(f"{BACKEND_URL}/api/contact", json=test_data)
            if response.status_code == 200:
                data = response.json()
                if 'credentials' in data:
                    self.test_credentials = data['credentials']
                    self.log_test("Contact Enquiry & User Creation", True, 
                                f"User created: {self.test_credentials['username']}")
                    return True
                else:
                    self.log_test("Contact Enquiry & User Creation", False, "No credentials returned")
                    return False
            else:
                self.log_test("Contact Enquiry & User Creation", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Contact Enquiry & User Creation", False, f"Error: {str(e)}")
            return False
    
    def test_authentication(self):
        """Test login functionality"""
        try:
            if not hasattr(self, 'test_credentials'):
                self.log_test("Authentication", False, "No test credentials available")
                return False
                
            login_data = {
                "username": self.test_credentials['username'],
                "password": self.test_credentials['password']
            }
            
            response = requests.post(f"{BACKEND_URL}/api/login", json=login_data)
            if response.status_code == 200:
                data = response.json()
                if 'token' in data and 'user' in data:
                    self.token = data['token']
                    self.user_data = data['user']
                    self.log_test("Authentication", True, f"Login successful for {data['user']['username']}")
                    return True
                else:
                    self.log_test("Authentication", False, "Invalid response format")
                    return False
            else:
                self.log_test("Authentication", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Authentication", False, f"Error: {str(e)}")
            return False
    
    def test_groups_functionality(self):
        """Test group creation and retrieval"""
        if not self.token:
            self.log_test("Groups Functionality", False, "No authentication token")
            return False
            
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            # Test getting groups (should be empty initially)
            response = requests.get(f"{BACKEND_URL}/api/groups", headers=headers)
            if response.status_code == 200:
                groups = response.json()
                self.log_test("Get Groups", True, f"Retrieved {len(groups)} groups")
            else:
                self.log_test("Get Groups", False, f"Status: {response.status_code}")
                return False
            
            # Test creating a group
            group_data = {
                "name": "Test Automation Group",
                "description": "Group created by automated testing"
            }
            
            response = requests.post(f"{BACKEND_URL}/api/groups", json=group_data, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'group_id' in data:
                    self.test_group_id = data['group_id']
                    self.log_test("Create Group", True, f"Group created with ID: {data['group_id']}")
                    return True
                else:
                    self.log_test("Create Group", False, "No group ID returned")
                    return False
            else:
                self.log_test("Create Group", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Groups Functionality", False, f"Error: {str(e)}")
            return False
    
    def test_events_functionality(self):
        """Test event creation"""
        if not self.token or not hasattr(self, 'test_group_id'):
            self.log_test("Events Functionality", False, "Missing token or group ID")
            return False
            
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            event_data = {
                "title": "Automated Test Event",
                "description": "Event created by automated testing",
                "event_type": "dinner",
                "group_id": self.test_group_id
            }
            
            response = requests.post(f"{BACKEND_URL}/api/events", json=event_data, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if 'event_id' in data:
                    self.log_test("Create Event", True, f"Event created with ID: {data['event_id']}")
                    return True
                else:
                    self.log_test("Create Event", False, "No event ID returned")
                    return False
            else:
                self.log_test("Create Event", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Events Functionality", False, f"Error: {str(e)}")
            return False
    
    def test_api_integrations(self):
        """Test external API integrations"""
        if not self.token:
            self.log_test("API Integrations", False, "No authentication token")
            return False
            
        headers = {'Authorization': f'Bearer {self.token}'}
        
        try:
            # Test Places API
            response = requests.get(f"{BACKEND_URL}/api/places/search?query=restaurant&location=40.7128,-74.0060", headers=headers)
            if response.status_code == 200:
                places = response.json()
                self.log_test("Places API", True, f"Retrieved {len(places)} places (may be empty due to API key)")
            else:
                self.log_test("Places API", False, f"Status: {response.status_code}")
            
            # Test Movies API
            response = requests.get(f"{BACKEND_URL}/api/movies/search?query=action", headers=headers)
            if response.status_code == 200:
                movies = response.json()
                self.log_test("Movies API", True, f"Retrieved {len(movies)} movies (may be empty due to API key)")
            else:
                self.log_test("Movies API", False, f"Status: {response.status_code}")
            
            # Test Weather API
            response = requests.get(f"{BACKEND_URL}/api/weather/forecast?lat=40.7128&lon=-74.0060", headers=headers)
            if response.status_code == 200:
                weather = response.json()
                self.log_test("Weather API", True, f"Retrieved {len(weather)} weather entries (may be empty due to API key)")
            else:
                self.log_test("Weather API", False, f"Status: {response.status_code}")
                
            return True
            
        except Exception as e:
            self.log_test("API Integrations", False, f"Error: {str(e)}")
            return False
    
    def test_frontend_accessibility(self):
        """Test if frontend is accessible"""
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.log_test("Frontend Accessibility", True, "Frontend server is running")
                return True
            else:
                self.log_test("Frontend Accessibility", False, f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Frontend Accessibility", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting Comprehensive Test Suite for Plan My Outings")
        print("=" * 60)
        
        # Backend Tests
        print("\n📡 BACKEND TESTS")
        print("-" * 30)
        
        if not self.test_backend_health():
            print("❌ Backend is not running. Please start the backend server first.")
            return
        
        self.test_contact_enquiry()
        self.test_authentication()
        self.test_groups_functionality()
        self.test_events_functionality()
        self.test_api_integrations()
        
        # Frontend Tests
        print("\n🌐 FRONTEND TESTS")
        print("-" * 30)
        self.test_frontend_accessibility()
        
        # Summary
        print("\n📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        total = len(self.test_results)
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! The application is working correctly.")
        else:
            print(f"\n⚠️  {total - passed} tests failed. Check the details above.")
            
        return passed == total

if __name__ == "__main__":
    tester = TestRunner()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)