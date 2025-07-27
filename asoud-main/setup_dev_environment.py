#!/usr/bin/env python3
"""
Complete development environment setup for ASOUD project
This script handles all necessary setup steps including migrations and initial data
"""

import os
import sys
import django
import subprocess
from django.conf import settings
from django.core.management import execute_from_command_line

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

def run_command(command, description):
    """Run a command and handle errors gracefully"""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, list):
            execute_from_command_line(command)
        else:
            subprocess.run(command, shell=True, check=True)
        print(f"✅ {description} completed successfully")
        return True
    except Exception as e:
        print(f"⚠️  {description} failed: {e}")
        return False

def setup_development_environment():
    """Complete setup for development environment"""
    
    print("🚀 Setting up ASOUD development environment...")
    print("=" * 50)
    
    # Setup Django
    django.setup()
    
    # Step 1: Check database connection
    print("🔍 Checking database connection...")
    try:
        from django.db import connection
        cursor = connection.cursor()
        print("✅ Database connection successful")
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("Please check your database configuration in .env or .env.docker")
        return False
    
    # Step 2: Create migrations in correct order
    steps = [
        (['manage.py', 'makemigrations', 'users'], "Creating users migrations"),
        (['manage.py', 'makemigrations', 'base'], "Creating base migrations"),
        (['manage.py', 'makemigrations'], "Creating all remaining migrations"),
        (['manage.py', 'migrate'], "Applying all migrations"),
        (['manage.py', 'collectstatic', '--noinput'], "Collecting static files"),
    ]
    
    for command, description in steps:
        if not run_command(command, description):
            print(f"❌ Setup failed at: {description}")
            return False
    
    # Step 3: Create superuser (optional)
    print("\n🔐 Creating superuser (optional)...")
    print("You can skip this step and create superuser later with: python manage.py createsuperuser")
    create_superuser = input("Create superuser now? (y/N): ").lower().strip()
    
    if create_superuser == 'y':
        run_command(['manage.py', 'createsuperuser'], "Creating superuser")
    
    # Step 4: Final status check
    print("\n📊 Final system check...")
    run_command(['manage.py', 'check'], "System check")
    run_command(['manage.py', 'showmigrations'], "Migration status")
    
    print("\n🎉 Development environment setup completed!")
    print("=" * 50)
    print("🚀 Ready to start development!")
    print("\nNext steps:")
    print("1. For Docker: docker-compose -f docker-compose.dev.yaml up")
    print("2. For local: python manage.py runserver")
    print("3. Access admin at: http://localhost:8000/admin/")
    print("4. API docs at: http://localhost:8000/api/docs/")
    
    return True

if __name__ == '__main__':
    setup_development_environment()