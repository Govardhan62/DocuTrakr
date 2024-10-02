# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a directory for the app
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libtesseract-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set environment variable for Tesseract path
ENV TESSERACT_PATH="/usr/bin/tesseract"

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose the port Django will run on
EXPOSE 8000

# Run the Django development server (or use gunicorn in production)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
