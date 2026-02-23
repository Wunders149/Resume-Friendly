#!/bin/bash
# CV Forge - Resume Builder
# Quick start script for macOS/Linux

echo ""
echo "======================================"
echo "  CV Forge - Resume Builder"
echo "======================================"
echo ""

# Check if venv exists
if [ -d "venv" ]; then
    echo "Virtual environment found. Activating..."
else
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install/Update requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# Run the app
echo ""
echo "Starting CV Forge..."
echo ""
python3 app.py

