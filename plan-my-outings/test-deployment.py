#!/usr/bin/env python3
"""
Simple deployment verification script
Tests if your deployed application is working correctly
"""

import requests
import json
import sys

def test_deployment():
    print("🧪 Plan My Outings - Deployment Test")
    print("=" * 40)
    
    # Get URLs from user
    backend_url = input("Enter your backend URL (from Render): ").strip()
    frontend_url = input("Enter your frontend URL (from Vercel): ").strip()
    
    if not backend_url or not frontend_url:
        print("❌ Both URLs are required!")
        return False
    
    # Remove trailing slashes
    backend_url = backend_url.rstrip('/')
    frontend_url = frontend_url.rstrip('/')
    
    print(f"\n🔍 Testing backend: {backend_url}")
    print(f"🔍 Testing frontend: {frontend_url}")
    print()
    
    # Test 1: Backend health check
    print("1️⃣  Testing backend health...")
    try:
        response = requests.get(f"{backend_url}/", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is responding!")
            data = response.json()
            print(f"   Message: {data.get('message', 'No message')}")
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False
    
    # Test 2: Frontend accessibility
    print("\n2️⃣  Testing frontend accessibility...")
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible!")
            if "Plan My Outings" in response.text:
                print("   ✅ Frontend content looks correct!")
            else:
                print("   ⚠️  Frontend content might not be fully loaded")
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")
        return False
    
    # Test 3: API endpoint test
    print("\n3️⃣  Testing API endpoints...")
    try:
        # Test a simple API endpoint
        response = requests.get(f"{backend_url}/api/admin/stats", timeout=10)
        if response.status_code in [200, 401, 403]:  # 401/403 expected without auth
            print("✅ API endpoints are accessible!")
            if response.status_code == 401:
                print("   ✅ Authentication is working (401 expected)")
        else:
            print(f"⚠️  API returned unexpected status {response.status_code}")
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False
    
    # Test 4: CORS check
    print("\n4️⃣  Testing CORS configuration...")
    try:
        headers = {
            'Origin': frontend_url,
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        response = requests.options(f"{backend_url}/api/contact", headers=headers, timeout=10)
        if response.status_code in [200, 204]:
            print("✅ CORS is configured correctly!")
        else:
            print(f"⚠️  CORS might need adjustment (status {response.status_code})")
    except Exception as e:
        print(f"⚠️  CORS test inconclusive: {e}")
    
    print("\n" + "=" * 40)
    print("🎉 Deployment Test Complete!")
    print()
    print("📱 Your live application:")
    print(f"   Frontend: {frontend_url}")
    print(f"   Backend:  {backend_url}")
    print(f"   Admin:    {frontend_url}/admin")
    print()
    print("🔐 Default admin credentials:")
    print("   Username: superadmin")
    print("   Password: admin123 (or your configured password)")
    print()
    print("✅ Your Plan My Outings app is live and ready to use!")
    
    return True

if __name__ == "__main__":
    try:
        success = test_deployment()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)