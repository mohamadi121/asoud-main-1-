#!/bin/bash
# ASOUD Project - Django Dependencies Installation Script

echo "🚀 Installing ASOUD Django Project Dependencies..."
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Installing pip..."
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python3 get-pip.py
    rm get-pip.py
fi

echo "✅ pip version: $(pip3 --version)"

# Upgrade pip
echo "🔄 Upgrading pip..."
pip3 install --upgrade pip

# Install Django and core dependencies
echo "🔄 Installing Django and core dependencies..."
pip3 install Django==5.1.5
pip3 install djangorestframework
pip3 install django-cors-headers
pip3 install django-hosts
pip3 install django-comments-xtd
pip3 install django-extensions

# Install database dependencies
echo "🔄 Installing database dependencies..."
pip3 install psycopg2-binary
pip3 install redis
pip3 install channels
pip3 install channels-redis

# Install async and WebSocket support
echo "🔄 Installing async and WebSocket support..."
pip3 install daphne
pip3 install uvicorn
pip3 install asgiref

# Install authentication and security
echo "🔄 Installing authentication and security..."
pip3 install django-rest-knox
pip3 install djangorestframework-simplejwt
pip3 install django-oauth-toolkit

# Install utilities
echo "🔄 Installing utility packages..."
pip3 install python-decouple
pip3 install pillow
pip3 install celery
pip3 install flower

# Install from requirements.txt if it exists
if [ -f "requirements.txt" ]; then
    echo "🔄 Installing from requirements.txt..."
    pip3 install -r requirements.txt
else
    echo "⚠️  requirements.txt not found, skipping..."
fi

echo ""
echo "✅ All dependencies installed successfully!"
echo "=================================================="
echo "📋 Next steps:"
echo "1. Set up your database configuration in .env"
echo "2. Run: python3 manage.py migrate"
echo "3. Run: python3 manage.py runserver"
echo ""
echo "🎯 Ready to start development!"