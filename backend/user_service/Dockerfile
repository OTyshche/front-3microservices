FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5001

# Set the environment variable for Flask
CMD ["python3", "user_service.py"]