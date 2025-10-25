#!/usr/bin/env python3
"""
Plan My Outings - CLI Admin Tool
Super Admin CLI for database CRUD operations
"""

import sys
import os
from datetime import datetime
from tabulate import tabulate
from database import db, User, Group, Event, Enquiry, GroupMember, Poll, EventOption, Vote
from app import app
from config import Config

class CLIAdmin:
    def __init__(self):
        self.authenticated = False
        self.admin_user = None
        
    def authenticate(self):
        """Authenticate super admin"""
        print("🔐 Plan My Outings - Super Admin CLI")
        print("=" * 50)
        
        username = input("Username: ")
        password = input("Password: ")
        
        if (username == Config.SUPER_ADMIN_USERNAME and 
            password == Config.SUPER_ADMIN_PASSWORD):
            self.authenticated = True
            print("✅ Authentication successful!")
            print(f"Welcome, Super Admin {username}!")
            return True
        else:
            print("❌ Invalid credentials!")
            return False
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "=" * 50)
        print("📊 SUPER ADMIN DASHBOARD")
        print("=" * 50)
        print("1.  👥 User Management")
        print("2.  🏠 Group Management") 
        print("3.  📅 Event Management")
        print("4.  📝 Enquiry Management")
        print("5.  🗳️  Poll & Vote Management")
        print("6.  📊 System Statistics")
        print("7.  🔧 Database Operations")
        print("8.  📧 Send Admin Email")
        print("9.  🔄 Refresh Data")
        print("0.  🚪 Exit")
        print("=" * 50)
    
    def user_management(self):
        """User CRUD operations"""
        while True:
            print("\n👥 USER MANAGEMENT")
            print("-" * 30)
            print("1. List all users")
            print("2. Search user")
            print("3. Create user")
            print("4. Update user")
            print("5. Delete user")
            print("6. User statistics")
            print("0. Back to main menu")
            
            choice = input("\nSelect option: ")
            
            if choice == '1':
                self.list_users()
            elif choice == '2':
                self.search_user()
            elif choice == '3':
                self.create_user()
            elif choice == '4':
                self.update_user()
            elif choice == '5':
                self.delete_user()
            elif choice == '6':
                self.user_statistics()
            elif choice == '0':
                break
    
    def list_users(self):
        """List all users"""
        users = User.query.all()
        if not users:
            print("No users found.")
            return
            
        data = []
        for user in users:
            data.append([
                user.id,
                user.username,
                user.email,
                f"{user.first_name} {user.last_name}",
                user.year_of_birth,
                user.created_at.strftime("%Y-%m-%d %H:%M")
            ])
        
        headers = ["ID", "Username", "Email", "Name", "Birth Year", "Created"]
        print(f"\n📋 Total Users: {len(users)}")
        print(tabulate(data, headers=headers, tablefmt="grid"))
    
    def search_user(self):
        """Search for a user"""
        query = input("Enter username or email to search: ")
        users = User.query.filter(
            (User.username.contains(query)) | 
            (User.email.contains(query)) |
            (User.first_name.contains(query)) |
            (User.last_name.contains(query))
        ).all()
        
        if not users:
            print(f"No users found matching '{query}'")
            return
            
        data = []
        for user in users:
            groups_count = len(user.groups)
            events_count = Event.query.filter_by(created_by=user.id).count()
            
            data.append([
                user.id,
                user.username,
                user.email,
                f"{user.first_name} {user.last_name}",
                groups_count,
                events_count,
                user.created_at.strftime("%Y-%m-%d")
            ])
        
        headers = ["ID", "Username", "Email", "Name", "Groups", "Events", "Created"]
        print(f"\n🔍 Found {len(users)} users:")
        print(tabulate(data, headers=headers, tablefmt="grid"))
    
    def group_management(self):
        """Group CRUD operations"""
        while True:
            print("\n🏠 GROUP MANAGEMENT")
            print("-" * 30)
            print("1. List all groups")
            print("2. Group details")
            print("3. Delete group")
            print("4. Group statistics")
            print("0. Back to main menu")
            
            choice = input("\nSelect option: ")
            
            if choice == '1':
                self.list_groups()
            elif choice == '2':
                self.group_details()
            elif choice == '3':
                self.delete_group()
            elif choice == '4':
                self.group_statistics()
            elif choice == '0':
                break
    
    def list_groups(self):
        """List all groups"""
        groups = Group.query.all()
        if not groups:
            print("No groups found.")
            return
            
        data = []
        for group in groups:
            creator = User.query.get(group.created_by)
            member_count = len(group.members)
            event_count = len(group.events)
            
            data.append([
                group.id,
                group.name,
                group.description[:50] + "..." if len(group.description or "") > 50 else group.description or "",
                creator.username if creator else "Unknown",
                member_count,
                event_count,
                group.created_at.strftime("%Y-%m-%d")
            ])
        
        headers = ["ID", "Name", "Description", "Creator", "Members", "Events", "Created"]
        print(f"\n📋 Total Groups: {len(groups)}")
        print(tabulate(data, headers=headers, tablefmt="grid"))
    
    def system_statistics(self):
        """Show system statistics"""
        print("\n📊 SYSTEM STATISTICS")
        print("=" * 50)
        
        # Basic counts
        user_count = User.query.count()
        group_count = Group.query.count()
        event_count = Event.query.count()
        enquiry_count = Enquiry.query.count()
        
        print(f"👥 Total Users: {user_count}")
        print(f"🏠 Total Groups: {group_count}")
        print(f"📅 Total Events: {event_count}")
        print(f"📝 Total Enquiries: {enquiry_count}")
        
        # Recent activity
        print(f"\n📈 RECENT ACTIVITY (Last 7 days)")
        print("-" * 30)
        
        from datetime import timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        
        recent_users = User.query.filter(User.created_at >= week_ago).count()
        recent_groups = Group.query.filter(Group.created_at >= week_ago).count()
        recent_events = Event.query.filter(Event.created_at >= week_ago).count()
        recent_enquiries = Enquiry.query.filter(Enquiry.created_at >= week_ago).count()
        
        print(f"New Users: {recent_users}")
        print(f"New Groups: {recent_groups}")
        print(f"New Events: {recent_events}")
        print(f"New Enquiries: {recent_enquiries}")
        
        # Top users by activity
        print(f"\n🏆 TOP ACTIVE USERS")
        print("-" * 30)
        
        users_with_activity = []
        for user in User.query.all():
            groups_created = Group.query.filter_by(created_by=user.id).count()
            events_created = Event.query.filter_by(created_by=user.id).count()
            total_activity = groups_created + events_created
            
            if total_activity > 0:
                users_with_activity.append([
                    user.username,
                    f"{user.first_name} {user.last_name}",
                    groups_created,
                    events_created,
                    total_activity
                ])
        
        users_with_activity.sort(key=lambda x: x[4], reverse=True)
        
        if users_with_activity:
            headers = ["Username", "Name", "Groups", "Events", "Total"]
            print(tabulate(users_with_activity[:10], headers=headers, tablefmt="grid"))
        else:
            print("No user activity found.")
    
    def database_operations(self):
        """Database maintenance operations"""
        while True:
            print("\n🔧 DATABASE OPERATIONS")
            print("-" * 30)
            print("1. Backup database")
            print("2. Clean old enquiries")
            print("3. Reset demo data")
            print("4. Database info")
            print("5. ⚠️  DANGER: Clear all data")
            print("0. Back to main menu")
            
            choice = input("\nSelect option: ")
            
            if choice == '1':
                self.backup_database()
            elif choice == '2':
                self.clean_old_enquiries()
            elif choice == '3':
                self.reset_demo_data()
            elif choice == '4':
                self.database_info()
            elif choice == '5':
                self.clear_all_data()
            elif choice == '0':
                break
    
    def backup_database(self):
        """Create database backup"""
        import shutil
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"plan_my_outings_backup_{timestamp}.db"
        
        try:
            shutil.copy2("plan_my_outings.db", backup_name)
            print(f"✅ Database backed up to: {backup_name}")
        except Exception as e:
            print(f"❌ Backup failed: {e}")
    
    def run(self):
        """Main CLI loop"""
        if not self.authenticate():
            sys.exit(1)
        
        while True:
            self.show_menu()
            choice = input("\nSelect option: ")
            
            if choice == '1':
                self.user_management()
            elif choice == '2':
                self.group_management()
            elif choice == '3':
                print("📅 Event management - Coming soon!")
            elif choice == '4':
                print("📝 Enquiry management - Coming soon!")
            elif choice == '5':
                print("🗳️ Poll management - Coming soon!")
            elif choice == '6':
                self.system_statistics()
            elif choice == '7':
                self.database_operations()
            elif choice == '8':
                print("📧 Email management - Coming soon!")
            elif choice == '9':
                print("🔄 Data refreshed!")
            elif choice == '0':
                print("👋 Goodbye, Super Admin!")
                break
            else:
                print("❌ Invalid option. Please try again.")

if __name__ == "__main__":
    with app.app_context():
        admin = CLIAdmin()
        admin.run()