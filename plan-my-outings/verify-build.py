#!/usr/bin/env python3
"""
Verify that the build is ready for unified deployment
"""

import os
import json

def verify_build():
    print("🔍 Verifying Build for Unified Deployment")
    print("=" * 45)
    
    # Check if frontend build exists
    build_path = os.path.join("frontend", "build")
    if os.path.exists(build_path):
        print("✅ Frontend build folder exists")
        
        # Check for index.html
        index_path = os.path.join(build_path, "index.html")
        if os.path.exists(index_path):
            print("✅ Frontend index.html exists")
        else:
            print("❌ Frontend index.html missing")
            return False
            
        # Check for static assets
        static_path = os.path.join(build_path, "static")
        if os.path.exists(static_path):
            print("✅ Frontend static assets exist")
        else:
            print("❌ Frontend static assets missing")
            return False
    else:
        print("❌ Frontend build folder missing")
        print("   Run: build-for-deployment.bat")
        return False
    
    # Check backend files
    backend_files = [
        "backend/app.py",
        "backend/requirements.txt",
        "backend/config_production.py"
    ]
    
    for file_path in backend_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            return False
    
    # Check if app.py has unified serving code
    with open("backend/app.py", "r", encoding="utf-8") as f:
        app_content = f.read()
        if "serve_frontend" in app_content:
            print("✅ Backend configured for unified serving")
        else:
            print("❌ Backend not configured for unified serving")
            return False
    
    print("\n🎉 Build Verification Complete!")
    print("\n📋 Your application is ready for unified deployment:")
    print("   - Frontend built and ready")
    print("   - Backend configured to serve frontend")
    print("   - Single URL deployment ready")
    print("\n🚀 Next step: Deploy to Render")
    print("   See UNIFIED-DEPLOY.md for instructions")
    
    return True

if __name__ == "__main__":
    success = verify_build()
    exit(0 if success else 1)