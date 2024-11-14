FROM python:3.8-slim

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1  # Adds libGL.so.1

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code
COPY . /app

# Set environment variables, if needed
ENV FLASK_APP=app.py

# Expose the necessary ports
EXPOSE 5001

# Start the app
CMD ["python", "app.py"]
