#!/bin/bash

# Update the package lists
apt-get update

# Install Tesseract
apt-get install -y tesseract-ocr

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input
