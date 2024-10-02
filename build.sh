#!/bin/bash

# Update package lists
apt-get update

# Install Tesseract OCR
apt-get install -y tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev

# Optionally install additional languages (if needed)
# apt-get install -y tesseract-ocr-fra tesseract-ocr-deu

# Install Python dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input
