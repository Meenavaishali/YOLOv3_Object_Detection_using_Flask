# Use a Python image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy UI backend code
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
