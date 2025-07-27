#!/usr/bin/env python3
"""
Script to fix migration dependencies for ASOUD project
This script creates initial migrations for all apps to resolve dependency issues
"""

import os
import sys
import django
from django.conf import settings
from django.core.management import execute_from_command_line

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Setup Django
django.setup()

def fix_migrations():
    """Fix migration dependencies by creating migrations in correct order"""
    
    print("🔧 Fixing migration dependencies for ASOUD...")
    
    # Step 1: Create users migration first (most critical)
    print("📝 Creating users app migration...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'users'])
        print("✅ Users migration created successfully")
    except Exception as e:
        print(f"⚠️  Users migration issue: {e}")
    
    # Step 2: Create base app migration  
    print("📝 Creating base app migration...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations', 'base'])
        print("✅ Base migration created successfully")
    except Exception as e:
        print(f"⚠️  Base migration issue: {e}")
    
    # Step 3: Create all other migrations
    print("📝 Creating all remaining migrations...")
    try:
        execute_from_command_line(['manage.py', 'makemigrations'])
        print("✅ All migrations created successfully")
    except Exception as e:
        print(f"⚠️  Migration creation issue: {e}")
    
    # Step 4: Show migration status
    print("📊 Checking migration status...")
    try:
        execute_from_command_line(['manage.py', 'showmigrations'])
    except Exception as e:
        print(f"⚠️  Show migrations issue: {e}")
    
    print("🎯 Migration fix completed!")
    print("\nNext steps:")
    print("1. Review the created migrations")
    print("2. Run: python manage.py migrate")
    print("3. Start your development server")

if __name__ == '__main__':
    fix_migrations()