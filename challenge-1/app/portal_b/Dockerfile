# Use a Python base image
FROM python:3.12.7

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY . .

# Expose port 5001 for app2
EXPOSE 5003

# Run the Flask app
CMD ["python", "app.py"]
