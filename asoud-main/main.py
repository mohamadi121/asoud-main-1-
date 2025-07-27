"""
Main application entry point for ASOUD Django project
Imports the WSGI application to make it available for deployment
"""

import os
import sys

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

# Import the WSGI application
from django.core.wsgi import get_wsgi_application

# Make the app available for deployment platforms
application = get_wsgi_application()
app = application

if __name__ == "__main__":
    # For development server
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)